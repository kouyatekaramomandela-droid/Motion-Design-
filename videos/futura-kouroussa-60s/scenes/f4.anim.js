// F4 — Le contraste (27.4–38.6). No more gold lines. The village well (photo D, soft community grade)
// loses its colour while « l'eau potable manque encore » is said; then the school and the health post,
// drawn in grey; the question « Et les communautés ? » holds to the end of the scene.
const well = $(".well");
tl.fromTo(well, { opacity: 0 }, { opacity: 1, duration: 0.8, ease: "sine.out" }, at(27.6));
camera($(".plate.dc"), at(27.6), 5.2, [1.0, 0, 0], [1.08, 0, -12], 2.0, "none");
camera($(".plate.dd"), at(27.6), 5.2, [1.0, 0, 0], [1.08, 0, -12], 2.0, "none");
// the colour withdraws (cross-fade between the two treatments of the same photo)
tl.fromTo($(".dwrap.dry"), { opacity: 0 }, { opacity: 1, duration: 2.4, ease: "sine.inOut" }, at(29.5));

function drawDry(shot, t0, hold) {
  const box = shot.querySelector(".ill-box");
  const strokes = Array.from(box.querySelectorAll(".ink > *"));
  prepDraw(strokes);
  tl.fromTo(shot, { opacity: 0 }, { opacity: 1, duration: 0.35, ease: "sine.out" }, at(t0 - 0.15));
  tl.fromTo(strokes, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.6, ease: "power2.inOut", stagger: 0.5 / Math.max(1, strokes.length - 1) }, at(t0));
  tl.fromTo(box, { scale: 1, transformOrigin: "50% 60%" }, { scale: 1.04, duration: hold, ease: "none", transformOrigin: "50% 60%" }, at(t0));
}
drawDry($(".ecole"), 32.5, 2.6);
drawDry($(".sante"), 34.9, 0.9);

// « Et les communautés ? » — the health post steps aside, the question holds 2.6 s
const ill = $(".sante .ill-box");
tl.to(ill, { ...pick({ x: -360, scale: 0.86 }, { y: -150, scale: 0.86 }, { y: -40, scale: 0.8 }), duration: 0.8, ease: "power2.inOut" }, at(35.8));
const q = $(".question");
const words = splitWords(q);
tl.fromTo(words, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out", stagger: 0.12 }, at(35.9));
tl.to(q, { opacity: 0, duration: 0.3, ease: "sine.in" }, at(38.3));
