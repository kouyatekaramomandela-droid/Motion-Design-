"""Cut the pieces the film animates out of the three supplied screens (pixels kept as they are: crop only).

Outputs assets/prep/*.png (+ crops.json with each source box, so the build can place an overlay exactly over
its place in the full screen).
Usage: <venv>/bin/python -I tools/crops.py <project dir>
"""
import json, sys
from pathlib import Path
from PIL import Image

P = Path(sys.argv[1]); E = P / "assets/ecrans"; OUT = P / "assets/prep"; OUT.mkdir(parents=True, exist_ok=True)
SIGNUP, LOGIN, HOME = "01_creer-un-compte.webp", "02_connexion.webp", "03_accueil.webp"
# module tiles of the home page (left, right) on y 524-668, in the order of the brief
TILES = [("makiti", 35, 158), ("pharmacie", 160, 289), ("services", 290, 419), ("makeup", 420, 551),
         ("tontine", 552, 676), ("marketplace", 677, 806), ("bank", 807, 931), ("agritech", 932, 1053),
         ("immo", 1054, 1173), ("sante", 1174, 1291), ("edutech", 1292, 1406), ("move", 1407, 1512)]
BOXES = {
    # S2: the photo behind the sign-up form (lighthouse, sea, city, the woman on her phone)
    "hero-guinee": (SIGNUP, (335, 360, 662, 884)),
    # S5 bubbles: photos of the home page
    "photo-alimentation": (HOME, (705, 726, 857, 808)),
    "photo-pharmacie": (HOME, (872, 726, 1010, 808)),
    "photo-transport": (HOME, (1342, 726, 1495, 808)),
    "photo-marketplace": (HOME, (352, 694, 518, 842)),
    "module-strip": (HOME, (35, 524, 1512, 668)),
    "panel-12-modules": (HOME, (1268, 120, 1505, 207)),
    # S6: the four trust badges of the home panel
    "badge-paiement": (HOME, (1272, 218, 1506, 267)),
    "badge-livraison": (HOME, (1272, 273, 1506, 322)),
    "badge-service": (HOME, (1272, 329, 1506, 378)),
    "badge-experience": (HOME, (1272, 384, 1506, 433)),
    # S7: the key-figures band of the sign-up screen (+100 000, as confirmed by the client)
    "band": (SIGNUP, (0, 897, 1536, 1024)),
    "band-explorer": (SIGNUP, (1266, 922, 1498, 969)),
    "band-figures": (SIGNUP, (480, 897, 1530, 1024)),
    "band-users": (SIGNUP, (500, 915, 680, 975)),
    "band-modules": (SIGNUP, (722, 915, 880, 975)),
    "band-secure": (SIGNUP, (915, 915, 1030, 975)),
    "band-partout": (SIGNUP, (1080, 915, 1200, 975)),
    # buttons pressed in S3/S4 (cropped so they can be pushed in)
    "btn-signup": (SIGNUP, (687, 676, 1191, 725)),
    "btn-login": (LOGIN, (834, 547, 1311, 601)),
    # the phone of the home hero
    "phone": (HOME, (995, 140, 1205, 516)),
}
for name, l, r in TILES:
    BOXES[f"tile-{name}"] = (HOME, (l, 524, r, 668))
    c = (l + r) // 2
    BOXES[f"icon-{name}"] = (HOME, (c - 34, 528, c + 34, 597))
meta = {}
for name, (src, box) in BOXES.items():
    Image.open(E / src).convert("RGB").crop(box).save(OUT / f"{name}.png", optimize=True)
    meta[name] = {"src": src, "box": list(box)}
# colour of the band behind each figure, to cover it before the count-up redraws it
import numpy as np
band = np.asarray(Image.open(E / SIGNUP).convert("RGB")).astype(float)
for key, (x0, y0, x1, y1) in {"users": (566, 926, 632, 948), "modules": (779, 926, 802, 948), "secure": (971, 926, 1012, 948)}.items():
    ring = np.concatenate([band[y0 - 3:y0, x0:x1].reshape(-1, 3), band[y1:y1 + 3, x0:x1].reshape(-1, 3)])
    meta[f"figure-{key}"] = {"src": SIGNUP, "box": [x0, y0, x1, y1], "bg": "#%02X%02X%02X" % tuple(int(v) for v in ring.mean(0))}
(OUT / "crops.json").write_text(json.dumps(meta, indent=1) + "\n")
print(len(meta), "crops")
