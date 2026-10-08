// F5 — La réponse (37.4–52.6). The gold lines come back from the edges and draw the logo on
// « Futura Kouroussa » (41.5); the two badges; then the meeting photo as a soft background and the
// three guarantees, each lit on its word: « suivie » 46.98, « audités » 48.6, « communautés » 49.84
// (the background turns to the elders' assembly on that last one).
const L = pick({ top: 90, w: 380 }, { top: 250, w: 560 }, { top: 56, w: 300 });
const cx = W / 2 + (204 - 200) / 400 * L.w, cy = L.top + 162 / 400 * L.w;

// the lines return over the question of F4, then the night settles behind them
const svg = $("svg.converge"), NS = "http://www.w3.org/2000/svg";
svg.setAttribute("width", W); svg.setAttribute("height", H); svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
const starts = [[-20, H * 0.18], [W + 20, H * 0.32], [-20, H * 0.78], [W + 20, H * 0.86]];
const backs = starts.map(([sx, sy], i) => {
  const p = document.createElementNS(NS, "path");
  p.setAttribute("d", `M${sx} ${sy} C${sx + (cx - sx) * 0.55} ${sy} ${cx + (sx < cx ? -1 : 1) * W * 0.12} ${cy + (sy - cy) * 0.35} ${cx} ${cy}`);
  p.setAttribute("fill", "none"); p.setAttribute("stroke", i % 2 ? "#F8DF7A" : "#F5C518");
  p.setAttribute("stroke-width", "4"); p.setAttribute("stroke-linecap", "round");
  svg.appendChild(p);
  return p;
});
prepDraw(backs);
tl.fromTo(backs, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 1.3, ease: "power2.inOut", stagger: 0.1 }, at(37.5));
tl.to(backs, { strokeDashoffset: -1, duration: 0.7, ease: "power2.in", stagger: 0.05 }, at(39.0));
tl.fromTo($(".base"), { opacity: 0 }, { opacity: 1, duration: 0.6, ease: "sine.inOut" }, at(38.2));

// the logo: nugget (39.0), hand (39.2–40.8), rays (40.9–41.5), wordmark on « Futura Kouroussa »
const emb = $(".emb svg");
const nug = emb.querySelector(".nugget"), rays = Array.from(emb.querySelectorAll(".ray"));
const ho = emb.querySelector(".hand-outline"), th = emb.querySelector(".hand-thumb");
prepDraw([ho, th]);
tl.fromTo(nug, { scale: 0, rotation: -20, opacity: 0, svgOrigin: "204 162" }, { scale: 1, rotation: 0, opacity: 1, duration: 0.7, ease: "back.out(2)", svgOrigin: "204 162" }, at(39.0));
tl.fromTo(ho, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 1.5, ease: "power2.inOut" }, at(39.2));
tl.fromTo(th, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 1.0, ease: "power2.inOut" }, at(39.8));
tl.fromTo(rays, { scale: 0.15, opacity: 0, svgOrigin: "204 162" }, { scale: 1, opacity: 1, duration: 0.6, ease: "power3.out", stagger: 0.05, svgOrigin: "204 162" }, at(40.9));
tl.fromTo($(".word"), { opacity: 0, y: 28 }, { opacity: 1, y: 0, duration: 0.7, ease: "power3.out" }, at(41.4));
// badges: « mission parlementaire » (39.6) and the legal form (42.6); both hold to 44.6
tl.fromTo($(".b1"), { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, at(39.7));
tl.fromTo($(".b2"), { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, at(42.6));
tl.to($(".badges"), { opacity: 0, y: 20, duration: 0.5, ease: "power2.in" }, at(44.6));

// the lockup rises to the top, the meeting photo comes in soft behind (blurred grade, slow drift)
tl.to($(".lockup"), { ...pick({ scale: 0.5, y: -50 }, { scale: 0.45, y: -110 }, { scale: 0.55, y: -26 }), transformOrigin: "50% 0%", duration: 0.9, ease: "power2.inOut" }, at(44.6));
tl.fromTo($(".office"), { opacity: 0 }, { opacity: 1, duration: 1.0, ease: "sine.inOut" }, at(44.6));
camera($(".plate.r1"), at(44.6), 8.0, [1.02, 20, 0], [1.08, -20, 0], 1.8, "none");
// « et où les communautés ont leur mot à dire » : the elders' assembly takes over the background
tl.fromTo($(".elders"), { opacity: 0 }, { opacity: 1, duration: 0.8, ease: "sine.inOut" }, at(49.5));
camera($(".plate.r2"), at(49.5), 3.1, [1.02, 0, 0], [1.06, 0, -6], 1.0, "none");

// the three guarantees: dim first, then lit on their word
const cards = [$(".k1"), $(".k2"), $(".k3")];
tl.fromTo(cards, { opacity: 0, y: 30 }, { opacity: 0.45, y: 0, duration: 0.6, ease: "power2.out", stagger: 0.12 }, at(45.2));
[46.95, 48.55, 49.8].forEach((t, i) => {
  const c = cards[i], icon = c.querySelector(".ic svg");
  const strokes = Array.from(icon.querySelectorAll(".ic-a, .ic-b"));
  prepDraw(strokes);
  tl.set(strokes, { strokeDashoffset: 0 }, at(45.2));
  tl.to(c, { opacity: 1, duration: 0.3 }, at(t));
  tl.fromTo(icon, { stroke: "#A9B3BC" }, { stroke: "#F5C518", duration: 0.3 }, at(t));
  tl.fromTo(strokes, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.6, ease: "power2.out", stagger: 0.1 }, at(t));
  tl.fromTo(c.querySelector(".ic"), { scale: 1, boxShadow: "0 0 0px rgba(245,197,24,0)" },
    { scale: 1.12, boxShadow: "0 0 60px rgba(245,197,24,0.55)", duration: 0.25, ease: "power2.out", yoyo: true, repeat: 1 }, at(t));
});

// exit to the signature
tl.to([$(".cards"), $(".lockup")], { opacity: 0, duration: 0.5, ease: "sine.in" }, at(51.9));
