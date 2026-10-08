// F4 — Le contraste (27.4–38.6). No more gold lines. « dans beaucoup de villages » : a village among its
// fields (soft community grade); « l'eau potable manque encore » : the well loses its colour; then the
// classroom and the health post, already grey; « Et les communautés ? » holds to the end of the scene.
// the four shots, each on its words, joined by short dissolves
[[".village", 27.6, 0.8], [".well", 30.2, 0.5], [".ecole", 32.4, 0.35], [".sante", 34.85, 0.35]].forEach(([sel, t, d]) => {
  tl.fromTo($(sel), { opacity: 0 }, { opacity: 1, duration: d, ease: "sine.inOut" }, at(t));
});
camera($(".plate.bv"), at(27.6), 3.2, [1.0, 24, 0], [1.07, -24, 0], 1.8, "none");
camera($(".plate.dc"), at(30.2), 2.8, [1.0, 0, 0], [1.06, 0, -10], 2.0, "none");
camera($(".plate.dd"), at(30.2), 2.8, [1.0, 0, 0], [1.06, 0, -10], 2.0, "none");
// the colour withdraws from the well (cross-fade between two treatments of the same photo)
tl.fromTo($(".dwrap.dry"), { opacity: 0 }, { opacity: 1, duration: 1.6, ease: "sine.inOut" }, at(30.7));
camera($(".plate.kc"), at(32.4), 2.8, [1.0, 0, 0], [1.06, 0, 0], 1.7, "none");
camera($(".plate.sh"), at(34.85), 3.8, [1.0, 0, 0], [1.07, 0, 6], 1.8, "none");

// « Et les communautés ? » over the health post, held 2.4 s
tl.fromTo($(".qscrim"), { opacity: 0 }, { opacity: 1, duration: 0.6, ease: "sine.out" }, at(35.6));
const q = $(".question");
const words = splitWords(q);
tl.fromTo(words, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out", stagger: 0.12 }, at(35.9));
tl.to(q, { opacity: 0, duration: 0.3, ease: "sine.in" }, at(38.3));
