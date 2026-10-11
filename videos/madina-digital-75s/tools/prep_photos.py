"""Prepare the generated illustration photos (assets/generated/*.jpg, 1680x944, Canva AI) for the v2 film.

  assets/generated/blur/<name>.jpg   9:16 cover crop around the subject, blurred and tinted night blue: the
                                     full-bleed backdrop behind the sharp photo card in the vertical film
  assets/generated/tint/conakry-nuit-{h,v}.jpg   the aerial view of Conakry as a blue duotone for the signature

FOCUS is the horizontal centre of the subject (0..1); the vertical film crops the photos around it, and
scenes/*.frag.html use the same values as object-position. Usage: python3 tools/prep_photos.py
"""
from pathlib import Path
from PIL import Image, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets/generated"
NIGHT = (10, 26, 74)

FOCUS = {
    "conakry-aerien": 0.40, "phare": 0.68,
    "makiti": 0.35, "pharmacie": 0.40, "services": 0.52, "makeup": 0.58, "tontine": 0.45, "marketplace": 0.42,
    "bank": 0.35, "agritech": 0.70, "immo": 0.50, "sante": 0.35, "edutech": 0.50, "move": 0.45,
    "b-paiement": 0.60, "b-livraison": 0.50, "b-service": 0.45, "b-experience": 0.50,
}


def cover(im, w, h, fx):
    s = max(w / im.width, h / im.height)
    r = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = min(max(0, round(r.width * fx - w / 2)), r.width - w)
    y = (r.height - h) // 2
    return r.crop((x, y, x + w, y + h))


def main():
    (SRC / "blur").mkdir(exist_ok=True)
    (SRC / "tint").mkdir(exist_ok=True)
    for name, fx in FOCUS.items():
        im = Image.open(SRC / f"{name}.jpg").convert("RGB")
        b = cover(im, 360, 640, fx).filter(ImageFilter.GaussianBlur(16))
        b = Image.blend(b, Image.new("RGB", b.size, NIGHT), 0.42)
        b.save(SRC / "blur" / f"{name}.jpg", quality=88)
    aer = Image.open(SRC / "conakry-aerien.jpg").convert("L")
    for fmt, (w, h) in {"h": (1920, 1080), "v": (720, 1280)}.items():
        g = cover(aer, w, h, FOCUS["conakry-aerien"])
        if fmt == "v":
            g = g.filter(ImageFilter.GaussianBlur(2))
        ImageOps.colorize(ImageOps.autocontrast(g, cutoff=1), black=(6, 14, 46), white=(120, 160, 255), mid=(30, 63, 217)).save(
            SRC / "tint" / f"conakry-nuit-{fmt}.jpg", quality=88)
    print("ok", len(FOCUS), "photos")


if __name__ == "__main__":
    main()
