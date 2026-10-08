// Scene 7 — Les résultats attendus (94.4–110.6). The scene-2 vignettes return and light up; the dashboard rises.
const figs = [1, 2, 3].map((i) => $(".s7 .tri" + i));
// start exactly where scene 2 left them, then settle into the dashboard layout
const from = H_
  ? [{ x: 120 - 210, y: 120, scale: 1.3 }, { x: 700 - 760, y: 120, scale: 1.3 }, { x: 1280 - 1310, y: 120, scale: 1.3 }]
  : [{ x: 0, y: 20, scale: 1.2 }, { x: 0, y: 75, scale: 1.2 }, { x: 0, y: 130, scale: 1.2 }];
const inks = figs.map((f) => Array.from(f.querySelectorAll(".ink")));
const caps = figs.map((f) => f.querySelector("figcaption"));
figs.forEach((f, i) => {
  tl.fromTo(f, { x: from[i].x, y: from[i].y, scale: from[i].scale, opacity: 0, transformOrigin: "0% 0%" }, { x: from[i].x, y: from[i].y, scale: from[i].scale, opacity: 1, duration: 0.8, ease: "sine.out", transformOrigin: "0% 0%" }, at(95.0));
  tl.fromTo(inks[i], { stroke: "#A9B3BC" }, { stroke: "#A9B3BC", duration: 0.01 }, 0);
  tl.fromTo(caps[i], { color: "#A9B3BC" }, { color: "#A9B3BC", duration: 0.01 }, 0);
});
tl.fromTo($(".s7-glow"), { opacity: 0 }, { opacity: 0.9, duration: 1.4 }, at(95.6));

// the drop that fell from the ring lands in the pump
const dropY = pick(388, 327);
tl.fromTo($(".s7-drop"), { y: 0, opacity: 0, rotation: -45 }, { y: dropY + 40, opacity: 1, rotation: -45, duration: 1.0, ease: "power2.in" }, at(95.4));
tl.to($(".s7-drop"), { opacity: 0, scale: 0.4, duration: 0.25 }, at(96.4));

function light(i, g) {
  tl.to(inks[i], { stroke: "#F8DF7A", duration: 0.6, ease: "sine.inOut" }, at(g));
  tl.to(caps[i], { color: "#F5C518", duration: 0.6 }, at(g + 0.1));
}
// « De l'eau » 96.6
const f1 = figs[0];
light(0, 96.6);
tl.fromTo(f1.querySelector(".lit.water"), { opacity: 0 }, { opacity: 1, duration: 0.2 }, at(96.6));
tl.fromTo(f1.querySelector(".stream"), { scaleY: 0, transformOrigin: "50% 0%" }, { scaleY: 1, duration: 0.5, ease: "power2.in", transformOrigin: "50% 0%" }, at(96.6));
tl.fromTo(f1.querySelector(".fill"), { scaleX: 0.2, opacity: 0, transformOrigin: "50% 50%" }, { scaleX: 1, opacity: 1, duration: 0.6, ease: "power2.out", transformOrigin: "50% 50%" }, at(97.0));
Array.from(f1.querySelectorAll(".drop")).forEach((d, k) => {
  tl.fromTo(d, { y: -26, opacity: 0 }, { y: 6, opacity: 1, duration: 0.55, ease: "power1.in", repeat: 6, repeatDelay: 0.25 }, at(96.9 + k * 0.27));
});
// « des écoles » 97.35
const f2 = figs[1];
light(1, 97.35);
const chalk = Array.from(f2.querySelectorAll(".chalk path"));
prepDraw(chalk);
tl.fromTo(f2.querySelector(".chalk"), { opacity: 0 }, { opacity: 1, duration: 0.1 }, at(97.35));
tl.fromTo(chalk, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.5, ease: "power2.out", stagger: 0.15 }, at(97.4));
tl.fromTo(f2.querySelector(".kit"), { opacity: 0 }, { opacity: 1, duration: 0.1 }, at(97.5));
tl.fromTo(Array.from(f2.querySelector(".kit").children), { scale: 0, transformOrigin: "50% 100%" }, { scale: 1, duration: 0.45, ease: "back.out(2.4)", stagger: 0.08, transformOrigin: "50% 100%" }, at(97.5));
tl.to(f2.querySelector(".arm-down"), { opacity: 0, duration: 0.2 }, at(97.9));
tl.fromTo(f2.querySelector(".arm-up"), { opacity: 0, rotation: 50, svgOrigin: "134 194" }, { opacity: 1, rotation: 0, duration: 0.5, ease: "back.out(2)", svgOrigin: "134 194" }, at(97.9));
// « des soins » 98.35
const f3 = figs[2];
light(2, 98.35);
tl.fromTo(f3.querySelector(".solar"), { opacity: 0, y: -14 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, at(98.35));
tl.fromTo(f3.querySelector(".lit.light"), { opacity: 0 }, { opacity: 1, duration: 0.3 }, at(98.4));
tl.fromTo(f3.querySelector(".halo"), { scale: 0, svgOrigin: "160 212" }, { scale: 1, duration: 0.6, ease: "back.out(2)", svgOrigin: "160 212" }, at(98.4));
tl.to(f3.querySelector(".halo"), { scale: 1.18, duration: 0.8, ease: "sine.inOut", yoyo: true, repeat: 5, svgOrigin: "160 212" }, at(99.1));

// the vignettes rise, the dashboard slides in beneath (no values, only trends)
figs.forEach((f) => tl.to(f, { x: 0, y: 0, scale: 1, duration: 1.4, ease: "power2.inOut", transformOrigin: "0% 0%" }, at(101.0)));
tl.fromTo($(".s7-dash"), { opacity: 0, y: 80 }, { opacity: 1, y: 0, duration: 0.9, ease: "power3.out" }, at(101.6));
tl.fromTo($(".s7 .chip"), { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2.4)" }, at(102.2));
tl.fromTo($$(".s7 .kpi .lab"), { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.5, stagger: 0.15 }, at(102.0));
const sl = $$(".s7 .spark .line");
prepDraw(sl);
tl.fromTo(sl, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 1.2, ease: "power2.out", stagger: 0.3 }, at(102.3));
tl.fromTo($$(".s7 .spark .area"), { opacity: 0 }, { opacity: 0.14, duration: 0.8, stagger: 0.3 }, at(102.7));
tl.fromTo($$(".s7 .spark .arrow"), { opacity: 0, scale: 0.4, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(3)", stagger: 0.3, transformOrigin: "50% 50%" }, at(103.3));
tl.fromTo($(".s7-title .t1"), { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }, at(103.6));
tl.fromTo($(".s7-title .t2"), { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }, at(104.2));
// living hold under the title (105–108.6)
tl.to($(".s7 .chip"), { scale: 1.07, duration: 0.6, ease: "sine.inOut", yoyo: true, repeat: 3 }, at(105.0));
tl.to($$(".s7 .spark .arrow"), { y: -5, duration: 0.5, ease: "sine.inOut", yoyo: true, repeat: 5, stagger: 0.2 }, at(104.8));
tl.fromTo($(".s7-glow"), { scale: 1 }, { scale: 1.1, duration: 3.2, ease: "sine.inOut" }, at(104.6));
// exit
tl.to($$(".s7-dash, .s7-title"), { opacity: 0, duration: 0.8, ease: "power2.in" }, at(108.6));
tl.to($(".s7-tri"), { opacity: 0, y: -30, duration: 0.8, ease: "power2.in" }, at(108.9));
tl.to($(".s7-glow"), { opacity: 0, duration: 1.0 }, at(109.0));
