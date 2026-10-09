"""Transparent, trimmed versions of the client logos (assets/logos → assets/logos/prep).

- républic emblem: already transparent, trimmed.
- AN emblem (white square): background removed by flood fill from the border, so the emblem stays opaque.
- AN logo with wordmark, Simandou 2040, Guinée brand: white → alpha ("colour to alpha"), exact on light grounds.
No logo is redrawn, recoloured or distorted; only the white ground is removed and the margins trimmed.
Usage: venv/bin/python -I tools/prep_logos.py <project dir>
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

P = Path(sys.argv[1]); SRC = P / "assets/logos"; OUT = SRC / "prep"; OUT.mkdir(exist_ok=True)

def trim(im, pad=6):
    a = np.array(im)[..., 3]
    ys, xs = np.where(a > 8)
    box = (max(0, xs.min() - pad), max(0, ys.min() - pad), min(im.width, xs.max() + pad + 1), min(im.height, ys.max() + pad + 1))
    return im.crop(box)

def colour_to_alpha(path):
    rgb = np.asarray(Image.open(path).convert("RGB")).astype(np.float32)
    a = np.clip((255 - rgb).max(axis=2) / 255.0, 0, 1)
    a = np.where(a < 0.035, 0, a)  # jpeg noise on the white ground
    safe = np.maximum(a, 1e-4)[..., None]
    col = np.clip(255 - (255 - rgb) / safe, 0, 255)
    return Image.fromarray(np.dstack([col, a * 255]).astype(np.uint8), "RGBA")

def flood_ground(path, tol=28):
    rgb = np.asarray(Image.open(path).convert("RGB")).astype(np.int16)
    white = (255 - rgb).max(axis=2) < tol
    lab, _ = ndimage.label(white)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    ground = np.isin(lab, list(border))
    # soft edge: 1.2 px feather of the ground mask
    alpha = 1 - ndimage.gaussian_filter(ground.astype(np.float32), 1.2)
    alpha[ground & (ndimage.distance_transform_edt(~ground) > 2)] = 0
    return Image.fromarray(np.dstack([rgb.astype(np.uint8), (np.clip(alpha, 0, 1) * 255).astype(np.uint8)]), "RGBA")

jobs = {
    "republique-de-guinee-armoiries.png": lambda p: Image.open(p).convert("RGBA"),
    "assemblee-nationale-embleme.png": lambda p: flood_ground(SRC / "assemblee-nationale-embleme.jpg"),
    "assemblee-nationale-logo.png": lambda p: colour_to_alpha(SRC / "assemblee-nationale-depuis-rapport.jpg"),
    "guinee-marque-nationale.png": lambda p: colour_to_alpha(SRC / "guinee-marque-nationale.jpg"),
    "simandou-2040.png": lambda p: Image.open(p).convert("RGBA"),
}
for name, fn in jobs.items():
    im = trim(fn(SRC / name))
    im.save(OUT / name, optimize=True)
    print(name, im.size)
