// F1 — Ouverture (0–5.6). Black, a gold spark (0.4 s), the bridge over the Niger opens out of it in a
// slow plunge (2.5D: the bridge comes up faster than the water), KOUROUSSA is engraved in gold.
const plate = $(".plate.a1"), dark = $(".plate.a1d");
const spark = $(".f1-spark");
tl.fromTo(spark, { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.5)" }, at(0.4));
tl.to(spark, { scale: 2.8, opacity: 0, duration: 1.3, ease: "power2.in" }, at(0.95));
// the photo opens out of the spark through a soft-edged light (mask radius is a CSS variable)
tl.fromTo($(".f1-shot"), { "--r": "0%" }, { "--r": "90%", duration: 2.0, ease: "power2.inOut" }, at(0.7));
camera(plate, at(0.75), 4.85, [1.34, 0, -30], [1.04, 0, 0], 1.7, "power2.out");
camera(dark, at(0.75), 4.85, [1.34, 0, -30], [1.04, 0, 0], 1.7, "power2.out");
const po = plate.dataset.ox + "px " + plate.dataset.oy + "px";
const cam = $(".cam"), co = (parseFloat(plate.style.left) + parseFloat(plate.dataset.ox)) + "px " + (parseFloat(plate.style.top) + parseFloat(plate.dataset.oy)) + "px";
tl.fromTo(cam, { rotation: -4, transformOrigin: co }, { rotation: 0, duration: 4.85, ease: "power2.out", transformOrigin: co }, at(0.75));
// the photo darkens under the title: cross-fade to the same grade at exposure -0.6 (baked)
tl.fromTo($(".dark"), { opacity: 0 }, { opacity: 1, duration: 1.4, ease: "sine.inOut" }, at(1.4));

// gold particles born from the spark
const cv = $("canvas.dust"); cv.width = W; cv.height = H;
const ctx = cv.getContext("2d");
const field = FK.makeField(pick(1500, 1300, 1100), 5);
const geo = { cx: W / 2, cy: H / 2, maxR: pick(760, 620, 560), line: { x0: 0, x1: W, y: H / 2 } };
const P = { t: 0 };
tl.fromTo(P, { t: 0 }, { t: DUR, duration: DUR, ease: "none", onUpdate: () => FK.drawGenesis(ctx, field, P.t + 0.4, geo) }, 0);
tl.to(cv, { opacity: 0.4, duration: 1.6, ease: "sine.inOut" }, at(2.4));

// KOUROUSSA: letters set in gold one by one, then a light sweep runs through them
const toSpans = (el) => {
  const txt = el.textContent; el.textContent = "";
  return Array.from(txt).map((ch) => { const s = document.createElement("span"); s.textContent = ch; el.appendChild(s); return s; });
};
const letters = toSpans($(".f1-word"));
tl.fromTo(letters, { opacity: 0, y: 26, scale: 1.25, filter: "blur(8px)" },
  { opacity: 1, y: 0, scale: 1, filter: "blur(0px)", duration: 0.7, ease: "power3.out", stagger: 0.07 }, at(1.5));
tl.fromTo(letters, { backgroundPosition: "130% 0%, 0% 0%" }, { backgroundPosition: "-30% 0%, 0% 0%", duration: 0.7, ease: "sine.inOut", stagger: 0.08 }, at(2.6));
tl.fromTo($(".f1-title"), { scale: 1, transformOrigin: "50% 50%" }, { scale: 1.04, duration: 3.6, ease: "none", transformOrigin: "50% 50%" }, at(2.0));
