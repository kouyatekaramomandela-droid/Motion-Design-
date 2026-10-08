// F2 — La terre et les gens (4.4–15.6). One shot per idea, each on its word, joined by a gold line
// that sweeps the frame: the river (photo A, 2.5D), a quarter, a market (gold line illustrations).
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

// shots 2 and 3 — the line art draws itself, its three planes drift at different speeds, windows and stalls light up
function drawIll(box, t0, dur, hold) {
  const strokes = Array.from(box.querySelectorAll(".ink > *"));
  prepDraw(strokes);
  const each = 0.7, stag = (dur - each) / Math.max(1, strokes.length - 1);
  tl.fromTo(strokes, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: each, ease: "power2.inOut", stagger: stag }, at(t0));
  tl.fromTo(Array.from(box.querySelectorAll(".lit")), { opacity: 0 }, { opacity: 1, duration: 0.6, ease: "sine.out" }, at(t0 + dur));
  const depth = { back: 8, mid: 16, front: 34 };
  Object.keys(depth).forEach((k) => {
    const g = box.querySelector(".layer." + k);
    if (g) tl.fromTo(g, { x: depth[k] }, { x: -depth[k], duration: hold, ease: "none" }, at(t0));
  });
  tl.fromTo(box, { scale: 1, transformOrigin: "50% 60%" }, { scale: 1.05, duration: hold, ease: "none", transformOrigin: "50% 60%" }, at(t0));
}
drawIll($(".p2 .ill-box"), 7.75, 1.3, 2.9);
drawIll($(".p3 .ill-box"), 10.25, 1.5, 5.3);
// the woman carrying the basin walks on, the child follows
tl.fromTo($(".p3 .carrier"), { x: -14 }, { x: 10, duration: 5.2, ease: "sine.inOut" }, at(10.3));
tl.fromTo($(".p3 .child"), { x: -8 }, { x: 8, duration: 5.2, ease: "sine.inOut" }, at(10.3));
