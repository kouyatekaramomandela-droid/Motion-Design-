"""Assemble the three HyperFrames projects of the 60 s film from one source.

  16:9 1920x1080  this project            (index.html, compositions/)
  9:16 1080x1920  ../<name>-9x16          (generated; assets/ links back here)
  1:1  1080x1080  ../<name>-1x1           (generated; assets/ links back here)

Sources: scenes/fN.frag.html (layout, .h/.v/.s rules) + scenes/fN.anim.js (motion, global film time via at()).
Photo grades: tools/grades.json, validated by `hyperframes media-treatment` (tools/grades.lock.json) and baked
into the plate images by tools/bake_grades.py (HyperFrames' own shader, one still per photo and grade).
Usage: python tools/build.py   (from the project root)
"""
import json, re, subprocess
from pathlib import Path
from fragments import expand, ROOT, FORMATS

FILM = 60.0
NOMINAL = [0, 5, 15, 28, 38, 52]   # client timecodes (scene starts)
LEAD = 0.6                         # scenes overlap 1.2 s for the gold-line handoffs
PROJ = {"h": ROOT, "v": ROOT.parent / (ROOT.name + "-9x16"), "s": ROOT.parent / (ROOT.name + "-1x1")}
LABEL = {"h": "16:9", "v": "9:16", "s": "1:1"}
CSS = (ROOT / "assets/film.css").read_text()
CSS_NO_FONTS = re.sub(r"@font-face\s*\{[^}]*\}\s*", "", CSS)
PARTICLES = (ROOT / "assets/particles.js").read_text()
CAPS = json.loads((ROOT / "assets/captions/captions.json").read_text())
CLI = ["npx", "--yes", "hyperframes@0.8.141"]

PRELUDE = """const FMT = "%(fmt)s", W = %(W)d, H = %(H)d, T0 = %(T0)s, DUR = %(DUR)s;
const root = document.querySelector('[data-composition-id="%(cid)s"]');
const $ = (s) => root.querySelector(s);
const $$ = (s) => Array.from(root.querySelectorAll(s));
const at = (g) => Math.max(0, Math.round((g - T0) * 1000) / 1000);
const pick = (h, v, s) => (FMT === "h" ? h : FMT === "v" ? v : s === undefined ? v : s);
const tl = gsap.timeline({ paused: true });
function prepDraw(els) {
  (Array.isArray(els) ? els : [els]).forEach((el) => {
    el.setAttribute("pathLength", "1");
    el.style.strokeDasharray = "1 1";
    el.style.strokeDashoffset = "1";
  });
}
function splitWords(el) {
  const out = [];
  const walk = (node) => {
    Array.from(node.childNodes).forEach((n) => {
      if (n.nodeType === 3) {
        const frag = document.createDocumentFragment();
        n.textContent.split(/(\\s+)/).forEach((p) => {
          if (!p) return;
          if (/^\\s+$/.test(p)) { frag.appendChild(document.createTextNode(p)); return; }
          const w = document.createElement("span");
          w.style.display = "inline-block"; w.style.whiteSpace = "nowrap"; w.textContent = p;
          frag.appendChild(w); out.push(w);
        });
        n.replaceWith(frag);
      } else if (n.nodeType === 1) walk(n);
    });
  };
  walk(el);
  return out;
}
// 2.5D camera on a photo plate: background and nearest plane scale/drift at different rates
// around the plate's focus point. a/b = [scale, x, y] at start/end for the background; the
// nearest plane gets the same move amplified by k (depth).
function camera(plate, t0, dur, a, b, k, ease) {
  const ox = plate.dataset.ox + "px " + plate.dataset.oy + "px";
  const bg = plate.querySelector(".pl-bg"), fg = plate.querySelector(".pl-fg");
  const fs = (s) => 1 + (s - 1) * k;
  tl.fromTo(bg, { scale: a[0], x: a[1], y: a[2], transformOrigin: ox },
    { scale: b[0], x: b[1], y: b[2], duration: dur, ease: ease || "none", transformOrigin: ox }, t0);
  tl.fromTo(fg, { scale: fs(a[0]), x: a[1] * k, y: a[2] * k, transformOrigin: ox },
    { scale: fs(b[0]), x: b[1] * k, y: b[2] * k, duration: dur, ease: ease || "none", transformOrigin: ox }, t0);
}
"""


def slots():
    out = []
    for i, n in enumerate(NOMINAL):
        start = max(0.0, n - LEAD)
        end = FILM if i == len(NOMINAL) - 1 else NOMINAL[i + 1] + LEAD
        out.append((i + 1, round(start, 3), round(end - start, 3)))
    return out


def load_grades():
    """Canonical grade payloads: validated/expanded by the HyperFrames CLI, cached by patch. Returns them."""
    patches = json.loads((ROOT / "tools/grades.json").read_text())
    lock_path = ROOT / "tools/grades.lock.json"
    lock = json.loads(lock_path.read_text()) if lock_path.exists() else {}
    probe = ROOT / ".hyperframes/grade-probe.html"
    for name, patch in patches.items():
        if name in lock and lock[name]["patch"] == patch:
            continue
        probe.parent.mkdir(exist_ok=True)
        probe.write_text('<!doctype html><html><body><div data-composition-id="probe" data-width="16" '
                         'data-height="16" data-duration="1"><img id="probe" src="probe.jpg" alt=""></div></body></html>')
        res = subprocess.run(CLI + ["media-treatment", "--file", str(probe.relative_to(ROOT)), "--selector", "#probe",
                                    "--grading", json.dumps(patch), "--apply", "--json"],
                             cwd=ROOT, check=True, capture_output=True, text=True)
        out = json.loads(res.stdout)
        if not out.get("ok"):
            raise SystemExit(f"grade {name}: {res.stdout}")
        lock[name] = {"patch": patch, "canonical": out["after"]}
        print("grade validated:", name)
    lock_path.write_text(json.dumps(lock, indent=1) + "\n")
    return {k: v["canonical"] for k, v in lock.items() if k in patches}


def sub_file(cid, W, H, dur, body_html, style, script):
    return f"""<!doctype html>
<html lang="fr">
<head><meta charset="utf-8"></head>
<body>
<template id="{cid}">
<style>
{style}
#{cid}-root {{ position: absolute; inset: 0; overflow: hidden; }}
</style>
<div id="{cid}-root" data-composition-id="{cid}" data-width="{W}" data-height="{H}" data-duration="{dur}">
{body_html}
</div>
<script>
(function () {{
{script}
window.__timelines["{cid}"] = tl;
}})();
</script>
</template>
</body>
</html>
"""


def build_format(fmt):
    W, H = FORMATS[fmt]
    sfx = "" if fmt == "h" else fmt
    outdir = PROJ[fmt] / "compositions"
    outdir.mkdir(parents=True, exist_ok=True)
    hosts = []
    for n, start, dur in slots():
        if not (ROOT / f"scenes/f{n}.frag.html").exists():
            continue  # scene not written yet
        cid = f"f{n}{sfx}"
        frag = expand((ROOT / f"scenes/f{n}.frag.html").read_text(), cid, fmt)
        anim = (ROOT / f"scenes/f{n}.anim.js").read_text()
        script = PARTICLES + PRELUDE % dict(fmt=fmt, W=W, H=H, T0=start, DUR=dur, cid=cid) + anim
        body = f'<div class="fk {fmt}">\n{frag}\n</div>'
        (outdir / f"f{n}.html").write_text(sub_file(cid, W, H, dur, body, CSS_NO_FONTS, script))
        hosts.append(f'      <div id="el-{cid}" data-composition-id="{cid}" data-composition-src="compositions/f{n}.html" '
                     f'data-start="{start}" data-duration="{dur}" data-track-index="{1 + (n - 1) % 2}" data-width="{W}" data-height="{H}"></div>')
    cid = f"captions{sfx}"
    cues, tw = [], []
    for k, c in enumerate(CAPS):
        cues.append(f'<div class="fk-caption cue c{k}"><span>{c["text"]}</span></div>')
        tw.append(f'tl.fromTo($(".c{k}"), {{ opacity: 0, y: 8 }}, {{ opacity: 1, y: 0, duration: 0.18, ease: "power2.out" }}, {c["start"]});')
        tw.append(f'tl.to($(".c{k}"), {{ opacity: 0, duration: 0.18, ease: "power2.in" }}, {max(c["start"] + 0.2, c["end"] - 0.18):.3f});')
    script = PRELUDE % dict(fmt=fmt, W=W, H=H, T0=0, DUR=FILM, cid=cid) + "\n".join(tw)
    body = f'<div class="fk {fmt}">\n' + "\n".join(cues) + "\n</div>"
    (outdir / "captions.html").write_text(sub_file(cid, W, H, FILM, body, CSS_NO_FONTS + "\n.fk-caption { opacity: 0; }", script))
    hosts.append(f'      <div id="el-{cid}" data-composition-id="{cid}" data-composition-src="compositions/captions.html" data-track-kind="captions" '
                 f'data-start="0" data-duration="{FILM}" data-track-index="3" data-width="{W}" data-height="{H}"></div>')
    return hosts


def root_file(fmt, hosts):
    W, H = FORMATS[fmt]
    rid = {"h": "main", "v": "vertical", "s": "square"}[fmt]
    return f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>FUTURA-Kouroussa 60 s — {LABEL[fmt]}</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <link rel="stylesheet" href="assets/film.css" />
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: #070C12; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #070C12; }}
      [data-composition-id="{rid}"] > div[data-composition-src] {{ position: absolute; inset: 0; }}
      #bg {{ position: absolute; inset: 0; background: #070C12; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="{rid}" data-width="{W}" data-height="{H}" data-duration="{FILM}">
      <div id="bg" class="clip" data-start="0" data-duration="{FILM}" data-track-index="0"></div>
{chr(10).join(hosts)}
      <audio id="vo" src="assets/audio/vo.wav" data-start="0" data-duration="{FILM}" data-track-index="10" data-volume="1"></audio>
      <audio id="music" src="assets/audio/music.wav" data-start="0" data-duration="{FILM}" data-track-index="11" data-volume="0.72"></audio>
      <audio id="sfx" src="assets/audio/sfx.wav" data-start="0" data-duration="{FILM}" data-track-index="12" data-volume="0.55"></audio>
    </div>
    <script>
      window.__timelines["{rid}"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""


def setup_sibling(fmt):
    proj = PROJ[fmt]
    proj.mkdir(exist_ok=True)
    link = proj / "assets"
    if not link.exists():
        link.symlink_to(Path("..") / ROOT.name / "assets")
    (proj / "hyperframes.json").write_text((ROOT / "hyperframes.json").read_text())
    pkg = json.loads((ROOT / "package.json").read_text()); pkg["name"] = proj.name
    (proj / "package.json").write_text(json.dumps(pkg, indent=2) + "\n")
    (proj / "meta.json").write_text(json.dumps({"id": proj.name, "name": proj.name}, indent=2) + "\n")
    (proj / ".gitignore").write_text("renders/\n.hyperframes/\n")
    (proj / "README.md").write_text(f"Version {LABEL[fmt]} du film 60 s FUTURA-Kouroussa. Généré par ../{ROOT.name}/tools/build.py ; "
                                    f"ne pas éditer à la main. `assets/` pointe vers le projet 16:9.\n")


if __name__ == "__main__":
    for fmt in ("h", "v", "s"):
        if fmt != "h":
            setup_sibling(fmt)
        PROJ[fmt].joinpath("index.html").write_text(root_file(fmt, build_format(fmt)))
    print("built:", slots())
