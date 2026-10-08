"""Shared fragment expansion for FUTURA-Kouroussa scenes (sketch pages and compositions)."""
import math, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ILL = ROOT / "assets" / "illustrations"
LOGO = ROOT / "assets" / "logo" / "emblem-negative.svg"

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

def _arc(r0, r1, a0, a1):
    def pt(r, a): return f"{r * math.cos(a):.2f} {r * math.sin(a):.2f}"
    large = 1 if (a1 - a0) > math.pi else 0
    return (f"M{pt(r1, a0)} A{r1} {r1} 0 {large} 1 {pt(r1, a1)} L{pt(r0, a1)} "
            f"A{r0} {r0} 0 {large} 0 {pt(r0, a0)} Z")

COLLEGES = [(40, "#F5C518", "Collectivités locales"), (25, "#F8DF7A", "Société civile"),
            (25, "#B8860B", "Partenaires institutionnels"), (10, "#A9B3BC", "Partenaires miniers")]
CTL_R = [300, 350, 400]
GATE_ANGLE = -math.pi / 6  # token leaves the core up-right

def _ring(uid):
    parts = ['<svg class="s6-ring" viewBox="-440 -440 880 880" fill="none">']
    parts.append('<g class="ctl-rings">')
    for i, r in enumerate(CTL_R):
        parts.append(f'<circle class="ctl c{i+1}" r="{r}" stroke="#B8860B" stroke-width="3" stroke-dasharray="4 10" opacity="0.7"/>')
        parts.append(f'<circle class="ctl-on c{i+1}" r="{r}" stroke="#F5C518" stroke-width="4"/>')
    parts.append('</g><circle class="halo-ring" r="233" stroke="#F5C518" stroke-width="66" transform="rotate(-90)"/><g class="gates">')
    for i, r in enumerate(CTL_R):
        x, y = r * math.cos(GATE_ANGLE), r * math.sin(GATE_ANGLE)
        parts.append(f'<g class="gate g{i+1}" transform="translate({x:.1f} {y:.1f})"><circle r="17" fill="#1A2A3A" stroke="#F5C518" stroke-width="3"/>'
                     f'<path class="tick" d="M-8 0 L-2 7 L9 -7" stroke="#F5C518" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></g>')
    parts.append('</g><g class="arcs">')
    a = -math.pi / 2; gap = math.radians(1.6)
    for i, (pct, col, _) in enumerate(COLLEGES):
        sweep = 2 * math.pi * pct / 100
        parts.append(f'<path class="arc a{i+1}" d="{_arc(200, 266, a + gap, a + sweep - gap)}" fill="{col}"/>')
        mid = a + sweep / 2
        tx, ty = 233 * math.cos(mid), 233 * math.sin(mid)
        parts.append(f'<text class="arc-pct p{i+1}" x="{tx:.1f}" y="{ty:.1f}" text-anchor="middle" dominant-baseline="central" '
                     f'font-family="Montserrat" font-weight="700" font-size="28" fill="#1A2A3A">{pct}&#8239;%</text>')
        a += sweep
    parts.append('</g>')
    # core: the nugget of the logo, recentred
    core = re.search(r'<g class="nugget">.*?</g>', LOGO.read_text(), re.S).group(0)
    parts.append(f'<g class="core" transform="translate(-204 -162) scale(1)"><circle cx="204" cy="162" r="120" fill="#F5C518" opacity="0.10"/>{core}</g>')
    tx, ty = 120 * math.cos(GATE_ANGLE), 120 * math.sin(GATE_ANGLE)
    parts.append(f'<path class="token-path" d="M{tx:.1f} {ty:.1f} L{440*math.cos(GATE_ANGLE):.1f} {440*math.sin(GATE_ANGLE):.1f}" stroke="#F5C518" stroke-width="2" stroke-dasharray="2 12" opacity="0.6"/>')
    parts.append(f'<circle class="token" cx="{tx:.1f}" cy="{ty:.1f}" r="13" fill="#F8DF7A"/>')
    parts.append('</svg>')
    return "".join(parts)

ICONS = {
    "board": '<svg viewBox="0 0 40 40" width="40" height="40" fill="none" stroke="#F5C518" stroke-width="3" stroke-linecap="round"><ellipse cx="20" cy="21" rx="11" ry="7"/><circle cx="7" cy="12" r="3"/><circle cx="33" cy="12" r="3"/><circle cx="20" cy="7" r="3"/><circle cx="20" cy="35" r="3"/></svg>',
    "audit": '<svg viewBox="0 0 40 40" width="40" height="40" fill="none" stroke="#F5C518" stroke-width="3" stroke-linecap="round"><circle cx="17" cy="17" r="10"/><path d="M25 25 L35 35"/><path d="M12 17 L16 21 L23 13"/></svg>',
    "ledger": '<svg viewBox="0 0 40 40" width="40" height="40" fill="none" stroke="#F5C518" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><rect x="7" y="5" width="26" height="30" rx="3"/><path d="M13 13 H27 M13 19 H27 M13 25 H21"/></svg>',
}

SPARKS = {
    1: [(0, 118), (40, 112), (80, 104), (120, 96), (160, 78), (200, 70), (240, 48), (280, 34)],
    2: [(0, 124), (40, 120), (80, 106), (120, 100), (160, 84), (200, 66), (240, 58), (280, 38)],
    3: [(0, 120), (40, 116), (80, 108), (120, 88), (160, 82), (200, 62), (240, 50), (280, 30)],
}

def _spark(n, uid):
    pts = SPARKS[n]
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    area = d + f" L{pts[-1][0]} 140 L0 140 Z"
    ex, ey = pts[-1]
    return (f'<svg class="spark sp{n}" viewBox="0 0 300 150" preserveAspectRatio="none" fill="none">'
            f'<path class="grid" d="M0 140 H300 M0 95 H300 M0 50 H300" stroke="#A9B3BC" stroke-width="1" opacity="0.25"/>'
            f'<path class="area" d="{area}" fill="#F5C518" opacity="0.14"/>'
            f'<path class="line" d="{d}" stroke="#F5C518" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path class="arrow" d="M{ex-14} {ey+4} L{ex+4} {ey-6} L{ex-6} {ey+14}" stroke="#F8DF7A" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
            f'</svg>')

def _lines(which, uid):
    out = []
    if which == "s3":
        for fmt, (w, h), mines, end_y, x0, x1 in (
            ("h", (1920, 1080), [(240.2, 377.4), (384.4, 373.2), (366.2, 518.8)], [548, 556, 566], 300, 1780),
            ("v", (1080, 1920), [(253.6, 309.9), (445.9, 304.3), (421.6, 498.4)], [996, 1006, 1016], 260, 1040)):
            gid = f"{uid}-fade-{fmt}"
            s = [f'<svg class="s3-lines only-{fmt}" viewBox="0 0 {w} {h}" fill="none"><defs><linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x0}" y1="0" x2="{x1}" y2="0">'
                 f'<stop offset="0" stop-color="#F5C518" stop-opacity="1"/><stop offset="0.55" stop-color="#F5C518" stop-opacity="0.45"/><stop offset="1" stop-color="#F5C518" stop-opacity="0"/></linearGradient></defs>']
            for i, ((mx, my), ey) in enumerate(zip(mines, end_y)):
                c1x, c1y = mx + (w - mx) * 0.3, my - 120 + i * 60
                c2x, c2y = mx + (w - mx) * 0.65, ey + 40 - i * 30
                s.append(f'<path class="flow f{i+1}" d="M{mx} {my} C{c1x:.0f} {c1y:.0f} {c2x:.0f} {c2y:.0f} {w + 10} {ey}" stroke="url(#{gid})" stroke-width="4" stroke-dasharray="14 12"/>')
            s.append('</svg>')
            out.append("".join(s))
    if which == "s4":
        for fmt, (w, h), center, starts in (
            ("h", (1920, 1080), (960, 470), [(1940, 300), (1940, 560), (1940, 820), (1940, 120)]),
            ("v", (1080, 1920), (540, 650), [(1100, 380), (1100, 900), (1100, 1400), (1100, 160)])):
            cx, cy = center
            s = [f'<svg class="s4-converge only-{fmt}" viewBox="0 0 {w} {h}" fill="none">']
            for i, (sx, sy) in enumerate(starts):
                s.append(f'<path class="back b{i+1}" d="M{sx} {sy} C{sx - 380} {sy} {cx + 320} {cy + (sy - cy) * 0.35:.0f} {cx} {cy}" stroke="#F5C518" stroke-width="4" stroke-linecap="round"/>')
            s.append(f'<circle class="focus" cx="{cx}" cy="{cy}" r="10" fill="#F8DF7A"/><circle class="focus-halo" cx="{cx}" cy="{cy}" r="46" fill="#F5C518" opacity="0.25"/></svg>')
            out.append("".join(s))
    return "".join(out)

def _waves(uid):
    out = []
    for fmt, (w, h), cy in (("h", (1920, 1080), 540), ("v", (1080, 1920), 960)):
        s = [f'<svg class="s8-waves only-{fmt}" viewBox="0 0 {w} {h}" fill="none">']
        for i, (amp, per, ph, col) in enumerate(((46, 520, 0.0, "#F5C518"), (34, 430, 1.3, "#F8DF7A"), (26, 610, 2.4, "#B8860B"))):
            pts = []
            for k in range(0, w + 41, 20):
                y = cy + (i - 1) * 40 + amp * math.sin(2 * math.pi * k / per + ph)
                pts.append(f"{k - 20} {y:.1f}")
            s.append(f'<path class="wave w{i+1}" d="M{" L".join(pts)}" stroke="{col}" stroke-width="{5 - i}" stroke-linecap="round"/>')
        s.append("</svg>")
        out.append("".join(s))
    return "".join(out)

def expand(fragment, uid):
    def rep(m):
        kind, arg = m.group(1), m.group(2)
        if kind == "svg": return _svg(arg, f"{uid}-{arg}")
        if kind == "ring": return _ring(uid)
        if kind == "icon": return ICONS[arg]
        if kind == "spark": return _spark(int(arg), uid)
        if kind == "lines": return _lines(arg, uid)
        if kind == "waves": return _waves(uid)
        raise ValueError(m.group(0))
    return re.sub(r"\{\{(\w+):(\w+)\}\}", rep, fragment)
