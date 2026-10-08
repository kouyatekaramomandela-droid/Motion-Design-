// Scene 1 — L'accroche (0–10.6). One spark → thousands → counter 2,35 → collapse into a gold thread.
const canvas = $("canvas.s1-particles");
canvas.width = W; canvas.height = H;
const ctx = canvas.getContext("2d");
const field = FK.makeField(H_ ? 2600 : 2300, 11);
const geo = pick(
  { cx: 960, cy: 500, maxR: 640, line: { x0: 230, x1: 930, y: 433 } },
  { cx: 540, cy: 860, maxR: 500, line: { x0: 90, x1: 990, y: 540 } });
const P = { t: 0 };
tl.fromTo(P, { t: 0 }, { t: DUR, duration: DUR, ease: "none", onUpdate: () => FK.drawGenesis(ctx, field, P.t, geo) }, 0);

// the black opens onto the night as the gold multiplies
tl.fromTo($(".s1-black"), { opacity: 1 }, { opacity: 0, duration: 3.4, ease: "sine.inOut" }, at(0.9));
tl.fromTo($(".s1-glow"), { opacity: 0, scale: 0.55 }, { opacity: 1, scale: 1, duration: 2.6, ease: "power2.out" }, at(0.8));
tl.to($(".s1-glow"), { scale: 1.07, duration: 1.4, ease: "sine.inOut", yoyo: true, repeat: 3 }, at(3.4));

// counter 0,00 → 2,35 (counting-dynamic-scale)
const num = $(".s1-num"), C = { v: 0 };
tl.fromTo($(".s1-count"), { opacity: 0, y: 40, scale: 0.88 }, { opacity: 1, y: 0, scale: 1, duration: 3.0, ease: "power2.out" }, at(2.6));
tl.fromTo(C, { v: 0 }, { v: 2.35, duration: 3.0, ease: "power2.out",
  onUpdate: () => { num.textContent = C.v.toFixed(2).replace(".", ","); } }, at(2.6));
tl.fromTo($(".s1-unit"), { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }, at(3.6));
tl.fromTo($(".s1-per"), { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.9, ease: "power2.out" }, at(4.2));
tl.fromTo($(".s1-line"), { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 1.0, ease: "power3.out" }, at(6.7));

// exit: the figures dissolve while the particles collapse into the thread (drawGenesis 9.0–10.3)
tl.to($(".s1-stack"), { opacity: 0, y: -24, filter: "blur(10px)", duration: 1.0, ease: "power2.in" }, at(8.9));
tl.to($(".s1-glow"), { opacity: 0, duration: 1.2, ease: "sine.in" }, at(9.2));
tl.to(canvas, { opacity: 0, duration: 0.5, ease: "sine.in" }, at(10.05));
