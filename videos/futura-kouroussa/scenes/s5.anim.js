// Scene 5 — La naissance (57.4–75.6). The point becomes the nugget, the open hand draws itself to receive it.
const emb = $(".s5-emblem svg");
const nug = emb.querySelector(".nugget"), rays = Array.from(emb.querySelectorAll(".ray"));
const handOutline = emb.querySelector(".hand-outline"), thumb = emb.querySelector(".hand-thumb");
prepDraw([handOutline, thumb]);
// floating position of the nugget before it lands (60 svg units above its seat)
const seat = pick({ x: 486, y: 411 }, { x: 546, y: 431 });
const float = { x: seat.x, y: seat.y - 93 };
const start = pick({ x: 960, y: 470 }, { x: 540, y: 650 });
tl.fromTo($(".s5 .lattice"), { opacity: 0 }, { opacity: 0.1, duration: 1.4 }, at(57.8));
const seed = $(".s5-seed");
tl.fromTo(seed, { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.5, ease: "power2.out" }, at(57.6));
tl.fromTo(seed, { x: 0, y: 0 }, { x: float.x - start.x, y: float.y - start.y, duration: 0.6, ease: "power2.in" }, at(58.0));
tl.to(seed, { scale: 2.2, opacity: 0, duration: 0.35, ease: "power2.out" }, at(58.6));

// particle-burst: fixed pool, index-seeded, pure function of time
const sparks = $(".s5-sparks");
const N = 34;
for (let i = 0; i < N; i++) {
  const s = document.createElement("i");
  s.style.left = float.x + "px"; s.style.top = float.y + "px";
  sparks.appendChild(s);
  const a = (i / N) * Math.PI * 2 + ((i * 7919) % 13) * 0.02;
  const r = 150 + ((i * 37) % 110);
  tl.fromTo(s, { x: 0, y: 0, scale: 1 }, { x: Math.cos(a) * r, y: Math.sin(a) * r * 0.85, scale: 0.3, duration: 1.3, ease: "power3.out" }, at(58.6));
  tl.fromTo(s, { opacity: 0 }, { opacity: 1, duration: 0.08 }, at(58.6));
  tl.to(s, { opacity: 0, duration: 1.0, ease: "power1.in" }, at(58.85));
}
tl.fromTo($(".s5-glow"), { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 1.4, ease: "power2.out" }, at(58.6));

// the nugget crystallises, floats, then lands in the hand (chime 61.0)
tl.fromTo(nug, { scale: 0, rotation: -25, y: -60, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, rotation: 0, y: -60, opacity: 1, duration: 0.8, ease: "back.out(2)", transformOrigin: "50% 50%" }, at(58.65));
tl.fromTo(handOutline, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 1.8, ease: "power2.inOut" }, at(58.9));
tl.fromTo(thumb, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 1.0, ease: "power2.inOut" }, at(59.7));
tl.to(nug, { y: 0, duration: 0.8, ease: "power2.in" }, at(60.2));
tl.to(nug, { y: -6, duration: 0.16, ease: "power1.out", yoyo: true, repeat: 1 }, at(61.0));
rays.forEach((r, i) => {
  const order = [0, 1, 2, 3, 4][i];
  tl.fromTo(r, { scale: 0.15, opacity: 0, svgOrigin: "204 162" }, { scale: 1, opacity: 1, duration: 0.6, ease: "power3.out", svgOrigin: "204 162" }, at(61.0 + Math.abs(order - 0) * 0.05));
});
tl.to(rays, { opacity: 0.72, duration: 0.9, ease: "sine.inOut", yoyo: true, repeat: 3, stagger: 0.12 }, at(67.6));
tl.to($(".s5-glow"), { scale: 1.08, duration: 1.6, ease: "sine.inOut", yoyo: true, repeat: 3 }, at(62.0));

// name, letter by letter, on « Futura Kouroussa » (59.5)
const wordChars = splitChars($(".s5-word"), true);
tl.fromTo(wordChars, { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out", stagger: 0.045 }, at(59.5));
const nameChars = splitChars($(".s5-name"), false);
tl.fromTo(nameChars, { opacity: 0 }, { opacity: 1, duration: 0.25, ease: "none", stagger: 0.02 }, at(61.6));
// badges on « OHADA » (64.4) and « né du rapport » (65.4)
const org = H_ ? "0% 50%" : "50% 50%";
tl.fromTo($(".badge.b1"), { opacity: 0, scale: 0.7, transformOrigin: org }, { opacity: 1, scale: 1, duration: 0.6, ease: "back.out(2.2)", transformOrigin: org }, at(64.4));
tl.fromTo($(".badge.b2"), { opacity: 0, scale: 0.7, transformOrigin: org }, { opacity: 1, scale: 1, duration: 0.6, ease: "back.out(2.2)", transformOrigin: org }, at(65.4));

// « centraliser et redistribuer… de manière traçable » (68.2–71.8)
const trace = $("svg.s5-trace");
const tNodes = Array.from(trace.querySelectorAll(".node")), movers = Array.from(trace.querySelectorAll(".mover"));
const nodeXY = tNodes.map((n) => [+n.getAttribute("cx"), +n.getAttribute("cy")]);
tl.fromTo(trace, { opacity: 0, rotation: -20 }, { opacity: 0.85, rotation: 0, duration: 1.2, ease: "power2.out" }, at(67.3));
tl.fromTo(tNodes, { scale: 0, transformOrigin: "50% 50%" }, { scale: 1, duration: 0.4, ease: "back.out(3)", stagger: 0.08, transformOrigin: "50% 50%" }, at(67.7));
movers.forEach((m, i) => {
  const [x, y] = nodeXY[i];
  tl.fromTo(m, { attr: { cx: x, cy: y }, opacity: 0 }, { attr: { cx: x, cy: y }, opacity: 1, duration: 0.2 }, at(68.1));
  tl.to(m, { attr: { cx: 0, cy: 0 }, duration: 0.7, ease: "power2.in" }, at(68.2 + i * 0.04));
  tl.to(m, { attr: { cx: x, cy: y }, duration: 0.8, ease: "power2.out" }, at(69.3 + i * 0.04));
  tl.to(m, { opacity: 0, duration: 0.3 }, at(70.3));
});
tl.to(nug, { scale: 1.1, duration: 0.18, ease: "power2.out", yoyo: true, repeat: 1, transformOrigin: "50% 50%" }, at(68.95));
tl.to(tNodes, { scale: 1.45, duration: 0.25, ease: "power2.out", yoyo: true, repeat: 1, stagger: 0.04, transformOrigin: "50% 50%" }, at(70.0));
tl.fromTo(trace.querySelector(".trace-ring"), { strokeDashoffset: 0 }, { strokeDashoffset: -230, duration: 6.0, ease: "none" }, at(67.4));
tl.to(trace, { opacity: 0, duration: 0.6, ease: "power2.in" }, at(73.4));

// exit: the text clears, the nugget glides to the heart of the governance ring
tl.to($$(".s5-text > *"), { opacity: 0, y: -16, duration: 0.6, ease: "power2.in", stagger: 0.1 }, at(73.4));
tl.to([handOutline, thumb], { opacity: 0, duration: 0.6 }, at(73.8));
tl.to(rays, { opacity: 0, scale: 0.4, duration: 0.6, ease: "power2.in", svgOrigin: "204 162" }, at(73.8));
const ring = pick({ x: 560, y: 490, s: 0.586 }, { x: 540, y: 560, s: 0.66 });
tl.to($(".s5-emblem"), { x: ring.x - seat.x, y: ring.y - seat.y, scale: ring.s, duration: 1.2, ease: "power2.inOut", transformOrigin: "316.2px 251.1px" }, at(74.0));
tl.to($(".s5-glow"), { opacity: 0, duration: 0.8 }, at(74.4));
tl.to($(".s5 .lattice"), { opacity: 0, duration: 0.8 }, at(74.6));
tl.to($(".s5-emblem"), { opacity: 0, duration: 0.3 }, at(75.25));
