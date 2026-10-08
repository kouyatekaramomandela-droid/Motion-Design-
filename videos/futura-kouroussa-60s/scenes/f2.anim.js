// F2 — La terre et les gens (4.4–15.6). One shot per idea, each on its word, joined by a gold line
// that sweeps the frame: the river (photo A, 2.5D), the Maison des Jeunes de Kouroussa, the women of an
// association (client photos; group photos get a slow camera move without a detached plane).
const shots = [$(".p1"), $(".p2"), $(".p3")], lines = $$(".wipe-line");
const cuts = [4.6, 7.7, 10.2];
shots.forEach((s, i) => {
  tl.fromTo(s, { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.6, ease: "power2.inOut" }, at(cuts[i]));
  tl.fromTo(lines[i], { x: -6, opacity: 1 }, { x: W, duration: 0.6, ease: "power2.inOut" }, at(cuts[i]));
  tl.set(lines[i], { opacity: 0 }, at(cuts[i] + 0.62));
});

// shot 1 — the river: lateral parallax (the bridge edge slides faster than the water), glints on the water
camera($(".plate.a2"), at(4.6), 3.8, [1.05, 36, 0], [1.1, -36, 0], 1.9, "sine.inOut");
const cv = $(".p1 canvas.dust"); cv.width = W; cv.height = H;
const ctx = cv.getContext("2d"), field = FK.makeField(pick(260, 260, 200), 23), D = { t: 0 };
tl.fromTo(D, { t: 0 }, { t: 4, duration: 4, ease: "none", onUpdate: () => FK.drawDust(ctx, field, D.t, 0.55) }, at(4.6));

// titles land on their word: « fleuve » 6.76, « quartiers » 8.36, « familles » 11.01
[[".t1", 5.9], [".t2", 8.3], [".t3", 10.8]].forEach(([sel, t]) => {
  const el = $(sel), rule = el.querySelector(".rule");
  tl.fromTo(el, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.7, ease: "power3.out" }, at(t));
  tl.fromTo(rule, { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: 0.6, ease: "power2.out", transformOrigin: "0% 50%" }, at(t + 0.1));
});

// shots 2 and 3 — slow camera moves on the photos
camera($(".plate.q2"), at(7.7), 2.9, [1.0, 0, 0], [1.07, 0, -8], 1.0, "none");
camera($(".plate.fm3"), at(10.2), 5.4, [1.04, 34, 0], [1.09, -34, 0], 1.0, "none");
