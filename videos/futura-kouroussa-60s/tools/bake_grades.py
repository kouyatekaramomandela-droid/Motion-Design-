"""Bake the photo grades into still images with HyperFrames' own shader.

Why: this container has no GPU. Real-time `data-color-grading` runs through SwiftShader and stalls the
render (measured: ~6 s per frame for two small graded images, no progress at all for full-frame plates).
The grades are static, so each one is computed once by `hyperframes snapshot` on the full photo and on its
clean plate, then the film animates plain images (seek-safe, fast). Film grain is animated, so it is not
baked: it is added to the final encode (tools/finish.sh).

Outputs: assets/photos/graded/<photo>.<grade>-bg.jpg (graded clean plate)
         assets/photos/graded/<photo>.<grade>-fg.png (graded photo cut by the nearest-plane alpha)
Usage: python3 tools/bake_grades.py   (from the project root; needs the venv with numpy + opencv for the cut)
"""
import hashlib, html, json, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build import load_grades, ROOT, CLI  # noqa: E402

PHOTOS = ROOT / "assets/photos"
OUT = PHOTOS / "graded"
WORK = ROOT / ".hyperframes/bake"
JOBS = [("A-pont-niger", "land"), ("A-pont-niger", "land-dark"), ("C-mine", "mine"), ("C-mine", "mine-sunk"),
        ("D-forage", "people"), ("D-forage", "dry"), ("D-forage", "gold"), ("R-reunion", "office")]


def size(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height", "-of", "csv=p=0", str(path)],
                         check=True, capture_output=True, text=True).stdout.strip().split(",")
    return int(out[0]), int(out[1])


def snap(src, payload, dest):
    """Grade one image at its native size and save the graded pixels as PNG."""
    w, h = size(src)
    key = hashlib.sha1((json.dumps(payload, sort_keys=True) + src.name).encode()).hexdigest()[:12]
    d = WORK / key
    if (d / "graded.png").exists():
        shutil.copy(d / "graded.png", dest); return
    shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
    shutil.copy(src, d / src.name)
    shutil.copy(ROOT / "assets/vendor/gsap.min.js", d / "gsap.min.js")
    shutil.copy(ROOT / "hyperframes.json", d / "hyperframes.json")
    attr = html.escape(json.dumps(payload, separators=(",", ":")), quote=True)
    (d / "index.html").write_text(
        f'<!doctype html><html><head><meta charset="UTF-8"><script src="gsap.min.js"></script><style>html,body{{margin:0;width:{w}px;height:{h}px;overflow:hidden;background:#000}}'
        f'#root{{position:relative;width:{w}px;height:{h}px}}img{{position:absolute;left:0;top:0;width:{w}px;height:{h}px}}</style></head><body>'
        f'<div id="root" data-composition-id="main" data-width="{w}" data-height="{h}" data-duration="1">'
        f'<img class="clip" data-start="0" data-duration="1" src="{src.name}" alt="" data-color-grading="{attr}"></div>'
        f'<script>window.__timelines=window.__timelines||{{}};window.__timelines["main"]=gsap.timeline({{paused:true}});</script>'
        f'</body></html>')
    subprocess.run(CLI + ["snapshot", str(d), "--at", "0.5", "--no-end", "--describe", "false", "--timeout", "60000", "-o", str(d / "snap")],
                   check=True, capture_output=True, text=True)
    shot = next((d / "snap").glob("frame-*.png"))
    shutil.copy(shot, d / "graded.png")
    shutil.copy(shot, dest)


def bake(job, grades):
    photo, grade = job
    payload = grades[grade]
    full, plate = OUT / f".{photo}.{grade}.full.png", OUT / f".{photo}.{grade}.plate.png"
    snap(PHOTOS / f"{photo}.jpg", payload, full)
    snap(PHOTOS / f"{photo}-bg.jpg", payload, plate)
    py = str(Path(sys.executable))
    subprocess.run([py, "-c", CUT, str(full), str(plate), str(PHOTOS / f"{photo}-fg.png"),
                    str(OUT / f"{photo}.{grade}-bg.jpg"), str(OUT / f"{photo}.{grade}-fg.png")], check=True)
    full.unlink(); plate.unlink()
    print("baked", photo, grade, flush=True)


CUT = r"""
import sys, cv2, numpy as np
full, plate, fgsrc, out_bg, out_fg = sys.argv[1:]
g = cv2.imread(full); p = cv2.imread(plate); a = cv2.imread(fgsrc, cv2.IMREAD_UNCHANGED)[..., 3]
cv2.imwrite(out_bg, p, [cv2.IMWRITE_JPEG_QUALITY, 92])
g[a < 2] = 0
cv2.imwrite(out_fg, np.dstack([g, a]), [cv2.IMWRITE_PNG_COMPRESSION, 9])
"""

if __name__ == "__main__":
    grades = load_grades()
    OUT.mkdir(exist_ok=True)
    with ThreadPoolExecutor(2) as ex:
        list(ex.map(lambda j: bake(j, grades), JOBS))
