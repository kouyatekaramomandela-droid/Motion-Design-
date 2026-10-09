"""Kouroussa prefecture map for scene S2 (and its 9:16 variant).

Boundaries: geoBoundaries gbOpen GIN ADM2/ADM3 (source: World Food Programme, OCHA ROWCA;
CC BY 3.0 IGO). That division predates the 2021 sub-prefectures, so Fadoussaba and Kouroukoro are
placed from their chef-lieu coordinates (OpenStreetMap via Mapcarta, fr.wikipedia). No source gives a
position for Kanséréya: at the client's request (« placer arbitrairement ») it sits at an indicative spot
in an empty part of the map — say so in the delivery report.
Other sub-prefectures: centroid of their territory. Commune urbaine: the town of Kouroussa.

Usage: python tools/make_map.py <dir with gin-ADM2.geojson and gin-ADM3.geojson>
Writes assets/geo/kouroussa-adm3.geojson (subset, for the record), assets/map/map.svg, assets/map/points.json
"""
import json, math, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
geo = Path(sys.argv[1])
adm2 = json.loads((geo / "gin-ADM2.geojson").read_text())
adm3 = json.loads((geo / "gin-ADM3.geojson").read_text())

def rings(g):
    return [g["coordinates"][0]] if g["type"] == "Polygon" else [p[0] for p in g["coordinates"]]

def inside(pt, ring):
    x, y = pt; c = False
    for i in range(len(ring)):
        x1, y1 = ring[i]; x2, y2 = ring[(i + 1) % len(ring)]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c

def centroid(ring):
    a = cx = cy = 0.0
    for i in range(len(ring) - 1):
        x1, y1 = ring[i]; x2, y2 = ring[i + 1]
        f = x1 * y2 - x2 * y1; a += f; cx += (x1 + x2) * f; cy += (y1 + y2) * f
    return cx / (3 * a), cy / (3 * a), abs(a / 2)

pref = next(f for f in adm2["features"] if f["properties"]["shapeName"].lower().startswith("kouroussa"))
outline = max(rings(pref["geometry"]), key=lambda r: centroid(r)[2])
units = []
for f in adm3["features"]:
    big = max(rings(f["geometry"]), key=lambda r: centroid(r)[2])
    cx, cy, _ = centroid(big)
    if inside((cx, cy), outline):
        units.append((f["properties"]["shapeName"], big, (cx, cy), f))
(ROOT / "assets/geo/kouroussa-adm3.geojson").write_text(json.dumps(
    {"type": "FeatureCollection", "source": "geoBoundaries gbOpen GIN ADM3 (WFP, OCHA ROWCA), CC BY 3.0 IGO",
     "features": [u[3] for u in units]}))

DATA = {u[0]: u[2] for u in units}
# report order (Rapport de mission, « Localités visitées »)
POINTS = [
    ("Kouroussa", "Commune urbaine", (-9.8833, 10.65), "town"),
    ("Babila", "", DATA["Babila"], "centroid"),
    ("Balato", "", DATA["Balato"], "centroid"),
    ("Banfélè", "", DATA["Banfele"], "centroid"),
    ("Baro", "", DATA["Baro"], "centroid"),
    ("Fadoussaba", "", (-10.5286, 10.9975), "town"),
    ("Cissela", "", DATA["Cissela"], "centroid"),
    ("Douako", "", DATA["Douako"], "centroid"),
    ("Doura", "", DATA["Doura"], "centroid"),
    ("Kanséréya", "", (-10.33, 10.60), "indicative"),
    ("Kiniéro", "", DATA["Kiniero"], "centroid"),
    ("Komola", "", DATA["Komola Khoura"], "centroid"),
    ("Koumana", "", DATA["Koumana"], "centroid"),
    ("Kouroukoro", "", (-10.75, 10.92), "town"),
    ("Sanguiana", "", DATA["Sanguiana"], "centroid"),
]
for name, _, ll, kind in POINTS:
    if ll and not inside(ll, outline):
        raise SystemExit(f"{name} {ll} falls outside the prefecture outline")

# equirectangular projection around the prefecture, 1 unit = 1 px at the drawing size
xs = [p[0] for p in outline]; ys = [p[1] for p in outline]
lat0 = (min(ys) + max(ys)) / 2; kx = math.cos(math.radians(lat0))
H = 1000.0
s = H / (max(ys) - min(ys)); W = (max(xs) - min(xs)) * kx * s
proj = lambda p: (round((p[0] - min(xs)) * kx * s, 1), round((max(ys) - p[1]) * s, 1))
path = lambda r: "M" + " L".join(f"{x} {y}" for x, y in map(proj, r)) + " Z"

svg = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}">']
svg.append('<g class="units">' + "".join(f'<path d="{path(u[1])}"/>' for u in units) + "</g>")
svg.append(f'<path class="outline" d="{path(outline)}"/>')
svg.append("</svg>")
(ROOT / "assets/map/map.svg").write_text("\n".join(svg) + "\n")
pts = []
for i, (name, sub, ll, kind) in enumerate(POINTS):
    x, y = proj(ll) if ll else (None, None)
    pts.append({"i": i + 1, "name": name, "sub": sub, "x": x, "y": y, "kind": kind,
                "lonlat": [round(ll[0], 4), round(ll[1], 4)] if ll else None})
(ROOT / "assets/map/points.json").write_text(json.dumps({"w": round(W), "h": round(H), "points": pts}, ensure_ascii=False, indent=1) + "\n")
print(f"map {W:.0f}x{H:.0f}, units {len(units)}, points on map {sum(1 for p in pts if p['x'] is not None)}")
