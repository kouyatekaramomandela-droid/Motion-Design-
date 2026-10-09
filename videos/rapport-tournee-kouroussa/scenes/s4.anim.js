// S4 — Les 8 axes (28–52), 3 s each. Axis k starts at A = 28 + 3(k-1); its word is spoken at A + 0.5.
// The new axis fades over the previous one; number, gold icon (drawn), title and line arrive in turn;
// the frise fills one point per axis.
tl.fromTo($(".dots"), { opacity: 0 }, { opacity: 1, duration: 0.8, ease: "sine.inOut" }, at(27.6));
const axes = $$(".ax"), dots = $$(".dots .dt");
axes.forEach((ax, i) => {
  const A = 28 + 3 * i;
  tl.fromTo(ax, { opacity: 0 }, { opacity: 1, duration: i === 0 ? 0.8 : 0.7, ease: "sine.inOut" }, at(i === 0 ? 27.4 : A - 0.4));
  if (i < axes.length - 1) tl.set(ax, { opacity: 0 }, at(A + 3.4));
  tl.fromTo(ax.querySelector(".win"), { x: pick(36, 0), y: pick(0, 24) }, { x: 0, y: 0, duration: 0.9, ease: "power2.out" }, at(A - 0.4));
  tl.fromTo(ax.querySelector(".win img, .win video"), { scale: 1.0 }, { scale: 1.045, duration: 3.9, ease: "none" }, at(A - 0.4));
  tl.fromTo(ax.querySelector(".t-num"), { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.6, ease: "power2.out" }, at(A + 0.05));
  const strokes = Array.from(ax.querySelectorAll(".icon .ic-s"));
  prepDraw(strokes);
  tl.fromTo(strokes, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.9, ease: "power2.inOut", stagger: 0.08 }, at(A + 0.25));
  tl.fromTo(ax.querySelector(".gold-rule"), { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: 0.6, ease: "power2.out", transformOrigin: "0% 50%" }, at(A + 0.35));
  tl.fromTo(ax.querySelector(".ttl"), { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.6, ease: "power2.out" }, at(A + 0.45));
  tl.fromTo(ax.querySelector(".line"), { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.6, ease: "power2.out" }, at(A + 0.75));
  // frise
  tl.fromTo(dots[i], { backgroundColor: "#00291A", borderColor: "rgba(246,242,233,0.55)" },
    { backgroundColor: "#C9A44C", borderColor: "#E6CC86", duration: 0.3, ease: "sine.out" }, at(A + 0.45));
  tl.fromTo(dots[i], { boxShadow: "0 0 0 0px rgba(201,164,76,0)" }, { boxShadow: "0 0 0 8px rgba(201,164,76,0.35)", duration: 0.4, ease: "power2.out" }, at(A + 0.45));
  if (i < axes.length - 1) tl.to(dots[i], { boxShadow: "0 0 0 0px rgba(201,164,76,0)", duration: 0.4, ease: "sine.in" }, at(A + 3.2));
  if (i > 0) tl.to($(".rail-fill"), { scaleX: i / 7, duration: 0.6, ease: "power2.inOut" }, at(A + 0.15));
});
tl.set($(".rail-fill"), { scaleX: 0 }, 0);
