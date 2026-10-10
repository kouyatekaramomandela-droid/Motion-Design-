"""Storyboard sheet from real frames of the built compositions (one key moment per cell, both canvases).
Snapshots are taken with `hyperframes snapshot`, then storyboard.html is written and photographed as one JPEG.
Usage: python3 tools/sheet.py   (from the project root)
"""
import shutil, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V = ROOT.parent / (ROOT.name + "-9x16")
CLI = ["npx", "--yes", "hyperframes@0.8.145"]
VERSION = "v1"
CELLS = [
    ("01", "Logo", "0:00–0:06", 3.4, 3.6, "Le M bleu se déplie dans l’espace, reflet métallique ; chevron, points, MADINA puis DIGITAL ; le slogan s’écrit en bleu marine.", "« Madina Digital. »"),
    ("02", "Contexte Guinée", "0:06–0:12", 7.0, 7.0, "Plan rapproché sur le phare et la ville, la caméra recule et révèle la femme au téléphone ; « La Guinée à portée de main ».", "« En Guinée, tout va vite… à portée de main. »"),
    ("03a", "Inscription · saisie", "0:12–0:20", 16.5, 16.5, "La fenêtre arrive en arc, zoom sur le formulaire ; le curseur orange va de champ en champ, chaque champ se remplit avec un halo bleu.", "« Créer votre compte ? … un mot de passe… »"),
    ("03b", "Inscription · validée", "0:20–0:22", 20.6, 20.6, "Étapes 2 et 3 allumées, pression sur « S’inscrire », coche verte.", "« … et c’est validé ! »"),
    ("04a", "Connexion", "0:22–0:25", 24.2, 24.2, "Même traitement : e-mail, mot de passe, pression sur « Se connecter ».", "« Connectez-vous… »"),
    ("04b", "Accueil", "0:25–0:30", 27.4, 27.4, "Volet bleu-orange, la page d’accueil se pose en 3D, la recherche prend le focus.", "« plus qu’une super-application, une vie plus simple ! »"),
    ("05a", "12 modules · Makiti", "0:30–0:57", 33.2, 33.2, "Les 12 vignettes sortent de la page et s’allument une à une (2 s chacune) ; bulle photo pour Makiti, Pharmacie, Tontine, Marketplace, Move.", "« Douze modules, une seule application. Makiti pour vos courses… »"),
    ("05b", "12 modules · Move", "0:52–0:57", 55.0, 55.0, "Dernier module : Move, avec le livreur à moto ; le panneau « 12 modules » respire.", "« … et Move, pour vous déplacer et vous faire livrer. »"),
    ("06", "Bénéfices", "0:57–1:06", 65.6, 65.6, "Les 4 pastilles basculent en cartes 3D sur leurs mots, puis « Votre vie, plus simple ! » se trace en orange.", "« Paiement sécurisé… Votre vie, plus simple ! »"),
    ("07a", "Signature · chiffres", "1:06–1:12", 69.0, 69.0, "Logo dans la lumière ; le bandeau se déploie, +100 000, 12, 100 % comptent ; « Explorer tous les modules » pulse.", "« Madina Digital : commander, recevoir, vivre mieux… »"),
    ("07b", "Signature · fin", "1:12–1:15", 73.4, 73.4, "Le logo seul au centre, fondu au noir, la lumière orange s’éteint en dernier.", "« … partout en Guinée. »"),
]


def snap(proj, times, out):
    shutil.rmtree(out, ignore_errors=True)
    subprocess.run(CLI + ["snapshot", str(proj), "--at", ",".join(str(t) for t in times), "--no-end", "--describe", "false",
                          "--timeout", "120000", "-o", str(out)], check=True, capture_output=True)
    return sorted(out.glob("frame-*.png"))


def main():
    png = ROOT / "sketches/png"; png.mkdir(parents=True, exist_ok=True)
    for proj, idx, sfx in ((ROOT, 3, "h"), (V, 4, "v")):
        frames = snap(proj, [c[idx] for c in CELLS], ROOT / f".hyperframes/sheet-{sfx}")
        for c, f in zip(CELLS, frames):
            subprocess.run(["convert", str(f), "-resize", "960x960", "-quality", "86", str(png / f"{c[0]}-{sfx}.jpg")], check=True)
    cells = "".join(
        f'<figure class="cell" id="frame-{c[0]}"><img src="sketches/png/{c[0]}-h.jpg" alt="{c[1]}"><figcaption>'
        f'<div class="lab"><b>{c[0]} · {c[1].upper()}</b><span>{c[2]}</span></div><p>{c[5]}</p><p class="vo">{c[6]}</p></figcaption></figure>'
        for c in CELLS)
    vert = "".join(f'<figure class="cell v"><img src="sketches/png/{c[0]}-v.jpg" alt="{c[1]} 9:16"><figcaption><div class="lab"><b>{c[0]}</b><span>{c[2]}</span></div></figcaption></figure>' for c in CELLS)
    (ROOT / "storyboard.html").write_text(f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>MADINA DIGITAL — storyboard {VERSION}</title>
<style>
@font-face{{font-family:"Poppins";font-weight:400;src:url("assets/fonts/poppins-latin-400-normal.woff2")}}
@font-face{{font-family:"Poppins";font-weight:600;src:url("assets/fonts/poppins-latin-600-normal.woff2")}}
@font-face{{font-family:"Poppins";font-weight:800;src:url("assets/fonts/poppins-latin-800-normal.woff2")}}
body{{margin:0;background:#081436;color:#fff;font-family:Poppins,sans-serif}}
header{{padding:36px 44px 6px;display:flex;flex-wrap:wrap;align-items:baseline;gap:14px 26px}}
h1{{margin:0;font-size:38px;font-weight:800}} h1 small{{font-size:15px;color:#FF8A1E;letter-spacing:.14em;margin-left:10px}}
.dek{{color:#B9C6EE;font-size:16px;max-width:900px;line-height:1.5}}
.tag{{margin-left:auto;font-size:13px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:#081436;background:#FF8A1E;padding:8px 14px;border-radius:999px}}
h2{{margin:30px 44px 12px;font-size:14px;letter-spacing:.2em;text-transform:uppercase;color:#FFB25C}}
.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px;padding:0 44px}}
.grid.v{{grid-template-columns:repeat(11,minmax(0,1fr));gap:10px}}
@media (max-width:1100px){{.grid{{grid-template-columns:1fr}} .grid.v{{grid-template-columns:repeat(3,minmax(0,1fr))}}}}
.cell{{margin:0;background:#0E2366;border-radius:14px;overflow:hidden;border:1px solid rgba(255,138,30,.35)}}
.cell img{{display:block;width:100%;aspect-ratio:16/9;object-fit:cover}} .cell.v img{{aspect-ratio:9/16}}
figcaption{{padding:12px 16px 16px}} .v figcaption{{padding:6px 8px 8px}}
.lab{{display:flex;justify-content:space-between;gap:10px;font-size:12.5px;letter-spacing:.06em}} .lab b{{color:#FFB25C}} .lab span{{color:#9FB0E6}}
figcaption p{{margin:8px 0 0;font-size:14px;line-height:1.5;color:#DDE5FF}} figcaption p.vo{{color:#FFB25C;font-style:italic}}
footer{{padding:26px 44px 50px;color:#9FB0E6;font-size:13px;line-height:1.6}}
</style></head><body>
<header><h1>MADINA DIGITAL — storyboard<small>{VERSION}</small></h1><span class="tag">1920×1080 + 1080×1920 · 30 i/s · 75 s · 7 séquences</span>
<p class="dek">Images fixes tirées du film déjà monté, au moment clé de chaque séquence. Vos écrans sont repris tels quels ; seuls le curseur, la saisie, les étapes, la coche et les compteurs sont ajoutés. En orange : la voix off (Amadou), qui sera calée sur ces moments.</p></header>
<h2>Master 16:9</h2><div class="grid">{cells}</div>
<h2>Version verticale 9:16</h2><div class="grid v">{vert}</div>
<footer>Musique et sons : générés sur place (libres de droits), ajoutés avec la voix. Chiffre retenu : +100 000 utilisateurs. Photos : uniquement celles de vos écrans.</footer>
</body></html>
""")
    subprocess.run(["node", str(ROOT / "tools/sheet.cjs"), str(ROOT / "storyboard.html"), str(ROOT / "sketches/storyboard-v1.jpg"), "1600"], check=True)
    print("sheet written")


if __name__ == "__main__":
    main()
