// Scene 2 — Le territoire (9.4–28.6). Map draws, three mines pulse, camera dives, the lack is drawn in grey.
const svgMap = $(".s2-map svg");
const outline = svgMap.querySelector(".outline"), river = svgMap.querySelector(".river");
prepDraw([outline, river]);
tl.fromTo($(".s2-glow"), { opacity: 0 }, { opacity: 0.8, duration: 1.8, ease: "sine.inOut" }, at(10.0));
tl.fromTo(outline, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 2.6, ease: "power2.inOut" }, at(10.0));
tl.fromTo(river, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 1.8, ease: "power1.inOut" }, at(11.0));
tl.fromTo(svgMap.querySelector(".hatch"), { opacity: 0 }, { opacity: 0.25, duration: 1.2 }, at(11.8));
tl.fromTo($(".s2-river"), { opacity: 0 }, { opacity: 1, duration: 0.8 }, at(12.4));
tl.fromTo(svgMap.querySelector(".town rect"), { opacity: 0, scale: 0, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(3)", transformOrigin: "50% 50%" }, at(12.8));
tl.fromTo($(".s2-town"), { opacity: 0, x: -10 }, { opacity: 1, x: 0, duration: 0.6, ease: "power2.out" }, at(12.9));
const lab = $$(".s2-labels > *");
tl.fromTo(lab[0], { opacity: 0, x: 30 }, { opacity: 1, x: 0, duration: 0.8, ease: "power3.out" }, at(12.2));
tl.fromTo(lab[1], { opacity: 0, x: 30 }, { opacity: 1, x: 0, duration: 0.8, ease: "power3.out" }, at(12.5));
tl.fromTo(lab[2], { opacity: 0 }, { opacity: 1, duration: 0.01 }, at(13.9));

// three mines — chimes at 14.0 / 14.7 / 15.4 (spring-pop-entrance + pulse rings)
const mines = $$(".s2-map .mine"), rings = $$(".s2-map .ring"), dots = $$(".s2-mines i");
[14.0, 14.7, 15.4].forEach((g, i) => {
  tl.fromTo(mines[i], { scale: 0, transformOrigin: "50% 50%" }, { scale: 1, duration: 0.55, ease: "back.out(3)", transformOrigin: "50% 50%" }, at(g));
  tl.fromTo(rings[i], { scale: 0.6, opacity: 0.8, transformOrigin: "50% 50%" }, { scale: 2.6, opacity: 0, duration: 1.5, ease: "power2.out", repeat: 2, transformOrigin: "50% 50%" }, at(g));
  tl.fromTo(dots[i], { scale: 0 }, { scale: 1, duration: 0.5, ease: "back.out(3)" }, at(g));
});
tl.fromTo(lab[3], { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.9, ease: "power3.out" }, at(15.6));

// camera dives toward the villages
const townOrigin = pick("562px 449px", "517px 560px");
tl.to($$(".s2-labels, .s2-town, .s2-river"), { opacity: 0, duration: 0.5, ease: "sine.in" }, at(16.3));
tl.to($(".s2-mapgroup"), { scale: 2.4, duration: 1.6, ease: "power2.in", transformOrigin: townOrigin }, at(16.5));
tl.to($(".s2-mapgroup"), { opacity: 0, duration: 0.85, ease: "power1.in" }, at(16.5));
tl.to($(".s2-glow"), { opacity: 0.45, duration: 1.2 }, at(16.6));

// the lack: three vignettes drawn in grey on the words
const tri = $(".s2-tri");
tl.fromTo(tri, { scale: 1, transformOrigin: "50% 40%" }, { scale: 1.04, duration: 10.0, ease: "none", transformOrigin: "50% 40%" }, at(17.0));
[[".tri1", 17.0], [".tri2", 18.45], [".tri3", 19.95]].forEach(([sel, g]) => {
  const fig = $(".s2 " + sel);
  const strokes = Array.from(fig.querySelectorAll(".ink path, .ink rect, .ink circle, .ink ellipse"));
  prepDraw(strokes);
  tl.fromTo(fig, { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.6, ease: "power2.out" }, at(g));
  tl.fromTo(strokes, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 1.1, ease: "power2.out", stagger: 0.035 }, at(g));
  tl.fromTo(fig.querySelector("figcaption"), { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.8, ease: "power2.out" }, at(g + 0.6));
});
tl.to($(".s2-glow"), { scale: 1.08, duration: 2.2, ease: "sine.inOut", yoyo: true, repeat: 1 }, at(22.0));
// exit
tl.to(tri, { opacity: 0, y: -40, duration: 1.0, ease: "power2.in" }, at(26.9));
tl.to($(".s2-glow"), { opacity: 0, duration: 1.0 }, at(27.2));
