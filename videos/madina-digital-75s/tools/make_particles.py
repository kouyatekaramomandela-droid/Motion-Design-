"""Bake the studio's orange/gold light particles into two transparent layers per canvas (far: small and sharp,
near: large and soft), so the background composition animates 2 images instead of ~50 gradient elements
(heavy overlays can make the capture go black). Deterministic seed.
Outputs: assets/prep/particles-{h,v}-{far,near}.png
Usage: <venv>/bin/python -I tools/make_particles.py <project dir>
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image

P = Path(sys.argv[1])
COLOURS = [(255, 138, 30), (255, 176, 80), (255, 95, 31), (255, 214, 140)]
for fmt, (W, H) in {"h": (1920, 1080), "v": (1080, 1920)}.items():
    rng = np.random.default_rng(20261010 + (0 if fmt == "h" else 7))
    for layer, n, sizes, alpha in (("far", 60, (3, 4, 5, 7), (0.35, 0.8)), ("near", 18, (14, 20, 30, 44), (0.12, 0.3))):
        img = np.zeros((H + 200, W + 200, 4), np.float32)
        yy, xx = np.mgrid[0:H + 200, 0:W + 200]
        for _ in range(n):
            r = float(rng.choice(sizes)); x, y = rng.uniform(0, W + 200), rng.uniform(0, H + 200)
            c = COLOURS[rng.integers(len(COLOURS))]; a = rng.uniform(*alpha)
            x0, x1, y0, y1 = int(max(0, x - 3 * r)), int(min(W + 200, x + 3 * r)), int(max(0, y - 3 * r)), int(min(H + 200, y + 3 * r))
            d2 = ((xx[y0:y1, x0:x1] - x) ** 2 + (yy[y0:y1, x0:x1] - y) ** 2) / (r * r)
            g = a * np.exp(-d2 * 1.6)
            sub = img[y0:y1, x0:x1]
            sub[..., :3] = np.maximum(sub[..., :3], np.array(c, np.float32) * (g[..., None] > 0))
            sub[..., 3] = np.maximum(sub[..., 3], g)
        out = np.dstack([img[..., :3], np.clip(img[..., 3], 0, 1) * 255]).astype(np.uint8)
        Image.fromarray(out, "RGBA").save(P / f"assets/prep/particles-{fmt}-{layer}.png", optimize=True)
print("particles baked")
