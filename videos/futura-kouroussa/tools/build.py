"""Assemble the HyperFrames project: compositions/{h,v}/*.html, captions, index.html (16:9) and vertical.html (9:16).
Sources: scenes/sN.frag.html (layout, shared with the sketches) + scenes/sN.anim.js (motion, global film time).
Usage: python tools/build.py   (from the project root)"""
import json, re
from pathlib import Path
from fragments import expand, ROOT

FILM = 120.0
NOMINAL = [0, 10, 28, 42, 58, 75, 95, 110]  # client timecodes (scene starts)
LEAD = 0.6                                   # scenes overlap 1.2 s for morph handoffs
FORMATS = {"h": (1920, 1080), "v": (1080, 1920)}
VPROJ = ROOT.parent / (ROOT.name + "-9x16")
CSS = (ROOT / "assets/film.css").read_text()
CSS_NO_FONTS = re.sub(r"@font-face\s*\{[^}]*\}\s*", "", CSS)
PARTICLES = (ROOT / "assets/particles.js").read_text()
CAPS = json.loads((ROOT / "assets/captions/captions.json").read_text())

PRELUDE = """const FMT = "%(fmt)s", W = %(W)d, H = %(H)d, T0 = %(T0)s, DUR = %(DUR)s, H_ = FMT === "h";
const root = document.querySelector('[data-composition-id="%(cid)s"]');
const $ = (s) => root.querySelector(s);
const $$ = (s) => Array.from(root.querySelectorAll(s));
const at = (g) => Math.max(0, Math.round((g - T0) * 1000) / 1000);
const pick = (h, v) => (H_ ? h : v);
const tl = gsap.timeline({ paused: true });
function prepDraw(els) {
  (Array.isArray(els) ? els : [els]).forEach((el) => {
    el.setAttribute("pathLength", "1");
    el.style.strokeDasharray = "1 1";
    el.style.strokeDashoffset = "1";
  });
}
function splitText(el, perChar, block) {
  const out = [];
  const walk = (node) => {
    Array.from(node.childNodes).forEach((n) => {
      if (n.nodeType === 3) {
        const frag = document.createDocumentFragment();
        n.textContent.split(/(\\s+)/).forEach((p) => {
          if (!p) return;
          if (/^\\s+$/.test(p)) { frag.appendChild(document.createTextNode(p)); return; }
          const w = document.createElement("span");
          w.style.display = "inline-block"; w.style.whiteSpace = "nowrap";
          if (perChar) {
            Array.from(p).forEach((ch) => {
              const c = document.createElement("span");
              c.textContent = ch;
              if (block) c.style.display = "inline-block";
              w.appendChild(c); out.push(c);
            });
          } else { w.textContent = p; out.push(w); }
          frag.appendChild(w);
        });
        n.replaceWith(frag);
      } else if (n.nodeType === 1) walk(n);
    });
  };
  walk(el);
  return out;
}
const splitWords = (el) => splitText(el, false, true);
const splitChars = (el, block) => splitText(el, true, block);
"""

def slots():
    out = []
    for i, n in enumerate(NOMINAL):
        start = max(0.0, n - LEAD)
        end = FILM if i == len(NOMINAL) - 1 else NOMINAL[i + 1] + LEAD
        out.append((i + 1, round(start, 3), round(end - start, 3)))
    return out

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
    sfx = "" if fmt == "h" else "v"
    proj = ROOT if fmt == "h" else VPROJ
    outdir = proj / "compositions"
    outdir.mkdir(parents=True, exist_ok=True)
    hosts = []
    for n, start, dur in slots():
        cid = f"s{n}{sfx}"
        frag = expand((ROOT / f"scenes/s{n}.frag.html").read_text(), cid)
        frag = frag.replace('<div class="bg"></div>', "").replace('<div class="vignette"></div>', "")
        anim = (ROOT / f"scenes/s{n}.anim.js").read_text()
        script = (PARTICLES if n == 1 else "") + PRELUDE % dict(fmt=fmt, W=W, H=H, T0=start, DUR=dur, cid=cid) + anim
        body = f'<div class="fk {fmt}">\n{frag}\n</div>'
        (outdir / f"s{n}.html").write_text(sub_file(cid, W, H, dur, body, CSS_NO_FONTS, script))
        hosts.append(f'  <div id="el-{cid}" data-composition-id="{cid}" data-composition-src="compositions/s{n}.html" '
                     f'data-start="{start}" data-duration="{dur}" data-track-index="{1 + (n - 1) % 2}" data-width="{W}" data-height="{H}"></div>')
    # captions: one sub-composition spanning the film
    cid = f"captions{sfx}"
    cues, tw = [], []
    for k, c in enumerate(CAPS):
        cues.append(f'<div class="fk-caption cue c{k}"><span>{c["text"]}</span></div>')
        tw.append(f'tl.fromTo($(".c{k}"), {{ opacity: 0, y: 8 }}, {{ opacity: 1, y: 0, duration: 0.18, ease: "power2.out" }}, {c["start"]});')
        tw.append(f'tl.to($(".c{k}"), {{ opacity: 0, duration: 0.18, ease: "power2.in" }}, {max(c["start"] + 0.2, c["end"] - 0.18):.3f});')
    script = PRELUDE % dict(fmt=fmt, W=W, H=H, T0=0, DUR=FILM, cid=cid) + "\n".join(tw)
    body = f'<div class="fk {fmt}">\n' + "\n".join(cues) + "\n</div>"
    (outdir / "captions.html").write_text(sub_file(cid, W, H, FILM, body, CSS_NO_FONTS + "\n.fk-caption { opacity: 0; }", script))
    hosts.append(f'  <div id="el-{cid}" data-composition-id="{cid}" data-composition-src="compositions/captions.html" data-track-kind="captions" '
                 f'data-start="0" data-duration="{FILM}" data-track-index="3" data-width="{W}" data-height="{H}"></div>')
    return hosts

def root_file(fmt, hosts):
    W, H = FORMATS[fmt]
    rid = "main" if fmt == "h" else "vertical"
    return f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>FUTURA-Kouroussa — {"16:9" if fmt == "h" else "9:16"}</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <link rel="stylesheet" href="assets/film.css" />
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: #1A2A3A; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #1A2A3A; }}
      [data-composition-id="{rid}"] > div[data-composition-src] {{ position: absolute; inset: 0; }}
      #bg {{ position: absolute; inset: 0;
        background: radial-gradient(ellipse 80% 75% at 50% 45%, #1F3246 0%, #1A2A3A 55%, #121E2A 100%); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="{rid}" data-width="{W}" data-height="{H}" data-duration="{FILM}">
      <div id="bg" class="clip" data-start="0" data-duration="{FILM}" data-track-index="0"></div>
{chr(10).join(hosts)}
      <audio id="vo" src="assets/audio/vo.wav" data-start="0" data-duration="{FILM}" data-track-index="10" data-volume="1"></audio>
      <audio id="music" src="assets/audio/music.wav" data-start="0" data-duration="{FILM}" data-track-index="11" data-volume="0.8"></audio>
      <audio id="sfx" src="assets/audio/sfx.wav" data-start="0" data-duration="{FILM}" data-track-index="12" data-volume="0.6"></audio>
    </div>
    <script>
      window.__timelines["{rid}"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""

def setup_vertical_project():
    VPROJ.mkdir(exist_ok=True)
    link = VPROJ / "assets"
    if not link.exists():
        link.symlink_to(Path("..") / ROOT.name / "assets")
    for f in ("hyperframes.json",):
        (VPROJ / f).write_text((ROOT / f).read_text())
    pkg = json.loads((ROOT / "package.json").read_text()); pkg["name"] = VPROJ.name
    (VPROJ / "package.json").write_text(json.dumps(pkg, indent=2) + "\n")
    (VPROJ / "meta.json").write_text(json.dumps({"id": VPROJ.name, "name": VPROJ.name}, indent=2) + "\n")
    (VPROJ / "README.md").write_text("Version verticale 9:16 de FUTURA-Kouroussa. Généré par ../futura-kouroussa/tools/build.py ; "
                                     "ne pas éditer à la main. `assets/` pointe vers le projet 16:9.\n")

setup_vertical_project()
for fmt in ("h", "v"):
    hosts = build_format(fmt)
    (ROOT if fmt == "h" else VPROJ).joinpath("index.html").write_text(root_file(fmt, hosts))
print("built:", [s for s in slots()])

# ---------------------------------------------------------------- mix: voiceover carve on the music bed
import subprocess
CARVE = ROOT.parent.parent / ".claude/skills/hyperframes-audio/scripts/carve.mjs"
if CARVE.exists() and (ROOT / "node_modules/@hyperframes/core").exists():
    subprocess.run(["node", str(CARVE), "--comp", "index.html", "--bed", "music", "--voice", "vo", "--strength", "0.5"], cwd=ROOT, check=True,
                   stdout=subprocess.DEVNULL)
    carved = re.search(r'<audio id="music"[^>]*></audio>', (ROOT / "index.html").read_text()).group(0)
    vidx = VPROJ / "index.html"
    vidx.write_text(re.sub(r'<audio id="music"[^>]*></audio>', lambda m: carved, vidx.read_text()))
    print("carve applied to both formats")
else:
    print("WARNING: carve skipped (run `npm i -D @hyperframes/core` in the project)")
