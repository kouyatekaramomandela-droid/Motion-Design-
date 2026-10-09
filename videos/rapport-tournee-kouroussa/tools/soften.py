"""Pre-blurred versions of the graded media, used for the soft backgrounds (S4, S5) and the blur-to-sharp
opening of S1. Baked once (960 px wide, Gaussian blur) instead of a CSS blur filter on every frame
(no GPU in this container).
Outputs: assets/prep/<key>-soft.jpg, assets/prep/clips/<key>-soft.mp4
Usage: <venv>/bin/python -I tools/soften.py <project dir>
"""
import subprocess, sys
from pathlib import Path
import cv2

ROOT = Path(sys.argv[1]).resolve(); PREP = ROOT / "assets/prep"
for jpg in sorted(PREP.glob("*.jpg")):
    if jpg.stem.endswith("-soft"): continue
    img = cv2.imread(str(jpg)); h, w = img.shape[:2]; k = 960 / w
    small = cv2.resize(img, (960, round(h * k)), interpolation=cv2.INTER_AREA)
    soft = cv2.GaussianBlur(small, (0, 0), 9)
    cv2.imwrite(str(PREP / f"{jpg.stem}-soft.jpg"), soft, [cv2.IMWRITE_JPEG_QUALITY, 88])
for mp4 in sorted((PREP / "clips").glob("*.mp4")):
    if mp4.stem.endswith("-soft"): continue
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp4), "-vf", "scale=480:-2,gblur=sigma=5", "-an",
                    "-c:v", "libx264", "-crf", "22", "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                    str(PREP / "clips" / f"{mp4.stem}-soft.mp4")], check=True)
print("softened")
