"""Split the supplied MADINA DIGITAL logo into animation layers (nothing redrawn or recoloured).

The white ground is turned into alpha ("colour to alpha"), then pixels are sorted into layers by region and
hue: the blue M ribbon, the orange chevron, the two orange dots, the MADINA wordmark, DIGITAL. Every layer keeps
the same canvas (the lockup box of the source, y 80-960), so stacking them rebuilds the logo exactly.
Outputs: assets/logo/layers/{m,chevron,dot-l,dot-r,madina,digital,lockup}.png + layers.json
Usage: <venv>/bin/python -I tools/prep_logo.py <project dir>
"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image

P = Path(sys.argv[1]); OUT = P / "assets/logo/layers"; OUT.mkdir(parents=True, exist_ok=True)
rgb = np.asarray(Image.open(P / "assets/logo/madina-digital-logo.webp").convert("RGB")).astype(np.float32)
H, W, _ = rgb.shape
a = np.clip((255 - rgb).max(axis=2) / 255.0, 0, 1)
a = np.where(a < 0.04, 0, a)
col = np.clip(255 - (255 - rgb) / np.maximum(a, 1e-4)[..., None], 0, 255)
r, g, b = (rgb[..., i] / 255 for i in range(3))
mx, mn = np.maximum(np.maximum(r, g), b), np.minimum(np.minimum(r, g), b)
d = np.maximum(mx - mn, 1e-6)
hue = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
orange = (hue < 75) | (hue > 330)
yy, xx = np.mgrid[0:H, 0:W]
Y0, Y1 = 80, 960   # lockup canvas (the slogan and swoosh of the source are not used)
regions = {
    "m": (yy >= 90) & (yy < 528) & ~orange,
    "chevron": (yy >= 280) & (yy < 515) & orange,
    "dot-l": (yy >= 515) & (yy < 655) & (xx < W // 2) & orange,
    "dot-r": (yy >= 515) & (yy < 655) & (xx >= W // 2) & orange,
    "madina": (yy >= 650) & (yy < 832),
    "digital": (yy >= 832) & (yy < 955),
}
meta = {"canvas": [W, Y1 - Y0], "source_offset_y": Y0, "layers": {}}
for name, m in list(regions.items()) + [("lockup", (yy >= Y0) & (yy < Y1))]:
    alpha = np.where(m, a, 0)
    img = np.dstack([col, alpha * 255]).astype(np.uint8)[Y0:Y1]
    Image.fromarray(img, "RGBA").save(OUT / f"{name}.png", optimize=True)
    ys, xs = np.where(alpha[Y0:Y1] > 0.1)
    meta["layers"][name] = {"bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]} if len(xs) else {}
(OUT / "layers.json").write_text(json.dumps(meta, indent=1) + "\n")
print(json.dumps(meta["layers"]))
