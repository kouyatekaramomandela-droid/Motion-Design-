// F3 — L'or (14.4–28.6). « Sous cette terre » : a gold line descends and opens the first mine (photo C,
// warm gold grade, calm top view, machines as the near plane). « Trois mines » : the photo sinks into the
// dark and the three mine sites come forward one by one (18.9 / 19.4 / 19.9) with the counter.
// Then the third mine fills the frame, dark, under « plus de 2 milliards USD par an ».
const line = $(".wipe-line.horz");
tl.fromTo($(".mineshot"), { clipPath: "inset(0% 0% 100% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.7, ease: "power2.inOut" }, at(14.6));
tl.fromTo(line, { y: -6, opacity: 1 }, { y: H, duration: 0.7, ease: "power2.inOut" }, at(14.6));
tl.set(line, { opacity: 0 }, at(15.32));
camera($(".plate.c1"), at(14.6), 13.0, [1.0, 0, 0], [1.16, 0, -10], 1.5, "none");
camera($(".plate.c1s"), at(14.6), 13.0, [1.0, 0, 0], [1.16, 0, -10], 1.5, "none");
tl.fromTo($(".sweep"), { x: 0 }, { x: W * 1.9, duration: 1.8, ease: "sine.inOut" }, at(16.3));

// gold dust rising from the pits
const cv = $("canvas.dust"); cv.width = W; cv.height = H;
const ctx = cv.getContext("2d"), field = FK.makeField(pick(320, 320, 260), 31), D = { t: 0 };
tl.fromTo(D, { t: 0 }, { t: 13.6, duration: 13.6, ease: "none", onUpdate: () => FK.drawDust(ctx, field, D.t * 1.6, 0.6) }, at(14.6));

// the first mine sinks into the dark: cross-fade to the same grade at exposure -1.1 + blur (baked)
tl.fromTo($(".sunk"), { opacity: 0 }, { opacity: 1, duration: 0.9, ease: "sine.inOut" }, at(18.1));
tl.to($(".warm"), { opacity: 0, duration: 0.01 }, at(19.05));
tl.to($(".sunk"), { opacity: 0.6, duration: 0.8, ease: "sine.inOut" }, at(19.1));

// three mine sites, one by one (chimes at 18.9 / 19.4 / 19.9), counter 1 · 2 · 3
const panels = [$(".m1"), $(".m2"), $(".m3")];
[18.9, 19.4, 19.9].forEach((t, i) => {
  const p = panels[i];
  tl.fromTo(p, { opacity: 0, y: 50, scale: 0.92, transformOrigin: "50% 50%" }, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "power3.out", transformOrigin: "50% 50%" }, at(t));
  tl.fromTo(p.querySelector(".nb"), { scale: 0, transformOrigin: "50% 50%" }, { scale: 1, duration: 0.4, ease: "back.out(3)", transformOrigin: "50% 50%" }, at(t + 0.15));
  camera(p.querySelector(".plate"), at(t), 3.0, [1.0, 0, 0], [1.06, 0, 0], 1.6, "none");
  const q = $(".q" + (i + 1));
  tl.fromTo(q, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, at(t));
  if (i < 2) tl.to(q, { opacity: 0, y: -24, duration: 0.2, ease: "power2.in" }, at(t + 0.45));
});
// « 3 mines » holds 2 s, then the sites give way to the figure
tl.to($(".count"), { opacity: 0, y: -30, duration: 0.4, ease: "power2.in" }, at(21.7));
tl.to(panels, { opacity: 0, scale: 0.94, duration: 0.5, ease: "power2.in", stagger: 0.05 }, at(21.6));
tl.fromTo($(".heroshot"), { opacity: 0 }, { opacity: 1, duration: 0.8, ease: "sine.inOut" }, at(21.7));
camera($(".plate.c3s"), at(21.7), 6.0, [1.04, 0, 0], [1.12, 0, -8], 1.5, "none");

// hero: « plus de 2 milliards USD par an » (« deux milliards » 22.6–23.3, « chaque année » 24.0)
const num = $(".hero-num"), C = { v: 0 };
tl.fromTo($(".hero-pre"), { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, at(22.0));
tl.fromTo($(".hero-num"), { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, at(22.1));
tl.fromTo(C, { v: 0 }, { v: 2, duration: 1.2, ease: "power2.out",
  onUpdate: () => { num.textContent = C.v < 1.995 ? C.v.toFixed(1).replace(".", ",") : "2"; } }, at(22.1));
tl.fromTo($(".hero-mil"), { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }, at(22.7));
tl.fromTo($(".hero-usd"), { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, at(23.3));
tl.fromTo($(".hero-usd .per"), { opacity: 0 }, { opacity: 1, duration: 0.5 }, at(23.9));
tl.fromTo($(".hero-num"), { scale: 1, transformOrigin: "50% 70%" }, { scale: 1.06, duration: 0.25, ease: "power2.out", yoyo: true, repeat: 1, transformOrigin: "50% 70%" }, at(23.3));
tl.fromTo($(".hero"), { scale: 1, transformOrigin: "50% 50%" }, { scale: 1.03, duration: 4.6, ease: "none", transformOrigin: "50% 50%" }, at(22.4));

// exit: the gold leaves, the frame goes dark (27.0–27.9)
tl.to($(".hero"), { opacity: 0, y: -20, filter: "blur(8px)", duration: 0.6, ease: "power2.in" }, at(27.0));
tl.to([$(".heroshot"), $(".mineshot")], { opacity: 0, duration: 0.8, ease: "sine.in" }, at(27.1));
tl.to(cv, { x: W * 0.4, opacity: 0, duration: 0.8, ease: "power2.in" }, at(27.0));
