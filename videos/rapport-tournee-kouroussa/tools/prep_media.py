"""Prepare every image and clip of the report film: clean, cut, correct, grade.

1. Clean (OpenCV), only what is not part of a face, a crowd, a place or a garment:
   the camera stamps « Galaxy A54 5G » are inpainted (text pixels only), the car plate of 03 is blurred,
   the green « AN » plates of the convoy clip are found on every frame and blurred. The CapCut mark of
   video 20 is cropped out. Garments are left untouched (client rule).
2. Clips: short segments of 20_video-accueil-populations.mp4 (muted, cropped 608x342).
3. Correction: `hyperframes media-treatment --analyze` measures each source and suggests a bounded
   primary correction (exposure, white balance).
4. Grade: that correction plus one shared warm look (tools/grades.json "warm"), validated by the CLI,
   rendered once by HyperFrames' own shader on an identity Hald CLUT (`hyperframes snapshot`), then
   applied with ffmpeg `haldclut` to the photo or clip. Same look on stills and moving footage, and no
   WebGL at render time (this container has no GPU).

Outputs: assets/prep/<key>.jpg, assets/prep/clips/<key>.mp4, tools/grades.lock.json
Usage: <venv>/bin/python -I tools/prep_media.py <project dir> [KEY ...]
"""
import hashlib, html, json, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import cv2
import numpy as np

ROOT = Path(sys.argv[1]).resolve()
ONLY = set(sys.argv[2:])
CLI = ["npx", "--yes", "hyperframes@0.8.141"]
PREP, CLEAN, WORK = ROOT / "assets/prep", ROOT / "assets/prep/clean", ROOT / ".hyperframes/prep"
for d in (PREP, CLEAN, WORK, PREP / "clips"):
    d.mkdir(parents=True, exist_ok=True)
M, I = ROOT / "assets/mission", ROOT / "assets/illustration"
V20 = M / "20_video-accueil-populations.mp4"

PHOTOS = {
    "m01": "01_hon-lamine-kouyate-portrait-exterieur.jpg", "m02": "02_hon-dre-hadja-djoran-keita-accueil.jpg",
    "m03": "03_prefecture-kouroussa-bloc-administratif.jpg", "m04": "04_delegation-marche-terrain.jpg",
    "m05": "05_officiels-sous-tente.jpg", "m06": "06_assemblee-des-femmes-20-sept.jpg",
    "m07": "07_assemblee-des-femmes-2.jpg", "m08": "08_accueil-officiels-echarpes.jpg",
    "m09": "09_rencontre-plein-air-communaute.jpg", "m10": "10_banniere-bienvenue-chez-toi.jpg",
    "m12": "12_hon-keita-reunion-site-minier.jpg", "m13": "13_reunion-des-sages.jpg",
    "m14": "14_hon-lamine-kouyate-portrait.jpg", "m18": "18_hon-keita-prise-de-parole.jpg",
    "i01": "01_eau-potable-jerricans.jpg", "i02": "02_sante-batiment-de-sante.jpg",
    "i03": "03_agriculture-champ.jpg", "i04": "04_electricite-enfant-a-la-bougie.jpg",
}
# (start s, duration s) in video 20
CLIPS = {"v-convoi": (18.0, 4.2), "v-jeunesse": (34.0, 4.2), "v-sankarani": (125.4, 4.2), "v-foule": (68.0, 3.0)}
CROP = "crop=608:342:32:18"   # removes the CapCut mark (top-left corner)

# camera stamps: box (x0, y0, x1, y1) in source pixels; only the white text pixels inside are inpainted
STAMPS = {"m04": [(24, 422, 128, 443)], "m07": [(24, 423, 128, 443)], "m06": [(110, 1694, 486, 1760)]}
PLATES = {"m03": [(40, 910, 116, 945)]}


def src_path(key):
    return (I if key.startswith("i") else M) / PHOTOS[key]


def clean_photo(key):
    img = cv2.imread(str(src_path(key)))
    for (x0, y0, x1, y1) in STAMPS.get(key, []):
        roi = img[y0:y1, x0:x1]
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        text = ((hsv[..., 2] > 200) & (hsv[..., 1] < 60)).astype(np.uint8) * 255
        text = cv2.dilate(text, np.ones((3, 3), np.uint8), iterations=2)
        mask = np.zeros(img.shape[:2], np.uint8); mask[y0:y1, x0:x1] = text
        img = cv2.inpaint(img, mask, 5, cv2.INPAINT_TELEA)
    for (x0, y0, x1, y1) in PLATES.get(key, []):
        img[y0:y1, x0:x1] = cv2.GaussianBlur(img[y0:y1, x0:x1], (0, 0), 9)
    out = CLEAN / f"{key}.png"
    cv2.imwrite(str(out), img)
    return out


def blur_green_plates(frame):
    """Blur the mint-green « AN » plates (hue ~150-170 deg, saturated, bright); grass is yellow-green."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[..., 0].astype(int), hsv[..., 1], hsv[..., 2]
    m = ((h >= 66) & (h <= 92) & (s > 70) & (v > 120)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 17), np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m)
    out = frame.copy()
    for i in range(1, n):
        x, y, w, hh, area = stats[i]
        if area < 6 or w < 4 or w > 110 or hh > 34 or w < hh * 1.3:
            continue
        px, py = max(6, int(0.45 * w)), max(5, int(0.5 * hh))   # the white lettering splits the green: pad wide
        x0, y0 = max(0, x - px), max(0, y - py); x1, y1 = min(frame.shape[1], x + w + px), min(frame.shape[0], y + hh + py)
        out[y0:y1, x0:x1] = cv2.GaussianBlur(out[y0:y1, x0:x1], (0, 0), 7)
    return out


def cut_clip(key):
    t0, dur = CLIPS[key]
    raw = WORK / f"{key}.raw.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t0), "-i", str(V20), "-t", str(dur), "-an",
                    "-vf", CROP, "-c:v", "libx264", "-crf", "12", "-preset", "fast", str(raw)], check=True)
    if key != "v-convoi":
        return raw
    cap = cv2.VideoCapture(str(raw)); frames = []
    while True:
        ok, f = cap.read()
        if not ok: break
        frames.append(blur_green_plates(f))
    h, w = frames[0].shape[:2]
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", "30",
                          "-i", "-", "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p",
                          str(WORK / f"{key}.clean.mp4")], stdin=subprocess.PIPE)
    for f in frames:
        p.stdin.write(f.tobytes())
    p.stdin.close(); p.wait()
    cv2.imwrite(str(WORK / f"{key}.check.png"), np.vstack([frames[0], frames[len(frames) // 2], frames[-1]]))
    return WORK / f"{key}.clean.mp4"


def sha(path):
    return hashlib.sha1(Path(path).read_bytes()).hexdigest()[:16]


def analyze(key, media):
    d = WORK / "analyze" / key; d.mkdir(parents=True, exist_ok=True)
    ext = media.suffix
    shutil.copy(media, d / f"m{ext}")
    tag = f'<video id="m" src="m{ext}" muted></video>' if ext == ".mp4" else f'<img id="m" src="m{ext}" alt="">'
    (d / "index.html").write_text(f'<!doctype html><html><body><div data-composition-id="probe" data-width="16" '
                                  f'data-height="16" data-duration="1">{tag}</div></body></html>')
    res = subprocess.run(CLI + ["media-treatment", "--file", str((d / "index.html").relative_to(ROOT)), "--selector", "#m",
                                "--analyze", "--json"], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(res.stdout)
    return out["suggestedPatch"]["adjust"], out["diagnosis"]


def canonical(patch):
    probe = WORK / "grade-probe.html"
    probe.write_text('<!doctype html><html><body><div data-composition-id="probe" data-width="16" data-height="16" '
                     'data-duration="1"><img id="probe" src="probe.jpg" alt=""></div></body></html>')
    res = subprocess.run(CLI + ["media-treatment", "--file", str(probe.relative_to(ROOT)), "--selector", "#probe",
                                "--grading", json.dumps(patch), "--apply", "--json"], cwd=ROOT, check=True,
                         capture_output=True, text=True)
    out = json.loads(res.stdout)
    if not out.get("ok"): raise SystemExit(res.stdout)
    return out["after"]


def graded_clut(payload):
    """Render the identity Hald CLUT (level 8, 512x512) through HyperFrames' grading shader."""
    key = hashlib.sha1(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:12]
    d = WORK / "clut" / key; out = d / "clut.png"
    if out.exists(): return out
    shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "haldclutsrc=8", "-frames:v", "1", str(d / "hald.png")], check=True)
    shutil.copy(ROOT / "assets/vendor/gsap.min.js", d / "gsap.min.js")
    shutil.copy(ROOT / "hyperframes.json", d / "hyperframes.json")
    attr = html.escape(json.dumps(payload, separators=(",", ":")), quote=True)
    (d / "index.html").write_text(
        '<!doctype html><html><head><meta charset="UTF-8"><script src="gsap.min.js"></script><style>html,body{margin:0;width:512px;height:512px;overflow:hidden;background:#000}'
        '#root{position:relative;width:512px;height:512px}img{position:absolute;left:0;top:0;width:512px;height:512px;image-rendering:pixelated}</style></head><body>'
        '<div id="root" data-composition-id="main" data-width="512" data-height="512" data-duration="1">'
        f'<img class="clip" data-start="0" data-duration="1" src="hald.png" alt="" data-color-grading="{attr}"></div>'
        '<script>window.__timelines=window.__timelines||{};window.__timelines["main"]=gsap.timeline({paused:true});</script>'
        '</body></html>')
    subprocess.run(CLI + ["snapshot", str(d), "--at", "0.5", "--no-end", "--describe", "false", "--timeout", "90000", "-o", str(d / "snap")],
                   check=True, capture_output=True, text=True)
    shutil.copy(next((d / "snap").glob("frame-*.png")), out)
    return out


def apply_clut(media, clut, dest):
    if dest.suffix == ".mp4":
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(media), "-i", str(clut), "-filter_complex", "[0:v][1:v]haldclut=interp=tetrahedral,format=yuv420p",
               "-an", "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-movflags", "+faststart", str(dest)]
    else:
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(media), "-i", str(clut), "-filter_complex", "[0:v][1:v]haldclut=interp=tetrahedral",
               "-frames:v", "1", "-q:v", "2", str(dest)]
    subprocess.run(cmd, check=True)


LIMITS = {"exposure": (-1, 1), "contrast": (-1, 1), "blacks": (-1, 1), "whites": (-1, 1), "temperature": (-1, 1), "tint": (-1, 1)}


def merged(look, corr, scale):
    p = json.loads(json.dumps(look))
    adj = p.setdefault("adjust", {})
    for k, v in corr.items():
        lo, hi = LIMITS.get(k, (-1, 1))
        adj[k] = round(min(hi, max(lo, adj.get(k, 0) + v * scale)), 4)
    return p


def main():
    looks = json.loads((ROOT / "tools/grades.json").read_text())
    lock_path = ROOT / "tools/grades.lock.json"
    lock = json.loads(lock_path.read_text()) if lock_path.exists() else {}
    keys = [k for k in list(PHOTOS) + list(CLIPS) if not ONLY or k in ONLY]

    def stage(key):
        media = cut_clip(key) if key in CLIPS else clean_photo(key)
        digest = sha(media)
        ent = lock.get(key, {})
        if ent.get("source") != digest:
            corr, diag = analyze(key, media)
            ent = {"source": digest, "correction": corr, "diagnosis": diag}
        return key, media, ent

    with ThreadPoolExecutor(3) as ex:
        staged = list(ex.map(stage, keys))
    for key, media, ent in staged:
        look_name = "warm"
        payload = merged(looks[look_name], ent["correction"], looks.get("_correction_scale", 1.0))
        if ent.get("patch") != payload:
            ent["patch"] = payload; ent["canonical"] = canonical(payload)
        ent["look"] = look_name
        lock[key] = ent
    lock_path.write_text(json.dumps(lock, indent=1, ensure_ascii=False) + "\n")

    def finish(item):
        key, media, _ = item
        clut = graded_clut(lock[key]["canonical"])
        dest = PREP / "clips" / f"{key}.mp4" if key in CLIPS else PREP / f"{key}.jpg"
        apply_clut(media, clut, dest)
        print("prepared", key, "corr", lock[key]["correction"], flush=True)
    with ThreadPoolExecutor(2) as ex:
        list(ex.map(finish, staged))


if __name__ == "__main__":
    main()
