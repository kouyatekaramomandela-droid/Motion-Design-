// F6 — Signature (51.4–60). The three lacks of F4 come back recoloured in gold: the well where gold water
// flows, the school lit, the health post lit. Then the gold lines settle into the tricolour band, the logo
// returns at the centre and « L'or de Kouroussa, au service de Kouroussa. » holds to 60 s.
const line = $(".wipe-line");
tl.fromTo($(".reveal"), { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.6, ease: "power2.inOut" }, at(51.6));
tl.fromTo(line, { x: -6, opacity: 1 }, { x: W, duration: 0.6, ease: "power2.inOut" }, at(51.6));
tl.set(line, { opacity: 0 }, at(52.22));

const panels = [$(".pa"), $(".pb"), $(".pc")];
tl.fromTo(panels, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out", stagger: 0.12 }, at(51.8));
camera($(".plate.pd0"), at(51.8), 3.6, [1.0, 0, 0], [1.07, 0, -6], 1.8, "none");
camera($(".plate.pd1"), at(51.8), 3.6, [1.0, 0, 0], [1.07, 0, -6], 1.8, "none");

// 1 — the well turns gold (cross-fade between the dry and the gold treatment) and gold water flows
tl.fromTo($(".gold1"), { opacity: 0 }, { opacity: 1, duration: 0.8, ease: "sine.inOut" }, at(52.4));
const pl = $(".plate.pd0"), pw = parseFloat(pl.style.width), ph = parseFloat(pl.style.height);
const px = parseFloat(pl.style.left), py = parseFloat(pl.style.top);
const cv = $("canvas.stream"), panel = $(".pa");
cv.width = panel.offsetWidth || pick(560, 940, 320); cv.height = panel.offsetHeight || pick(700, 480, 640);
const ctx = cv.getContext("2d");
const spout = { x: px + 0.642 * pw, y0: py + 0.655 * ph, y1: py + 0.80 * ph };
const S = { t: 0 };
function drawStream(t) {
  ctx.clearRect(0, 0, cv.width, cv.height);
  if (t <= 0) return;
  ctx.globalCompositeOperation = "lighter";
  const on = Math.min(1, t / 0.5);
  for (let i = 0; i < 70; i++) {
    const ph2 = (t * 1.3 + i / 70) % 1;
    const y = spout.y0 + (spout.y1 - spout.y0) * ph2 * ph2;
    const x = spout.x + Math.sin(i * 12.9898) * 3 + ph2 * 2;
    const a = on * (1 - ph2) * 0.9;
    ctx.fillStyle = `rgba(248,223,122,${a.toFixed(3)})`;
    ctx.beginPath(); ctx.arc(x, y, 2.2 + (i % 3) * 0.6, 0, 6.2832); ctx.fill();
  }
  const g = ctx.createRadialGradient(spout.x, spout.y1, 0, spout.x, spout.y1, 46);
  g.addColorStop(0, `rgba(245,197,24,${(0.55 * on).toFixed(3)})`); g.addColorStop(1, "rgba(245,197,24,0)");
  ctx.fillStyle = g; ctx.beginPath(); ctx.arc(spout.x, spout.y1, 46, 0, 6.2832); ctx.fill();
  ctx.globalCompositeOperation = "source-over";
}
tl.fromTo(S, { t: 0 }, { t: 3.2, duration: 3.2, ease: "none", onUpdate: () => drawStream(S.t) }, at(52.5));

// 2 and 3 — the school and the health post light up (ink turns gold, lights on)
[[".pb", 53.2], [".pc", 54.0]].forEach(([sel, t]) => {
  const p = $(sel), inks = Array.from(p.querySelectorAll(".ink")), lits = Array.from(p.querySelectorAll(".lit"));
  tl.fromTo(inks, { stroke: "#A9B3BC" }, { stroke: "#F8DF7A", duration: 0.5, ease: "sine.out" }, at(t));
  tl.fromTo(lits, { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "sine.out", stagger: 0.08 }, at(t + 0.1));
  tl.fromTo(p, { boxShadow: "0 0 0px rgba(245,197,24,0)" }, { boxShadow: "0 0 50px rgba(245,197,24,0.45)", duration: 0.6 }, at(t));
});
tl.fromTo($(".pa"), { boxShadow: "0 0 0px rgba(245,197,24,0)" }, { boxShadow: "0 0 50px rgba(245,197,24,0.45)", duration: 0.6 }, at(52.4));
tl.to(panels, { opacity: 0, scale: 0.94, duration: 0.6, ease: "power2.in", stagger: 0.06 }, at(55.0));

// the gold lines settle into the tricolour band at the bottom
const svg = $("svg.waves"), NS = "http://www.w3.org/2000/svg";
svg.setAttribute("width", W); svg.setAttribute("height", H); svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
const cy = H * 0.5;
const waves = [[46, 520, 0.0, "#F5C518"], [34, 430, 1.3, "#F8DF7A"], [26, 610, 2.4, "#B8860B"]].map(([amp, per, ph0, col], i) => {
  const pts = [];
  for (let k = 0; k <= W + 40; k += 20) pts.push(`${k - 20} ${(cy + (i - 1) * 40 + amp * Math.sin(2 * Math.PI * k / per + ph0)).toFixed(1)}`);
  const p = document.createElementNS(NS, "path");
  p.setAttribute("d", "M" + pts.join(" L")); p.setAttribute("fill", "none"); p.setAttribute("stroke", col);
  p.setAttribute("stroke-width", String(5 - i)); p.setAttribute("stroke-linecap", "round");
  svg.appendChild(p);
  return p;
});
prepDraw(waves);
tl.fromTo(waves, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.9, ease: "power2.out", stagger: 0.1 }, at(54.9));
const bandH = pick(20, 28, 20);
tl.fromTo(svg, { y: 0, scaleY: 1, transformOrigin: "50% 50%" }, { y: H - bandH / 2 - cy, scaleY: 0.04, duration: 0.9, ease: "power2.inOut", transformOrigin: "50% 50%" }, at(55.6));
tl.to(svg, { opacity: 0, duration: 0.3 }, at(56.4));
tl.fromTo($$(".band i"), { scaleX: 0, transformOrigin: "50% 50%" }, { scaleX: 1, duration: 0.7, ease: "power3.out", stagger: 0.12, transformOrigin: "50% 50%" }, at(56.2));
tl.fromTo($(".g6"), { opacity: 0 }, { opacity: 1, duration: 1.4 }, at(55.4));

// the logo returns at the centre (chime 55.6)
const emb = $(".emb svg");
const nug = emb.querySelector(".nugget"), rays = Array.from(emb.querySelectorAll(".ray"));
const ho = emb.querySelector(".hand-outline"), th = emb.querySelector(".hand-thumb");
prepDraw([ho, th]);
tl.fromTo(nug, { scale: 0, rotation: -20, opacity: 0, svgOrigin: "204 162" }, { scale: 1, rotation: 0, opacity: 1, duration: 0.6, ease: "back.out(2)", svgOrigin: "204 162" }, at(55.5));
tl.fromTo(ho, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 1.1, ease: "power2.inOut" }, at(55.6));
tl.fromTo(th, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.8, ease: "power2.inOut" }, at(56.0));
tl.fromTo(rays, { scale: 0.15, opacity: 0, svgOrigin: "204 162" }, { scale: 1, opacity: 1, duration: 0.6, ease: "power3.out", stagger: 0.05, svgOrigin: "204 162" }, at(56.3));
tl.fromTo($(".word"), { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.7, ease: "power3.out" }, at(56.1));
// the signature, word by word on the voice (« L'or » 55.93 … « Kouroussa. » 58.0)
const words = splitWords($(".signature"));
const times = [55.85, 56.2, 56.35, 57.15, 57.3, 57.75, 57.92];
words.forEach((w, i) => {
  tl.fromTo(w, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, at(times[Math.min(i, times.length - 1)]));
});
// final hold: one slow breath, nothing fades before 60 s
tl.fromTo($(".lockup"), { scale: 1, transformOrigin: "50% 40%" }, { scale: 1.025, duration: 3.4, ease: "none", transformOrigin: "50% 40%" }, at(56.6));
