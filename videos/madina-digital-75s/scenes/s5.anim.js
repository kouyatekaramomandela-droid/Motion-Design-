// S5 — Les 12 modules (30–57), heart of the film. The camera eases back over the home page; the 12 module tiles
// lift out of the page (they start exactly over their place in the screen) and settle into a rail — one row at the
// bottom in 16:9, two rows of six under the photo card in 9:16. Then each module opens its own world, 2 s apart from
// 32.4 s, on its words: an illustration (full frame in 16:9, a card over its blurred backdrop in 9:16) arrives with a
// circle opening from the tile, a push or a zoom, and drifts slowly while the module's tile lifts and lights up.
const HFULL = [0, 0, 1536, 1024];
const S4END = pick(camState(HFULL, [140, 50, 1640, 980]), camState([0, 118, 760, 520], [40, 640, 1000, 640]));
const LIFT = pick(camState(HFULL, [210, 100, 1500, 760]), camState([0, 500, 1536, 690], [40, 760, 1000, 160]));
const cam = $(".home .cam");
tl.fromTo($(".scene"), { opacity: 0 }, { opacity: 1, duration: 0.6, ease: "sine.inOut" }, at(29.4));
tl.fromTo(cam, { ...S4END, transformOrigin: "0 0" }, { ...LIFT, duration: 1.6, ease: "power2.inOut", transformOrigin: "0 0" }, at(29.6));
tl.fromTo($(".home .win"), { rotationX: 0, transformPerspective: 2600, transformOrigin: "50% 60%" },
  { rotationX: pick(10, 0), duration: 1.6, ease: "power2.inOut", transformPerspective: 2600, transformOrigin: "50% 60%" }, at(29.6));
// tiles: final rail layout, then a FLIP from their place in the screen
const tiles = $$(".tile");
const T_LIFT = 31.2;
tiles.forEach((el, k) => {
  const l = +el.dataset.l, r = +el.dataset.r, w0 = r - l;
  let tx, ty, s;
  if (FMT === "h") { s = 0.92; tx = (1920 - 1477 * s) / 2 + (l - 35) * s; ty = 1080 - 40 - 144 * s; }
  else { s = 1.12; const c = k % 6, row = Math.floor(k / 6); tx = 540 + (c - 2.5) * 160 - (w0 * s) / 2; ty = 1400 + 185 * row; }
  Object.assign(el.style, { left: tx + "px", top: ty + "px", width: w0 * s + "px", height: 144 * s + "px" });
  const sx = LIFT.x + LIFT.scale * (WB + l), sy = LIFT.y + LIFT.scale * (WBAR + 524);
  tl.set(el, { opacity: 1 }, at(T_LIFT));
  tl.fromTo(el, { x: sx - tx, y: sy - ty, scale: LIFT.scale / s, transformOrigin: "0 0" },
    { x: 0, y: 0, scale: 1, duration: 1.0, ease: "power3.inOut", delay: k * 0.03, transformOrigin: "0 0" }, at(T_LIFT));
  el.dataset.cx = tx + (w0 * s) / 2; el.dataset.cy = ty + (144 * s) / 2;
});
tl.fromTo($(".dim"), { opacity: 0 }, { opacity: 1, duration: 1.0, ease: "sine.inOut" }, at(T_LIFT));
tl.fromTo($(".panel"), { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.8, ease: "power2.out" }, at(30.2));
tl.to($(".panel"), { opacity: 0, y: -16, duration: 0.4, ease: "power2.in" }, at(31.9));
// the photo stage opens with the first module
const T0M = 32.4, IN = 0.32, TR = 0.6;
const phs = $$(".ph"), bks = $$(".pbg img");
tl.fromTo($(".pgrad"), { opacity: 0 }, { opacity: 1, duration: 0.6, ease: "sine.inOut" }, at(T0M - IN));
if (FMT === "v") {
  tl.fromTo($(".pcard"), { opacity: 0, y: 60, scale: 0.94, transformOrigin: "50% 100%" },
    { opacity: 1, y: 0, scale: 1, duration: 0.6, ease: "power3.out", transformOrigin: "50% 100%" }, at(T0M - IN));
}
tl.set([$(".home"), $(".dim")], { autoAlpha: 0 }, at(T0M + 0.5));
const CARD = pick([0, 0, 1920, 1080], [60, 150, 960, 1200]);
phs.forEach((ph, k) => {
  const t = T0M + 2 * k, tin = t - IN, img = ph.querySelector("img");
  const tile = tiles[k], cx = +tile.dataset.cx - CARD[0], cy = Math.min(+tile.dataset.cy - CARD[1], CARD[3]);
  const kind = FMT === "v" && k === 0 ? "pop" : ["circle", "push", "zoom"][k % 3];
  if (kind === "pop") tl.set(ph, { opacity: 1 }, at(tin));
  else if (kind === "circle") {
    tl.set(ph, { opacity: 1 }, at(tin));
    tl.fromTo(ph, { clipPath: `circle(0px at ${cx}px ${cy}px)` }, { clipPath: `circle(${pick(2300, 1600)}px at ${cx}px ${cy}px)`, duration: TR + 0.1, ease: "power2.in" }, at(tin));
  } else if (kind === "push") {
    tl.set(ph, { opacity: 1 }, at(tin));
    tl.fromTo(ph, { xPercent: 100 }, { xPercent: 0, duration: TR, ease: "power3.inOut" }, at(tin));
    tl.to(phs[k - 1], { xPercent: -30, duration: TR, ease: "power3.inOut" }, at(tin));
  } else {
    tl.fromTo(ph, { opacity: 0, scale: 1.2, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: TR, ease: "power2.out", transformOrigin: "50% 50%" }, at(tin));
  }
  if (k > 0) tl.set(phs[k - 1], { autoAlpha: 0 }, at(tin + TR + 0.12));
  // slow drift; Move travels sideways
  const last = k === phs.length - 1, dur = last ? 3.4 : 2.0 + TR + 0.15;
  const a = k % 2 ? { scale: 1.14, xPercent: 1.5 } : { scale: 1.03, xPercent: -1.5 };
  const b = k % 2 ? { scale: 1.04, xPercent: -1.5 } : { scale: 1.13, xPercent: 1.5 };
  if (last) { a.xPercent = 3.5; b.xPercent = -3.5; }
  tl.fromTo(img, { ...a, transformOrigin: "50% 50%" }, { ...b, duration: dur, ease: "none", transformOrigin: "50% 50%" }, at(tin));
  if (FMT === "v") {
    tl.fromTo(bks[k], { opacity: 0 }, { opacity: 1, duration: TR, ease: "sine.inOut" }, at(tin));
    if (k > 0) tl.set(bks[k - 1], { autoAlpha: 0 }, at(tin + TR + 0.12));
  }
  // the module's tile lifts and lights up on its words
  tl.set(tile, { zIndex: 5 }, at(t));
  tl.to(tile, { y: pick(-30, -22), scale: pick(1.45, 1.3), duration: 0.35, ease: "back.out(2)", transformOrigin: "50% 100%" }, at(t));
  tl.fromTo(tile.querySelector(".glow"), { opacity: 0 }, { opacity: 1, duration: 0.3 }, at(t));
  tl.to(tile, { y: 0, scale: 1, duration: 0.4, ease: "power2.inOut", transformOrigin: "50% 100%" }, at(t + 1.65));
  tl.to(tile.querySelector(".glow"), { opacity: 0, duration: 0.4 }, at(t + 1.65));
  tl.set(tile, { zIndex: 1 }, at(t + 2.05));
});
// hand over to the benefits (S6 fades in on top)
tl.to($(".tiles"), { opacity: 0, y: 20, duration: 0.45, ease: "power2.in" }, at(56.75));
