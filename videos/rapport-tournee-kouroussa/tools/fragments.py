"""Fragment expansion for the report film (one scene source, two canvases + the textless build).

Placeholders in scenes/sN.frag.html:
  {{ph:CLS|KEY|h=fx,fy|v=fx,fy[|soft]}}  a photo or clip slot: <div class="ph CLS"><img|video ...></div>.
                                         KEY names a source in MEDIA; the cleaned, graded version in
                                         assets/prep/ is used when it exists. fx, fy (0-100) is the focus
                                         point kept in frame (object-position), so faces are never cut.
  {{map}}                                the prefecture map (assets/map) with its 15 points
  {{icon:NAME}}                          a gold line icon (the 8 axes)
  {{chrome}}                             the fixed logos (top and bottom)
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORMATS = {"h": (1920, 1080), "v": (1080, 1920)}

M, I = "assets/mission", "assets/illustration"
MEDIA = {
    "m01": f"{M}/01_hon-lamine-kouyate-portrait-exterieur.jpg",
    "m02": f"{M}/02_hon-dre-hadja-djoran-keita-accueil.jpg",
    "m03": f"{M}/03_prefecture-kouroussa-bloc-administratif.jpg",
    "m04": f"{M}/04_delegation-marche-terrain.jpg",
    "m05": f"{M}/05_officiels-sous-tente.jpg",
    "m06": f"{M}/06_assemblee-des-femmes-20-sept.jpg",
    "m07": f"{M}/07_assemblee-des-femmes-2.jpg",
    "m08": f"{M}/08_accueil-officiels-echarpes.jpg",
    "m09": f"{M}/09_rencontre-plein-air-communaute.jpg",
    "m10": f"{M}/10_banniere-bienvenue-chez-toi.jpg",
    "m12": f"{M}/12_hon-keita-reunion-site-minier.jpg",
    "m13": f"{M}/13_reunion-des-sages.jpg",
    "m14": f"{M}/14_hon-lamine-kouyate-portrait.jpg",
    "m15": f"{M}/15_rencontre-autorites-prefectorales.jpg",
    "m16": f"{M}/16_visite-village.jpg",
    "m17": f"{M}/17_hon-keita-avec-un-habitant.jpg",
    "m18": f"{M}/18_hon-keita-prise-de-parole.jpg",
    "i01": f"{I}/01_eau-potable-jerricans.jpg",
    "i02": f"{I}/02_sante-batiment-de-sante.jpg",
    "i03": f"{I}/03_agriculture-champ.jpg",
    "i04": f"{I}/04_electricite-enfant-a-la-bougie.jpg",
    # clips from 20_video-accueil-populations.mp4 (stills until the clips are cut)
    "v-convoi": "assets/prep/stills/v20-convoi.jpg",
    "v-jeunesse": "assets/prep/stills/v20-jeunesse.jpg",
    "v-foule": "assets/prep/stills/v20-foule.jpg",
    "v-sankarani": "assets/prep/stills/v20-sankarani.jpg",
}
ILLUSTRATION = {"i01", "i02", "i03", "i04"}


def media_src(key):
    clip = ROOT / f"assets/prep/clips/{key}.mp4"
    if key.startswith("v-") and clip.exists():
        return "video", f"assets/prep/clips/{key}.mp4"
    prep = ROOT / f"assets/prep/{key}.jpg"
    return "img", (f"assets/prep/{key}.jpg" if prep.exists() else MEDIA[key])


def _ph(arg, fmt):
    parts = arg.split("|")
    cls, key = parts[0], parts[1]
    opts = dict(p.split("=") for p in parts[2:] if "=" in p)
    flags = [p for p in parts[2:] if "=" not in p]
    fx, fy = (opts.get(fmt) or opts.get("h") or "50,50").split(",")
    kind, src = media_src(key)
    pos = f"object-position:{fx}% {fy}%"
    if kind == "video":
        el = f'<video src="{src}" muted playsinline style="{pos}"></video>'
    else:
        el = f'<img src="{src}" alt="" style="{pos}">'
    soft = " soft" if "soft" in flags else ""
    tag = ('<span class="illus-tag tx">Image d’illustration</span>'
           if key in ILLUSTRATION and "soft" not in flags and "notag" not in flags else "")
    return f'<div class="ph {cls}{soft}" data-key="{key}">{el}{tag}</div>'


def _map():
    svg = (ROOT / "assets/map/map.svg").read_text().strip()
    data = json.loads((ROOT / "assets/map/points.json").read_text())
    W, H = data["w"], data["h"]
    dots = []
    for p in data["points"]:
        dots.append(f'<g class="pt p{p["i"]}" transform="translate({p["x"]} {p["y"]})">'
                    f'<circle class="halo" r="34"/><circle class="ring" r="15"/><circle class="dot" r="9"/></g>')
    svg = svg.replace("</svg>", '<g class="pts">' + "".join(dots) + "</g></svg>")
    svg = svg.replace("<svg ", '<svg class="mapsvg" preserveAspectRatio="xMidYMid meet" ', 1)
    labels = "".join(
        f'<div class="plabel tx l{p["i"]}" style="left:{p["x"] / W * 100:.2f}%;top:{p["y"] / H * 100:.2f}%">'
        f'<span>{p["name"]}{"<small>" + p["sub"] + "</small>" if p["sub"] else ""}</span></div>'
        for p in data["points"])
    return f'<div class="mapbox">{svg}<div class="plabels">{labels}</div></div>'


# gold line icons, 100x100, stroke drawn by the animation (class ic-s)
ICONS = {
    "routes": '<path class="ic-s" d="M30 92 L44 14 M70 92 L56 14"/><path class="ic-s" d="M50 84 V72 M50 58 V48 M50 36 V28"/><path class="ic-s" d="M8 64 Q50 40 92 64"/><path class="ic-s" d="M18 58 V70 M82 58 V70"/>',
    "eau": '<path class="ic-s" d="M50 10 C50 10 22 44 22 62 A28 28 0 0 0 78 62 C78 44 50 10 50 10 Z"/><path class="ic-s" d="M36 64 A14 14 0 0 0 50 78"/>',
    "sante": '<rect class="ic-s" x="10" y="10" width="80" height="80" rx="14"/><path class="ic-s" d="M40 24 H60 V40 H76 V60 H60 V76 H40 V60 H24 V40 H40 Z"/>',
    "education": '<path class="ic-s" d="M50 28 C38 20 22 18 8 20 V80 C22 78 38 80 50 88 C62 80 78 78 92 80 V20 C78 18 62 20 50 28 Z"/><path class="ic-s" d="M50 28 V88"/><path class="ic-s" d="M20 36 C28 36 36 38 42 42 M58 42 C64 38 72 36 80 36"/>',
    "agriculture": '<path class="ic-s" d="M50 92 V30"/><path class="ic-s" d="M50 62 C34 62 24 50 22 36 C38 36 48 46 50 62 Z"/><path class="ic-s" d="M50 50 C66 50 76 38 78 24 C62 24 52 34 50 50 Z"/><path class="ic-s" d="M50 30 C44 24 44 14 50 8 C56 14 56 24 50 30 Z"/><path class="ic-s" d="M14 92 H86"/>',
    "jeunesse": '<circle class="ic-s" cx="40" cy="26" r="12"/><path class="ic-s" d="M16 88 C16 64 26 52 40 52 C50 52 58 58 62 68"/><path class="ic-s" d="M66 92 V52 M54 64 L66 52 L78 64"/><path class="ic-s" d="M80 22 L84 30 L92 31 L86 37 L88 45 L80 41 L72 45 L74 37 L68 31 L76 30 Z"/>',
    "femmes": '<circle class="ic-s" cx="50" cy="28" r="12"/><path class="ic-s" d="M34 26 C34 12 66 12 66 26"/><path class="ic-s" d="M28 90 L36 54 C40 46 60 46 64 54 L72 90 Z"/><circle class="ic-s" cx="18" cy="44" r="8"/><path class="ic-s" d="M6 82 C6 66 12 58 22 58"/><circle class="ic-s" cx="82" cy="44" r="8"/><path class="ic-s" d="M94 82 C94 66 88 58 78 58"/>',
    "electricite": '<path class="ic-s" d="M52 8 L24 54 H46 L40 92 L72 40 H50 Z"/><path class="ic-s" d="M76 22 A18 18 0 0 1 76 48 M84 12 A30 30 0 0 1 84 58"/>',
}


def _icon(name):
    return (f'<svg class="icon ic-{name}" viewBox="0 0 100 100" fill="none" stroke-linecap="round" '
            f'stroke-linejoin="round">{ICONS[name]}</svg>')


def _chrome():
    return ((ROOT / "scenes/chrome.frag.html").read_text())


def expand(fragment, uid, fmt):
    def rep(m):
        kind, arg = m.group(1), m.group(2)
        if kind == "ph": return _ph(arg, fmt)
        if kind == "icon": return _icon(arg)
        raise ValueError(m.group(0))
    fragment = fragment.replace("{{map}}", _map()).replace("{{chrome}}", _chrome())
    return re.sub(r"\{\{(\w+):([^}]+)\}\}", rep, fragment)
