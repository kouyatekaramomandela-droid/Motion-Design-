"""Static sketches of every storyboard cell (16:9 + 9:16) from the real scene fragments, then storyboard.html.
Usage: python3 tools/sketch.py   (needs Playwright via node; screenshots with tools/shoot.cjs)
"""
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fragments import expand, ROOT

OUT = ROOT / "sketches"; PNG = OUT / "png"
OUT.mkdir(exist_ok=True); PNG.mkdir(exist_ok=True)
VERSION = "v1"

AXES = ["Désenclavement", "Eau potable", "Santé", "Éducation", "Agriculture et élevage", "Jeunesse", "Femmes",
        "Électricité et numérique"]
AX_IMG = ["vidéo 20 · le convoi", "illustration · bidons d’eau", "illustration · bâtiment de santé",
          "vidéo 20 · Centre de formation de Sankarani", "illustration · champ", "vidéo 20 · les jeunes aux drapeaux",
          "07 · assemblée des femmes", "illustration · enfant à la bougie"]
AX_WORD = ["Désenclavement", "Eau", "Santé", "Éducation", "Agriculture", "Jeunesse", "Femmes", "Électricité et numérique"]


def ax_css(k):
    hide = ",".join(f".rk .s4 .ax{i}" for i in range(1, 9) if i != k)
    on = ",".join(f".rk .s4 .dots .d{i}" for i in range(1, k + 1))
    return (f"{hide}{{display:none}} {on}{{border-color:var(--gold-3);background:var(--gold-2)}} "
            f".rk .s4 .dots .d{k}{{box-shadow:0 0 0 8px rgba(201,164,76,.3)}} "
            f".rk .s4 .dots .rail-fill{{width:calc((100% - 40px) * {(k - 1) / 7:.4f})}}")


CELLS = [
    dict(id="01", name="Ouverture", scene="s1", span="0:00–0:06",
         css="", cap="nous sommes allés à la rencontre",
         note="<b>D’abord :</b> fond blanc cassé et reflets d’or ; les photos 01 (Hon. KOUYATÉ) et 02 (Hon. KEITA) passent du flou au net ; le titre monte ligne par ligne, puis la date sur sa bande verte.",
         seam="fondu vers la carte"),
    dict(id="02", name="La tournée", scene="s2", span="0:06–0:18",
         css=".s2 .card .ph:not(.k1){display:none} .s2 .plabel:not(.l11){display:none}",
         cap="Des centaines de voix.",
         note="<b>D’abord :</b> le contour de la préfecture se dessine en or ; les 15 points s’allument un à un (0,6 s chacun), chaque nom apparaît à son tour ; les photos de rencontres défilent dans le cadre (1,6 s chacune) ; « 10 jours » puis « 15 localités » comptent.",
         seam="les photos s’assombrissent"),
    dict(id="03", name="Les urgences", scene="s3", span="0:18–0:28",
         css=".s3 .bgs .ph:not(.b1){display:none}", cap="l’eau potable, la santé, l’agriculture.",
         note="<b>D’abord :</b> photos de réunions assombries ; les trois compteurs montent à 15/15, chacun sur son mot ; puis les deux barres se remplissent à 14/15.",
         seam="glissé vers l’axe 1"),
]
for k in range(1, 9):
    CELLS.append(dict(id=f"04-{k}", name=f"Axe {k} · {AXES[k - 1]}", scene="s4",
                      span=f"0:{28 + 3 * (k - 1):02d}–0:{31 + 3 * (k - 1):02d}", css=ax_css(k), cap=AX_WORD[k - 1],
                      note=f"<b>Image :</b> {AX_IMG[k - 1]}. Le numéro, l’icône (tracée en or), le titre et la ligne arrivent sur le mot « {AX_WORD[k - 1].lower()} » ; le point {k} de la frise s’allume.",
                      seam="glissé vers l’axe suivant" if k < 8 else "fondu vers les recommandations"))
CELLS += [
    dict(id="05", name="Recommandations", scene="s5", span="0:52–1:06",
         css=".s5 .bgs .ph:not(.b1){display:none}", cap="suivre, et rendre compte.",
         note="<b>D’abord :</b> les trois colonnes tombent en cascade sur « transmettre », « plaider », « suivre » ; le fond très doux passe de la préfecture (03) à la réunion (12) puis aux sages (13).",
         seam="fondu vers le plan final"),
    dict(id="06a", name="Kouroussa a parlé", scene="s6", span="1:06–1:11",
         css=".s6 .sign,.s6 .white{display:none}", cap=None,
         note="<b>D’abord :</b> l’assemblée des femmes (06), léger zoom avant ; la phrase arrive en deux temps sur sa bande verte.",
         seam="fondu au blanc cassé"),
    dict(id="06b", name="Signature", scene="s6", span="1:11–1:15",
         css=".s6 .white{display:none}", cap=None,
         note="<b>D’abord :</b> les deux portraits (14, 18) entrent l’un après l’autre, puis les noms et « Députés de Kouroussa » ; fondu au blanc sur la dernière seconde.",
         seam="fin · fondu au blanc"),
]
V_CELLS = ["01", "02", "03", "04-3", "05", "06a", "06b"]


def page(cell, fmt):
    W, H = (1920, 1080) if fmt == "h" else (1080, 1920)
    frag = expand((ROOT / f"scenes/{cell['scene']}.frag.html").read_text(), f"{cell['id']}{fmt}", fmt)
    chrome = expand("{{chrome}}", "chrome", fmt)
    cap = f'<div class="rk-caption"><span>{cell["cap"]}</span></div>' if cell["cap"] else ""
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><base href="../">
<link rel="stylesheet" href="assets/film.css">
<style>html,body{{margin:0;width:{W}px;height:{H}px;background:#003D1F;overflow:hidden}} {cell['css']}</style></head>
<body><div class="rk {fmt}" style="width:{W}px;height:{H}px">{frag}{chrome}{cap}</div></body></html>"""


def main():
    jobs = []
    for c in CELLS:
        for fmt in ("h", "v"):
            if fmt == "v" and c["id"] not in V_CELLS:
                continue
            html = OUT / f"{c['id']}-{fmt}.html"
            html.write_text(page(c, fmt))
            W, H = (1920, 1080) if fmt == "h" else (1080, 1920)
            jobs.append({"html": str(html), "png": str(PNG / f"{c['id']}-{fmt}.jpg"), "w": W, "h": H})
    (OUT / "jobs.json").write_text(json.dumps(jobs))
    subprocess.run(["node", str(ROOT / "tools/shoot.cjs"), str(OUT / "jobs.json")], check=True)
    write_sheet()
    print("sketched", len(jobs))


def write_sheet():
    def fig(c):
        return (f'<figure class="cell" id="frame-{c["id"]}"><img src="sketches/png/{c["id"]}-h.jpg" alt="{c["name"]}">'
                f'<figcaption><div class="lab"><b>{c["id"]} · {c["name"].upper()}</b><span>{c["span"]}</span></div>'
                f'<p>{c["note"]}</p><span class="chip">→ {c["seam"]}</span></figcaption></figure>')
    main_cells = "".join(fig(c) for c in CELLS if not c["id"].startswith("04-") or c["id"] == "04-1")
    axes = "".join(fig(c) for c in CELLS if c["id"].startswith("04-"))
    vert = "".join(f'<figure class="cell v" id="frame-{i}-v"><img src="sketches/png/{i}-v.jpg" alt="{i} vertical">'
                   f'<figcaption><div class="lab"><b>{i}</b><span>{next(c["span"] for c in CELLS if c["id"] == i)}</span></div></figcaption></figure>'
                   for i in V_CELLS)
    (ROOT / "storyboard.html").write_text(f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rapport de la tournée — storyboard {VERSION}</title>
<style>
@font-face{{font-family:"Playfair Display";font-weight:700;src:url("assets/fonts/playfair-display-latin-700-normal.woff2")}}
@font-face{{font-family:"Inter";font-weight:400;src:url("assets/fonts/inter-latin-400-normal.woff2")}}
@font-face{{font-family:"Inter";font-weight:600;src:url("assets/fonts/inter-latin-600-normal.woff2")}}
:root{{--ivory:#F6F2E9;--green:#006633;--deep:#003D1F;--ink:#00291A;--gold:#C9A44C;--gold-l:#E6CC86;--gold-d:#8B6914;--dim:#B9C4B8}}
body{{margin:0;background:var(--ink);color:var(--ivory);font-family:Inter,sans-serif}}
header{{padding:40px 48px 8px;display:flex;flex-wrap:wrap;align-items:baseline;gap:18px 28px}}
h1{{margin:0;font-family:"Playfair Display",serif;font-size:42px}}
h1 small{{font-family:Inter;font-size:16px;font-weight:600;color:var(--gold-l);letter-spacing:.14em;margin-left:10px}}
.dek{{color:var(--dim);font-size:17px;max-width:820px;line-height:1.5}}
.tag{{margin-left:auto;font-size:13px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--ink);background:var(--gold);padding:8px 14px;border-radius:999px}}
h2{{margin:34px 48px 14px;font-size:14px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold-l)}}
.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:26px;padding:0 48px}}
.grid.ax{{grid-template-columns:repeat(4,minmax(0,1fr))}}
.grid.v{{grid-template-columns:repeat(7,minmax(0,1fr))}}
@media (max-width:1100px){{.grid,.grid.ax{{grid-template-columns:1fr}} .grid.v{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
.cell{{margin:0;background:var(--deep);border-radius:12px;overflow:hidden;border:1px solid rgba(201,164,76,.4)}}
.cell img{{display:block;width:100%;aspect-ratio:16/9;object-fit:cover}}
.cell.v img{{aspect-ratio:9/16}}
figcaption{{padding:14px 18px 18px}}
.lab{{display:flex;justify-content:space-between;gap:12px;font-size:13px;letter-spacing:.06em}}
.lab b{{color:var(--gold-l)}} .lab span{{color:var(--dim)}}
figcaption p{{margin:10px 0 12px;font-size:14.5px;line-height:1.5;color:#DCE3D9}} figcaption p b{{color:var(--ivory)}}
.chip{{display:inline-block;font-size:12px;font-weight:600;color:var(--gold-l);border:1.5px solid var(--gold-d);border-radius:999px;padding:5px 11px}}
.panel{{background:var(--deep);border-radius:12px;padding:22px 24px;border:1px solid rgba(201,164,76,.4);font-size:14.5px;line-height:1.55}}
.panel h3{{margin:0 0 10px;font-family:"Playfair Display",serif;font-size:24px}}
.sw{{display:inline-flex;align-items:center;gap:8px;margin:4px 14px 4px 0}} .sw i{{width:22px;height:22px;border-radius:6px;display:inline-block;border:1px solid rgba(255,255,255,.25)}}
footer{{padding:30px 48px 60px;color:var(--dim);font-size:13px}}
</style></head><body>
<header><h1>Rapport de la tournée des Députés — storyboard<small>{VERSION}</small></h1>
<span class="tag">1920×1080 + 1080×1920 · 30 i/s · 75 s · 6 scènes</span>
<p class="dek">Images fixes au moment clé de chaque scène, avec les vraies polices, couleurs, textes, sous-titres, logos et photos de la mission. Photos encore brutes : nettoyage (plaques, tampons, marques) et étalonnage chaud à l’étape suivante. Le mouvement arrive au montage.</p></header>
<h2>Master 16:9</h2>
<div class="grid">{main_cells}
<div class="panel"><h3>Enchaînements</h3><p>S1 fondu → S2 carte → S3 photos assombries → S4 huit axes en glissé, frise de 8 points → S5 colonnes en cascade → S6 plan réel, signature, fondu au blanc.</p><p style="color:var(--dim)">Zooms lents de 3 à 5 %, aucun flash, aucune coupe brusque.</p></div>
<div class="panel"><h3>Charte</h3>
<div><span class="sw"><i style="background:#F6F2E9"></i>#F6F2E9</span><span class="sw"><i style="background:#006633"></i>#006633</span><span class="sw"><i style="background:#8B6914"></i>#8B6914</span><span class="sw"><i style="background:#C9A44C"></i>#C9A44C</span><span class="sw"><i style="background:#CE1126"></i></span><span class="sw"><i style="background:#FCD116"></i></span><span class="sw"><i style="background:#009460"></i></span></div>
<p>Titres : Playfair Display · Textes et sous-titres : Inter. Bandeaux vert foncé liserés d’or, marges 8 %.</p>
<p style="color:var(--dim)">Interdits : visage ou lieu inventé ou retouché, image étirée, flash, effet tape-à-l’œil.</p></div>
</div>
<h2>Les 8 axes (S4, 3 s chacun)</h2>
<div class="grid ax">{axes}</div>
<h2>Déclinaison verticale 9:16</h2>
<div class="grid v">{vert}</div>
<footer>Carte : limites administratives OCHA / PAM (geoBoundaries, CC BY 3.0 IGO) ; Fadoussaba et Kouroukoro placées d’après OpenStreetMap ; Kanséréya en position indicative. Version sans texte : mêmes images, sans titres, chiffres ni sous-titres.</footer>
</body></html>
""")


if __name__ == "__main__":
    main()
