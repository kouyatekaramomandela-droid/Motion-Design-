// F3 — L'or (14.4–28.6). « Sous cette terre » : a gold line descends and opens the mine (photo C, warm
// gold grade, calm top view, machines as the near plane). « Trois mines » : the photo sinks into the dark,
// the prefecture is drawn in gold and its three mines light up with a counter. Then the hero figure.
const plate = $(".plate.c1"), sunk = $(".plate.c1s");
const line = $(".wipe-line.horz");
tl.fromTo($(".mineshot"), { clipPath: "inset(0% 0% 100% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.7, ease: "power2.inOut" }, at(14.6));
tl.fromTo(line, { y: -6, opacity: 1 }, { y: H, duration: 0.7, ease: "power2.inOut" }, at(14.6));
tl.set(line, { opacity: 0 }, at(15.32));
camera(plate, at(14.6), 13.0, [1.0, 0, 0], [1.16, 0, -10], 1.5, "none");
camera(sunk, at(14.6), 13.0, [1.0, 0, 0], [1.16, 0, -10], 1.5, "none");
tl.fromTo($(".sweep"), { x: 0 }, { x: W * 1.9, duration: 1.8, ease: "sine.inOut" }, at(16.3));

// gold dust rising from the pit
const cv = $(".mineshot canvas.dust"); cv.width = W; cv.height = H;
const ctx = cv.getContext("2d"), field = FK.makeField(pick(320, 320, 260), 31), D = { t: 0 };
tl.fromTo(D, { t: 0 }, { t: 13.6, duration: 13.6, ease: "none", onUpdate: () => FK.drawDust(ctx, field, D.t * 1.6, 0.6) }, at(14.6));

// the photo sinks into the dark under the map: cross-fade to the same grade at exposure -1.1 + blur (baked)
tl.fromTo($(".sunk"), { opacity: 0 }, { opacity: 1, duration: 1.0, ease: "sine.inOut" }, at(18.2));
tl.to($(".warm"), { opacity: 0, duration: 0.01 }, at(19.25));
tl.to($(".sunk"), { opacity: 0.62, duration: 0.8, ease: "sine.inOut" }, at(19.3));

// the prefecture, drawn in gold
const map = $(".map-box svg");
const outline = map.querySelector(".outline"), river = map.querySelector(".river");
prepDraw([outline, river]);
tl.fromTo($(".map-box"), { opacity: 0 }, { opacity: 1, duration: 0.3 }, at(18.25));
tl.fromTo(outline, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 1.0, ease: "power2.inOut" }, at(18.3));
tl.fromTo(river, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.9, ease: "power2.inOut" }, at(18.6));
tl.fromTo(map.querySelector(".hatch"), { opacity: 0 }, { opacity: 0.25, duration: 0.8 }, at(18.7));
tl.fromTo(map.querySelector(".town"), { opacity: 0 }, { opacity: 1, duration: 0.4 }, at(18.9));
// three mines, one by one (chimes at 18.9 / 19.4 / 19.9), counter 1 · 2 · 3
const M = [[186, 182], [392, 176], [366, 384]];
[18.9, 19.4, 19.9].forEach((t, i) => {
  const dot = map.querySelector(".m" + (i + 1)), ring = map.querySelector(".r" + (i + 1));
  const o = M[i][0] + " " + M[i][1];
  tl.fromTo(dot, { scale: 0, svgOrigin: o }, { scale: 1, duration: 0.45, ease: "back.out(3)", svgOrigin: o }, at(t));
  tl.fromTo(ring, { scale: 0.4, opacity: 0.9, svgOrigin: o }, { scale: 1.8, opacity: 0, duration: 1.1, ease: "power2.out", svgOrigin: o }, at(t));
  const n = $(".n" + (i + 1));
  tl.fromTo(n, { opacity: 0, y: 40, scale: 0.8, transformOrigin: "50% 60%" }, { opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(2)", transformOrigin: "50% 60%" }, at(t));
  if (i < 2) tl.to(n, { opacity: 0, y: -30, duration: 0.25, ease: "power2.in" }, at(t + 0.45));
});
tl.fromTo($(".u1"), { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.4, ease: "power2.out" }, at(18.95));
tl.to($(".u1"), { opacity: 0, duration: 0.15 }, at(19.4));
tl.fromTo($(".u2"), { opacity: 0 }, { opacity: 1, duration: 0.15 }, at(19.4));
// « 3 mines » holds 2.1 s, then gives way to the hero figure
tl.to([$(".cn"), $(".cu")], { opacity: 0, y: -40, duration: 0.4, ease: "power2.in" }, at(21.7));
tl.to($(".map-box"), { opacity: 0.55, duration: 0.6 }, at(21.8));

// hero: « plus de 2 milliards USD par an » (« deux milliards » 22.6–23.3, « chaque année » 24.0)
const num = $(".hero-num"), C = { v: 0 };
tl.fromTo($(".hero-pre"), { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, at(22.0));
tl.fromTo($(".hero-num"), { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, at(22.1));
tl.fromTo(C, { v: 0 }, { v: 2, duration: 1.2, ease: "power2.out",
  onUpdate: () => { num.textContent = C.v < 1.995 ? C.v.toFixed(1).replace(".", ",") : "2"; } }, at(22.1));
tl.fromTo($(".hero-mil"), { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }, at(22.7));
tl.fromTo($(".hero-usd"), { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, at(23.3));
tl.fromTo($(".hero-usd .per"), { opacity: 0 }, { opacity: 1, duration: 0.5 }, at(23.9));
tl.fromTo($(".hero-num"), { scale: 1, transformOrigin: "0% 70%" }, { scale: 1.06, duration: 0.25, ease: "power2.out", yoyo: true, repeat: 1, transformOrigin: "0% 70%" }, at(23.3));

// gold flows from the three mines to the figure
const flows = $("svg.flows");
flows.setAttribute("width", W); flows.setAttribute("height", H); flows.setAttribute("viewBox", `0 0 ${W} ${H}`);
const box = pick({ x: 150, y: 150, w: 660 }, { x: 140, y: 160, w: 800 }, { x: 40, y: 190, w: 500 });
const tgt = pick([862, 560], [520, 925], [548, 470]);
const k = box.w / 600, NS = "http://www.w3.org/2000/svg";
const paths = M.map(([mx, my], i) => {
  const sx = box.x + mx * k, sy = box.y + my * k;
  const p = document.createElementNS(NS, "path");
  p.setAttribute("d", `M${sx} ${sy} C${sx + (tgt[0] - sx) * 0.45} ${sy - 60 + i * 40} ${tgt[0] - 120} ${tgt[1] + (i - 1) * 50} ${tgt[0]} ${tgt[1] + (i - 1) * 24}`);
  p.setAttribute("fill", "none"); p.setAttribute("stroke", "#F5C518"); p.setAttribute("stroke-width", "4");
  p.setAttribute("stroke-linecap", "round"); p.setAttribute("stroke-dasharray", "14 12");
  flows.appendChild(p);
  return p;
});
tl.fromTo(paths, { opacity: 0 }, { opacity: 0.85, duration: 0.6, stagger: 0.12 }, at(22.2));
tl.fromTo(paths, { strokeDashoffset: 0 }, { strokeDashoffset: -260, duration: 5.0, ease: "none" }, at(22.2));

// exit: the gold lines leave by the edges, the frame goes dark (27.0–27.9)
tl.to(paths, { x: W * 0.7, opacity: 0, duration: 0.8, ease: "power2.in", stagger: 0.06 }, at(27.0));
tl.to(outline, { strokeDashoffset: -1, duration: 0.8, ease: "power2.in" }, at(27.0));
tl.to([river, map.querySelector(".hatch"), map.querySelector(".town"), map.querySelector(".mines"), map.querySelector(".mine-rings")], { opacity: 0, duration: 0.5 }, at(27.1));
tl.to($(".hero"), { opacity: 0, y: -20, filter: "blur(8px)", duration: 0.6, ease: "power2.in" }, at(27.0));
tl.to([$(".mineshot .warm"), $(".mineshot .sunk")], { opacity: 0, duration: 0.8, ease: "sine.in" }, at(27.1));
tl.to(cv, { opacity: 0, duration: 0.6 }, at(27.1));
