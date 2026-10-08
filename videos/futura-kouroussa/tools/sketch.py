"""Write static sketch pages (16:9 + 9:16) for every storyboard cell, screenshot them, build storyboard.html.
Usage: python tools/sketch.py  (from the project root; needs Playwright via node)"""
import json, subprocess, html
from pathlib import Path
from fragments import expand, ROOT

OUT = ROOT / "sketches"
PNG = OUT / "png"
OUT.mkdir(exist_ok=True); PNG.mkdir(exist_ok=True)
CAPS = json.loads((ROOT / "assets/captions/captions.json").read_text())
VERSION = "v2"

CELLS = [
    dict(id="01", name="L’accroche", scene="s1", t=7.0, span="0:00–0:10",
         note="<b>D’abord :</b> une seule étincelle d’or au centre (0,8 s), puis des milliers en spirale ; le compteur monte jusqu’à 2,35 et tient 3,8 s.",
         seam="morphing → les particules se rangent en trait doré"),
    dict(id="02a", name="Le territoire · carte", scene="s2", phase="map", t=15.5, span="0:10–0:17",
         note="<b>D’abord :</b> le trait doré dessine le contour de la préfecture et le Niger ; les trois mines s’allument une à une (tintements à 14,0 / 14,7 / 15,4 s).",
         seam="plongée caméra vers le terrain"),
    dict(id="02b", name="Le territoire · le manque", scene="s2", phase="tri", t=21.0, span="0:17–0:28",
         note="<b>D’abord :</b> les trois vignettes se dessinent au trait gris, sans or, sur « l’eau potable », « des écoles », « des centres de santé ».",
         seam="la carte revient, les mines émettent des lignes"),
    dict(id="03", name="Le fil perdu", scene="s3", t=36.5, span="0:28–0:42",
         note="<b>D’abord :</b> les lignes d’or quittent les mines et s’effacent vers l’horizon ; le point d’interrogation se forme dans le vide. Plan fixe 38,5–41,5 s.",
         seam="une page glisse et recouvre le vide"),
    dict(id="04", name="Le socle légal", scene="s4", t=50.5, span="0:42–0:58",
         note="<b>D’abord :</b> le livre s’ouvre en 3D ; l’Article 130 s’illumine (« 1 % » lisible 8 s), puis l’Article 165 ; les lignes reviennent et convergent au centre.",
         seam="tout converge en un point lumineux"),
    dict(id="05", name="La naissance", scene="s5", t=70.0, span="0:58–1:15",
         note="<b>D’abord :</b> le point éclate ; la pépite se pose, la main se dessine dessous, les cinq rayons jaillissent ; le nom s’écrit lettre par lettre ; badges sur « OHADA » et « mission parlementaire ».",
         seam="le halo de la pépite devient l’anneau"),
    dict(id="06a", name="Gouvernance · collèges", scene="s6", phase="col", t=79.5, span="1:15–1:21",
         note="<b>D’abord :</b> l’anneau se divise en quatre arcs proportionnels ; la légende arrive ligne par ligne ; l’arc 40 % s’illumine sur « la majorité ».",
         seam="la légende bascule, les cercles de contrôle s’allument"),
    dict(id="06b", name="Gouvernance · contrôles", scene="s6", phase="ctl", t=91.0, span="1:21–1:35",
         note="<b>D’abord :</b> trois cercles s’allument sur « encadrée », « auditée », « publique » ; un jeton d’or franchit trois paliers « Validé » (88,6 / 90,1 / 91,6 s). Apogée musicale.",
         seam="le jeton retombe sur le territoire"),
    dict(id="07", name="Les résultats", scene="s7", t=106.0, span="1:35–1:50",
         note="<b>D’abord :</b> le triptyque revient aux places de la scène 2 et s’allume en or sur « l’eau », « les écoles », « les soins » ; puis il monte, le tableau de bord glisse dessous (tendances, aucune valeur).",
         seam="les courbes s’aplanissent en ondes"),
    dict(id="08", name="La signature", scene="s8", t=117.0, span="1:50–2:00",
         note="<b>D’abord :</b> les ondes d’or se posent en bande rouge-jaune-vert ; le logo se reforme, centré ; la signature arrive à 113,9 s et tient jusqu’à 120 s.",
         seam="fin — tenue sur le logo"),
]

PHASE_CSS = {
    ("s2", "map"): ".s2-tri{display:none!important}",
    ("s2", "tri"): ".s2-mapgroup{display:none!important}",
    ("s6", "col"): ".s6 .controls,.s6 .ctl-rings,.s6 .gates,.s6 .token,.s6 .token-path{display:none!important}",
    ("s6", "ctl"): ".s6 .colleges,.s6 .ctl-rings .ctl,.s6 .token{display:none!important}",
}

def caption_at(t):
    for c in CAPS:
        if c["start"] <= t <= c["end"]: return c["text"]
    return None

def page(cell, fmt):
    W, H = (1920, 1080) if fmt == "h" else (1080, 1920)
    frag = expand((ROOT / f"scenes/{cell['scene']}.frag.html").read_text(), f"{cell['scene']}{cell.get('phase','')}{fmt}")
    cap = caption_at(cell["t"])
    cap_html = f'<div class="fk-caption"><span>{html.escape(cap)}</span></div>' if cap else ""
    phase_css = PHASE_CSS.get((cell["scene"], cell.get("phase")), "")
    script = ""
    if cell["scene"] == "s1":
        script = f"""<script>
var c=document.querySelector('canvas.s1-particles');c.width={W};c.height={H};
var f=FK.makeField(2600,11);
FK.drawGenesis(c.getContext('2d'),f,{cell['t']},{{cx:{W/2},cy:{H*0.43 if fmt=='h' else H*0.41},maxR:{620 if fmt=='h' else 520},line:{{x0:230,x1:930,y:540}}}});
</script>"""
    doc = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<link rel="stylesheet" href="../assets/film.css">
<style>html,body{{margin:0;background:#0F1A25}} .frame{{width:{W}px;height:{H}px}} {phase_css}</style>
<script src="../assets/particles.js"></script></head>
<body><div class="frame fk {fmt}">{frag}{cap_html}</div>{script}</body></html>"""
    name = f"{cell['id']}-{fmt}"
    (OUT / f"{name}.html").write_text(doc)
    return name, W, H

jobs = []
for cell in CELLS:
    for fmt in ("h", "v"):
        name, W, H = page(cell, fmt)
        jobs.append({"html": str(OUT / f"{name}.html"), "png": str(PNG / f"{name}.jpg"), "w": W, "h": H})
(OUT / "jobs.json").write_text(json.dumps(jobs))
subprocess.run(["node", str(ROOT / "tools/shoot.cjs"), str(OUT / "jobs.json")], check=True)

# ------------------------------------------------------------- storyboard.html
def cell_h(c):
    return f"""<figure class="cell" id="frame-{c['id']}">
  <img src="sketches/png/{c['id']}-h.jpg" alt="Scène {c['id']} — {html.escape(c['name'])}">
  <figcaption><div class="lab"><b>{c['id']} · {html.escape(c['name']).upper()}</b><span>{c['scene']} · {c['span']}</span></div>
  <p>{c['note']}</p><span class="chip">→ {html.escape(c['seam'])}</span></figcaption></figure>"""

def cell_v(c):
    return f"""<figure class="cell v" id="frame-{c['id']}-v"><img src="sketches/png/{c['id']}-v.jpg" alt="Scène {c['id']} vertical">
  <figcaption><div class="lab"><b>{c['id']}</b><span>{c['span']}</span></div></figcaption></figure>"""

seams = "".join(f'<li><b>{c["id"]}</b> {html.escape(c["seam"])}</li>' for c in CELLS)
sheet = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>FUTURA-Kouroussa — storyboard {VERSION}</title>
<style>
@font-face{{font-family:"Playfair Display";font-weight:700;src:url("assets/fonts/playfair-display-latin-700-normal.woff2")}}
@font-face{{font-family:"Montserrat";font-weight:400;src:url("assets/fonts/montserrat-latin-400-normal.woff2")}}
@font-face{{font-family:"Montserrat";font-weight:700;src:url("assets/fonts/montserrat-latin-700-normal.woff2")}}
:root{{--night:#1A2A3A;--deep:#0F1A25;--raised:#22364A;--gold:#F5C518;--gold-deep:#B8860B;--ivory:#F3EEE3;--dim:#A9B3BC}}
body{{margin:0;background:var(--deep);color:var(--ivory);font-family:Montserrat,sans-serif}}
header{{padding:40px 48px 8px;display:flex;flex-wrap:wrap;align-items:baseline;gap:18px 28px}}
h1{{margin:0;font-family:"Playfair Display",serif;font-size:44px;letter-spacing:-.01em}}
h1 small{{font-family:Montserrat;font-size:16px;font-weight:700;color:var(--gold);letter-spacing:.14em;margin-left:10px}}
.dek{{color:var(--dim);font-size:17px;max-width:760px;line-height:1.5}}
.tag{{margin-left:auto;font-size:13px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--deep);background:var(--gold);padding:8px 14px;border-radius:999px}}
h2{{margin:34px 48px 14px;font-size:14px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold)}}
.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:26px;padding:0 48px}}
.grid.v{{grid-template-columns:repeat(5,minmax(0,1fr))}}
@media (max-width:1100px){{.grid{{grid-template-columns:1fr}} .grid.v{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
.cell{{margin:0;background:var(--raised);border-radius:14px;overflow:hidden;border:1px solid rgba(184,134,11,.35)}}
.cell img{{display:block;width:100%;aspect-ratio:16/9;object-fit:cover;background:var(--night)}}
.cell.v img{{aspect-ratio:9/16}}
figcaption{{padding:14px 18px 18px}}
.lab{{display:flex;justify-content:space-between;gap:12px;font-size:13px;letter-spacing:.08em}}
.lab b{{color:var(--gold)}} .lab span{{color:var(--dim)}}
figcaption p{{margin:10px 0 12px;font-size:14.5px;line-height:1.5;color:#DCD7CC}}
figcaption p b{{color:var(--ivory)}}
.chip{{display:inline-block;font-size:12px;font-weight:700;letter-spacing:.06em;color:var(--gold);border:1.5px solid var(--gold-deep);border-radius:999px;padding:5px 11px}}
.panel{{background:var(--raised);border-radius:14px;padding:22px 24px;border:1px solid rgba(184,134,11,.35);font-size:14.5px;line-height:1.55}}
.panel h3{{margin:0 0 10px;font-family:"Playfair Display",serif;font-size:24px}}
.panel ol{{margin:0;padding-left:0;list-style:none}} .panel li{{margin:6px 0}} .panel li b{{color:var(--gold);margin-right:8px}}
.sw{{display:inline-flex;align-items:center;gap:8px;margin:4px 14px 4px 0}} .sw i{{width:22px;height:22px;border-radius:6px;display:inline-block;border:1px solid rgba(255,255,255,.2)}}
footer{{padding:30px 48px 60px;color:var(--dim);font-size:13px}}
</style></head><body>
<header><h1>FUTURA-Kouroussa — storyboard<small>{VERSION}</small></h1>
<span class="tag">1920×1080 + 1080×1920 · 30 fps · 120 s · 8 scènes</span>
<p class="dek">« L’or de Kouroussa doit servir Kouroussa. » Images fixes au moment clé de chaque scène, avec les vraies polices, couleurs, textes, sous-titres et le logo du client. Le mouvement arrive à l’étape suivante.</p></header>
<h2>Master 16:9</h2>
<div class="grid">{''.join(cell_h(c) for c in CELLS)}
<div class="panel"><h3>Carte des transitions</h3><ol>{seams}</ol><p style="color:var(--dim);margin:12px 0 0">Aucune coupe sèche : chaque passage est un morphing du fil d’or.</p></div>
<div class="panel"><h3>Charte</h3>
<div><span class="sw"><i style="background:#1A2A3A"></i>#1A2A3A</span><span class="sw"><i style="background:#B8860B"></i>#B8860B</span><span class="sw"><i style="background:#F5C518"></i>#F5C518</span><span class="sw"><i style="background:#F3EEE3"></i>#F3EEE3</span><span class="sw"><i style="background:#CE1126"></i>#CE1126 (fin)</span><span class="sw"><i style="background:#009A44"></i>#009A44 (fin)</span></div>
<p>Titres : Playfair Display 700/900 · Textes et sous-titres : Montserrat 400/700 · Logo : Roboto (fidèle au logo fourni).</p>
<p style="color:var(--dim)">Interdits : visages, noms ou logos de sociétés, pelleteuses, foules, chiffres de résultats non cités, coupes sèches.</p></div>
</div>
<h2>Déclinaison verticale 9:16</h2>
<div class="grid v">{''.join(cell_v(c) for c in CELLS)}</div>
<footer>Carte : silhouette stylisée, positions des trois mines indicatives. Logo : redessiné en vectoriel d’après l’image fournie (remplaçable par le fichier source). Projet : videos/futura-kouroussa.</footer>
</body></html>"""
(ROOT / "storyboard.html").write_text(sheet)
print("storyboard.html written,", len(jobs), "sketches")
