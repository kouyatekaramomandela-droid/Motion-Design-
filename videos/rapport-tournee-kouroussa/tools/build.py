"""Assemble the three HyperFrames projects of the 75 s report film from one scene source.

  16:9 1920x1080             this project                  -> exports/rapport_tournee_16x9.mp4
  9:16 1080x1920 (recomposé) ../<name>-9x16                -> exports/rapport_tournee_9x16.mp4
  16:9 sans texte            ../<name>-sans-texte          -> exports/rapport_tournee_sans_texte.mp4

Sources: scenes/sN.frag.html (layout, .h/.v rules) + scenes/sN.anim.js (motion, global film time via at()),
scenes/chrome.* (fixed logos + final fade to white), assets/captions/captions.json (burned-in subtitles,
from tools/build_vo.py), audio/mix.wav (tools/mix_audio.sh). Generated projects link assets/ and audio/ back here.
Usage: python3 tools/build.py   (from the project root)
"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fragments import expand, ROOT, FORMATS

FILM = 75.0
SCENES = [(1, 0, 6), (2, 6, 18), (3, 18, 28), (4, 28, 52), (5, 52, 66), (6, 66, 75)]  # client timecodes
LEAD = 0.6   # each scene composition opens 0.6 s early and closes 0.6 s late, for the crossfades
VARIANTS = {"h": ("h", ROOT, True), "v": ("v", ROOT.parent / (ROOT.name + "-9x16"), True),
            "nt": ("h", ROOT.parent / (ROOT.name + "-sans-texte"), False)}
LABEL = {"h": "16:9", "v": "9:16", "nt": "16:9 sans texte"}
CSS = (ROOT / "assets/film.css").read_text()
CSS_NO_FONTS = re.sub(r"@font-face\s*\{[^}]*\}\s*", "", CSS)
CAPS = json.loads((ROOT / "assets/captions/captions.json").read_text())

PRELUDE = """const FMT = "%(fmt)s", W = %(W)d, H = %(H)d, T0 = %(T0)s, DUR = %(DUR)s;
const root = document.querySelector('[data-composition-id="%(cid)s"]');
const $ = (s) => root.querySelector(s);
const $$ = (s) => Array.from(root.querySelectorAll(s));
const at = (g) => Math.max(0, Math.round((g - T0) * 1000) / 1000);
const pick = (h, v) => (FMT === "h" ? h : v);
const tl = gsap.timeline({ paused: true });
function prepDraw(els) {
  (Array.isArray(els) ? els : [els]).forEach((el) => {
    el.setAttribute("pathLength", "1");
    el.style.strokeDasharray = "1 1";
    el.style.strokeDashoffset = "1";
  });
}
// seek-safe count-up: the DOM starts at `from`; the tween writes the rounded value on every render.
// unit = [labelEl, singular, plural]: the label agrees with the number (singular for 0 and 1).
function countUp(el, from, to, t, dur, ease, unit) {
  const show = (v) => {
    el.textContent = String(v);
    if (unit) unit[0].textContent = v <= 1 ? unit[1] : unit[2];
  };
  show(from);
  const o = { v: from };
  tl.to(o, { v: to, duration: dur, ease: ease || "power1.out", onUpdate: () => show(Math.round(o.v)) }, t);
}
// count of items revealed every `step` seconds from t0 (the first one at t0): 0 before t0, then 1, 2, … n
function stepCount(el, n, t0, step, unit) {
  const show = (v) => {
    el.textContent = String(v);
    if (unit) unit[0].textContent = v <= 1 ? unit[1] : unit[2];
  };
  show(0);
  const o = { v: 0 };
  tl.to(o, { v: n, duration: n * step, ease: "none", onUpdate: () => show(o.v <= 0 ? 0 : Math.min(n, Math.floor(o.v + 1e-6) + 1)) }, t0);
}
"""


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


def build_variant(var):
    fmt, proj, captions = VARIANTS[var]
    W, H = FORMATS[fmt]
    cls = f"rk {fmt}" + (" nt" if var == "nt" else "")
    sfx = {"h": "", "v": "v", "nt": "nt"}[var]
    outdir = proj / "compositions"; outdir.mkdir(parents=True, exist_ok=True)
    hosts = []

    def add(name, cid, start, dur, frag, anim, track):
        script = PRELUDE % dict(fmt=fmt, W=W, H=H, T0=start, DUR=dur, cid=cid) + anim
        body = f'<div class="{cls}">\n{frag}\n</div>'
        (outdir / f"{name}.html").write_text(sub_file(cid, W, H, dur, body, CSS_NO_FONTS, script))
        hosts.append(f'      <div id="el-{cid}" data-composition-id="{cid}" data-composition-src="compositions/{name}.html" '
                     f'data-start="{start}" data-duration="{dur}" data-track-index="{track}" data-width="{W}" data-height="{H}"></div>')

    for n, a, b in SCENES:
        start = max(0.0, a - LEAD); end = min(FILM, b + LEAD); dur = round(end - start, 3)
        frag = expand((ROOT / f"scenes/s{n}.frag.html").read_text(), f"s{n}{sfx}", fmt, start)
        add(f"s{n}", f"s{n}{sfx}", start, dur, frag, (ROOT / f"scenes/s{n}.anim.js").read_text(), 1 + (n - 1) % 2)
    if captions:
        cues, tw = [], []
        for k, c in enumerate(CAPS):
            cues.append(f'<div class="rk-caption cue c{k}"><span>{c["text"]}</span></div>')
            tw.append(f'tl.fromTo($(".c{k}"), {{ opacity: 0, y: 8 }}, {{ opacity: 1, y: 0, duration: 0.18, ease: "power2.out" }}, {c["start"]});')
            tw.append(f'tl.to($(".c{k}"), {{ opacity: 0, duration: 0.18, ease: "power2.in" }}, {max(c["start"] + 0.2, c["end"] - 0.18):.3f});')
        script = PRELUDE % dict(fmt=fmt, W=W, H=H, T0=0, DUR=FILM, cid=f"captions{sfx}") + "\n".join(tw)
        body = f'<div class="{cls}">\n' + "\n".join(cues) + "\n</div>"
        (outdir / "captions.html").write_text(sub_file(f"captions{sfx}", W, H, FILM, body, CSS_NO_FONTS + "\n.rk-caption { opacity: 0; }", script))
        hosts.append(f'      <div id="el-captions{sfx}" data-composition-id="captions{sfx}" data-composition-src="compositions/captions.html" '
                     f'data-track-kind="captions" data-start="0" data-duration="{FILM}" data-track-index="3" data-width="{W}" data-height="{H}"></div>')
    add("chrome", f"chrome{sfx}", 0, FILM, expand("{{chrome}}", "chrome", fmt), (ROOT / "scenes/chrome.anim.js").read_text(), 4)
    return hosts


def root_file(var, hosts):
    fmt = VARIANTS[var][0]; W, H = FORMATS[fmt]
    rid = {"h": "main", "v": "vertical", "nt": "textless"}[var]
    return f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>Rapport de la tournée des Députés — {LABEL[var]}</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <link rel="stylesheet" href="assets/film.css" />
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: #F6F2E9; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #F6F2E9; }}
      [data-composition-id="{rid}"] > div[data-composition-src] {{ position: absolute; inset: 0; }}
      #bg {{ position: absolute; inset: 0; background: #F6F2E9; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="{rid}" data-width="{W}" data-height="{H}" data-duration="{FILM}">
      <div id="bg" class="clip" data-start="0" data-duration="{FILM}" data-track-index="0"></div>
{chr(10).join(hosts)}
      <audio id="mix" src="audio/mix.wav" data-start="0" data-duration="{FILM}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["{rid}"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""


def setup_sibling(var):
    proj = VARIANTS[var][1]
    proj.mkdir(exist_ok=True)
    for d in ("assets", "audio"):
        link = proj / d
        if not link.exists():
            link.symlink_to(Path("..") / ROOT.name / d)
    (proj / "hyperframes.json").write_text((ROOT / "hyperframes.json").read_text())
    pkg = json.loads((ROOT / "package.json").read_text()); pkg["name"] = proj.name
    (proj / "package.json").write_text(json.dumps(pkg, indent=2) + "\n")
    (proj / "meta.json").write_text(json.dumps({"id": proj.name, "name": proj.name}, indent=2) + "\n")
    (proj / ".gitignore").write_text("renders/\n.hyperframes/\n")
    (proj / "README.md").write_text(f"Version {LABEL[var]} du film « Rapport de la tournée des Députés » (75 s). Généré par "
                                    f"../{ROOT.name}/tools/build.py ; ne pas éditer à la main. `assets/` et `audio/` pointent vers le projet 16:9.\n")


if __name__ == "__main__":
    for var in ("h", "v", "nt"):
        if var != "h":
            setup_sibling(var)
        VARIANTS[var][1].joinpath("index.html").write_text(root_file(var, build_variant(var)))
    print("built", [(n, max(0.0, a - LEAD), min(FILM, b + LEAD)) for n, a, b in SCENES])
