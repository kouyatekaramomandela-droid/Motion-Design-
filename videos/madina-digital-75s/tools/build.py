"""Assemble the MADINA DIGITAL film (75 s) from one scene source, in two canvases.

  16:9 1920x1080   this project              -> exports/madina_digital_16x9.mp4
  9:16 1080x1920   ../madina-digital-75s-9x16 -> exports/madina_digital_9x16.mp4

Sources: scenes/sN.frag.html (layout, .h/.v rules) + scenes/sN.anim.js (motion in global film time via at()),
scenes/bg.* (studio background, particles), audio/mix.wav when it exists.
Screen overlays (typed text, focus rings, cursor, steps, check) are placed in the supplied screen's own pixels and
ride the camera with it. Usage: python3 tools/build.py   (from the project root)
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILM = 75.0
FORMATS = {"h": (1920, 1080), "v": (1080, 1920)}
SCENES = [(1, 0.0, 6.0), (2, 6.0, 12.0), (3, 12.0, 22.0), (4, 22.0, 30.0), (5, 30.0, 57.0), (6, 57.0, 66.0), (7, 66.0, 75.0)]
LEAD = 0.6
PROJ = {"h": ROOT, "v": ROOT.parent / (ROOT.name + "-9x16")}
CSS = (ROOT / "assets/film.css").read_text()
CSS_NO_FONTS = re.sub(r"@font-face\s*\{[^}]*\}\s*", "", CSS)
CROPS = json.loads((ROOT / "assets/prep/crops.json").read_text())

PRELUDE = """const FMT = "%(fmt)s", W = %(W)d, H = %(H)d, T0 = %(T0)s, DUR = %(DUR)s;
const root = document.querySelector('[data-composition-id="%(cid)s"]');
const $ = (s) => root.querySelector(s);
const $$ = (s) => Array.from(root.querySelectorAll(s));
const at = (g) => Math.max(0, Math.round((g - T0) * 1000) / 1000);
const pick = (h, v) => (FMT === "h" ? h : v);
const tl = gsap.timeline({ paused: true });
// camera on a floating window: frame the screen rect [x0,y0,x1,y1] (screen px) inside the canvas box [x,y,w,h]
const WB = 8, WBAR = 34;
function camState(rect, box) {
  const rw = rect[2] - rect[0], rh = rect[3] - rect[1];
  const s = Math.min(box[2] / rw, box[3] / rh);
  return { scale: s, x: box[0] + (box[2] - s * rw) / 2 - s * (WB + rect[0]), y: box[1] + (box[3] - s * rh) / 2 - s * (WBAR + rect[1]) };
}
function camSet(el, rect, box, t) { tl.set(el, { ...camState(rect, box), transformOrigin: "0 0" }, t); }
function camTo(el, rectA, rectB, box, t, dur, ease) {
  tl.fromTo(el, { ...camState(rectA, box), transformOrigin: "0 0" },
    { ...camState(rectB, box), duration: dur, ease: ease || "power2.inOut", transformOrigin: "0 0" }, t);
}
// seek-safe typing: the DOM starts empty, the tween writes the visible prefix (and a caret) on every render
function typeText(el, text, t, dur, keepCaret) {
  el.innerHTML = "";
  const chars = Array.from(text);
  const o = { n: 0 };
  tl.to(o, { n: chars.length, duration: dur, ease: "none", onUpdate: () => {
    const k = Math.round(o.n);
    el.innerHTML = chars.slice(0, k).join("") + (k < chars.length || keepCaret ? '<i class="caret"></i>' : "");
  } }, t);
}
function prepDraw(els) {
  (Array.isArray(els) ? els : [els]).forEach((el) => { el.setAttribute("pathLength", "1"); el.style.strokeDasharray = "1 1"; el.style.strokeDashoffset = "1"; });
}
// seek-safe count-up with a formatter
function countUp(el, from, to, t, dur, fmt) {
  const f = fmt || ((v) => String(v));
  el.textContent = f(from);
  const o = { v: from };
  tl.to(o, { v: to, duration: dur, ease: "power2.out", onUpdate: () => { el.textContent = f(Math.round(o.v)); } }, t);
}
"""


def expand(frag, fmt):
    def crop(m):
        return f"assets/prep/{m.group(1)}.png"
    return re.sub(r"\{\{crop:([\w-]+)\}\}", crop, frag)


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
    outdir = PROJ[fmt] / "compositions"; outdir.mkdir(parents=True, exist_ok=True)
    hosts = []

    def add(name, cid, start, dur, frag, anim, track):
        script = PRELUDE % dict(fmt=fmt, W=W, H=H, T0=start, DUR=dur, cid=cid) + anim
        body = f'<div class="md {fmt}">\n{frag}\n</div>'
        (outdir / f"{name}.html").write_text(sub_file(cid, W, H, dur, body, CSS_NO_FONTS, script))
        hosts.append(f'      <div id="el-{cid}" data-composition-id="{cid}" data-composition-src="compositions/{name}.html" '
                     f'data-start="{start}" data-duration="{dur}" data-track-index="{track}" data-width="{W}" data-height="{H}"></div>')

    add("bg", f"bg{sfx}", 0, FILM, expand((ROOT / "scenes/bg.frag.html").read_text(), fmt), (ROOT / "scenes/bg.anim.js").read_text(), 0)
    for n, a, b in SCENES:
        if not (ROOT / f"scenes/s{n}.frag.html").exists():
            continue
        start = max(0.0, a - LEAD); end = min(FILM, b + LEAD); dur = round(end - start, 3)
        frag = expand((ROOT / f"scenes/s{n}.frag.html").read_text(), fmt)
        add(f"s{n}", f"s{n}{sfx}", start, dur, frag, (ROOT / f"scenes/s{n}.anim.js").read_text(), 1 + (n - 1) % 2)
    return hosts


def root_file(fmt, hosts):
    W, H = FORMATS[fmt]
    rid = {"h": "main", "v": "vertical"}[fmt]
    audio = (f'      <audio id="mix" src="audio/mix.wav" data-start="0" data-duration="{FILM}" data-track-index="10" data-volume="1"></audio>\n'
             if (ROOT / "audio/mix.wav").exists() else "")
    return f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>MADINA DIGITAL — film 75 s ({"16:9" if fmt == "h" else "9:16"})</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <link rel="stylesheet" href="assets/film.css" />
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: #0A1A4A; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #0A1A4A; }}
      [data-composition-id="{rid}"] > div[data-composition-src] {{ position: absolute; inset: 0; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="{rid}" data-width="{W}" data-height="{H}" data-duration="{FILM}">
{chr(10).join(hosts)}
{audio}    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["{rid}"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""


def setup_sibling(fmt):
    proj = PROJ[fmt]; proj.mkdir(exist_ok=True)
    for d in ("assets", "audio"):
        link = proj / d
        if not link.exists():
            link.symlink_to(Path("..") / ROOT.name / d)
    (proj / "hyperframes.json").write_text((ROOT / "hyperframes.json").read_text())
    pkg = json.loads((ROOT / "package.json").read_text()); pkg["name"] = proj.name
    (proj / "package.json").write_text(json.dumps(pkg, indent=2) + "\n")
    (proj / "meta.json").write_text(json.dumps({"id": proj.name, "name": proj.name}, indent=2) + "\n")
    (proj / ".gitignore").write_text("renders/\n.hyperframes/\n")
    (proj / "README.md").write_text(f"Version 9:16 du film MADINA DIGITAL (75 s). Généré par ../{ROOT.name}/tools/build.py ; "
                                    "ne pas éditer à la main. `assets/` et `audio/` pointent vers le projet 16:9.\n")


if __name__ == "__main__":
    for fmt in ("h", "v"):
        if fmt != "h":
            setup_sibling(fmt)
        PROJ[fmt].joinpath("index.html").write_text(root_file(fmt, build_format(fmt)))
    print("built", [(n, max(0.0, a - LEAD), min(FILM, b + LEAD)) for n, a, b in SCENES])
