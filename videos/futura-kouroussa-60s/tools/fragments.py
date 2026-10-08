"""Fragment expansion for the FUTURA-Kouroussa 60 s scenes (one source, three canvases).

Placeholders in scenes/fN.frag.html:
  {{svg:NAME}}                       an illustration (assets/illustrations) or the logo (emblem)
  {{plate:CLS|PHOTO|GRADE|h=fx,fy,z|v=fx,fy,z|s=fx,fy,z}}
                                     a 2.5D photo plate: clean background plate + detached nearest plane,
                                     both pre-graded with GRADE (assets/photos/graded, see tools/bake_grades.py).
                                     fx, fy: focus point in the photo (0-1) kept near the frame centre;
                                     z: coverage margin for camera moves (>= 1); an optional 4th/5th
                                     value (bw,bh) covers a box of that size instead of the frame.
  {{icon:NAME}}                      a line icon for the three guarantees
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ILL = ROOT / "assets" / "illustrations"
LOGO = ROOT / "assets" / "logo" / "emblem-negative.svg"
PHOTOS = ROOT / "assets" / "photos"
FORMATS = {"h": (1920, 1080), "v": (1080, 1920), "s": (1080, 1080)}


def _size(path):
    """Width/height of a JPEG or PNG without third-party modules."""
    b = path.read_bytes()
    if b[:8] == b"\x89PNG\r\n\x1a\n":
        return int.from_bytes(b[16:20], "big"), int.from_bytes(b[20:24], "big")
    i = 2
    while i < len(b):
        if b[i] != 0xFF: i += 1; continue
        m = b[i + 1]
        if m in (0xC0, 0xC1, 0xC2):
            return int.from_bytes(b[i + 7:i + 9], "big"), int.from_bytes(b[i + 5:i + 7], "big")
        i += 2 + int.from_bytes(b[i + 2:i + 4], "big")
    raise ValueError(path)


def _svg(name, uid):
    src = (LOGO if name == "emblem" else ILL / f"{name}.svg").read_text()
    src = re.sub(r'<svg xmlns="http://www.w3.org/2000/svg" ', '<svg ', src, count=1)
    if name == "map":  # clip the terrain hatch to the prefecture outline
        outline = re.search(r'class="outline" d="([^"]+)"', src).group(1)
        cid = f"{uid}-clip"
        src = src.replace('<path class="hatch"', f'<defs><clipPath id="{cid}"><path d="{outline}"/></clipPath></defs><path class="hatch" clip-path="url(#{cid})"', 1)
    if name == "emblem":
        src = src.replace("<svg ", '<svg class="emblem" ', 1)
    return src


def plate_geometry(photo, fmt, fx, fy, z, box=None):
    W, H = box or FORMATS[fmt]
    iw, ih = _size(PHOTOS / f"{photo}.jpg")
    k = max(W / iw, H / ih) * z
    pw, ph = iw * k, ih * k
    left = min(0.0, max(W - pw, W / 2 - fx * pw))
    top = min(0.0, max(H - ph, H / 2 - fy * ph))
    return round(left, 1), round(top, 1), round(pw, 1), round(ph, 1)


def _plate(arg, fmt):
    parts = arg.split("|")
    cls, photo, grade = parts[:3]
    geo = dict(p.split("=") for p in parts[3:])
    vals = [float(x) for x in geo[fmt].split(",")]
    fx, fy, z = vals[:3]
    left, top, pw, ph = plate_geometry(photo, fmt, fx, fy, z, tuple(vals[3:5]) if len(vals) == 5 else None)
    # transform origin of the camera move = focus point, in plate pixels
    ox, oy = round(fx * pw, 1), round(fy * ph, 1)
    if not (PHOTOS / "graded" / f"{photo}.{grade}-bg.jpg").exists():
        raise SystemExit(f"missing baked grade {photo}.{grade}: run tools/bake_grades.py")
    style = f"left:{left}px;top:{top}px;width:{pw}px;height:{ph}px"
    return (f'<div class="plate {cls}" style="{style}" data-ox="{ox}" data-oy="{oy}">'
            f'<img class="pl pl-bg" src="assets/photos/graded/{photo}.{grade}-bg.jpg" alt="">'
            f'<img class="pl pl-fg" src="assets/photos/graded/{photo}.{grade}-fg.png" alt="">'
            f'</div>')


ICONS = {
    "suivi": '<svg viewBox="0 0 80 80" fill="none" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"><circle class="ic-ring" cx="40" cy="40" r="34"/><path class="ic-a" d="M18 52 L32 38 L42 46 L60 26"/><path class="ic-b" d="M50 26 H60 V36"/></svg>',
    "audit": '<svg viewBox="0 0 80 80" fill="none" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"><circle class="ic-ring" cx="40" cy="40" r="34"/><circle class="ic-a" cx="36" cy="36" r="14"/><path class="ic-b" d="M46 46 L58 58 M29 36 L34 41 L43 31"/></svg>',
    "communautes": '<svg viewBox="0 0 80 80" fill="none" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"><circle class="ic-ring" cx="40" cy="40" r="34"/><path class="ic-a" d="M26 58 Q26 46 40 46 Q54 46 54 58 M40 40 A8 8 0 1 0 40 24 A8 8 0 1 0 40 40"/><path class="ic-b" d="M14 56 Q14 48 22 46 M66 56 Q66 48 58 46 M22 40 A6 6 0 1 1 22 28 M58 40 A6 6 0 1 0 58 28"/></svg>',
}


def expand(fragment, uid, fmt):
    def rep(m):
        kind, arg = m.group(1), m.group(2)
        if kind == "svg": return _svg(arg, f"{uid}-{arg}")
        if kind == "plate": return _plate(arg, fmt)
        if kind == "icon": return ICONS[arg]
        raise ValueError(m.group(0))
    return re.sub(r"\{\{(\w+):([^}]+)\}\}", rep, fragment)
