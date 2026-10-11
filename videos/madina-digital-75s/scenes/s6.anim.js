// S6 — Bénéfices (57–66). Each benefit has its picture (paying with the phone, a parcel handed over at the door,
// the support agent, a family around a phone) and the matching trust badge of the home page flips in as a 3D card
// on its words (57.3, 58.9, 60.5, 62.7); then « Votre vie, plus simple ! » traces itself in orange script over the
// family. Everything fades before the signature so the studio light comes back clean.
tl.fromTo($(".scene"), { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "sine.inOut" }, at(56.75));
const TS = [57.3, 58.9, 60.5, 62.7];
const phs = $$(".ph"), bks = $$(".pbg img");
phs.forEach((ph, i) => {
  const tin = i === 0 ? 56.75 : TS[i] - 0.3, img = ph.querySelector("img");
  if (i === 0) tl.set(ph, { opacity: 1 }, at(tin));
  else if (i === 2) {
    tl.fromTo(ph, { opacity: 0, scale: 1.2, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.6, ease: "power2.out", transformOrigin: "50% 50%" }, at(tin));
  } else {
    tl.set(ph, { opacity: 1 }, at(tin));
    tl.fromTo(ph, { xPercent: 100 }, { xPercent: 0, duration: 0.6, ease: "power3.inOut" }, at(tin));
    tl.to(phs[i - 1], { xPercent: -30, duration: 0.6, ease: "power3.inOut" }, at(tin));
  }
  if (i > 0) tl.set(phs[i - 1], { autoAlpha: 0 }, at(tin + 0.75));
  const end = i < 3 ? TS[i + 1] - 0.3 + 0.75 : 66.0;
  tl.fromTo(img, { scale: i % 2 ? 1.12 : 1.03, xPercent: i % 2 ? 1.5 : -1.5, transformOrigin: "50% 50%" },
    { scale: i % 2 ? 1.03 : 1.12, xPercent: i % 2 ? -1.5 : 1.5, duration: end - tin, ease: "none", transformOrigin: "50% 50%" }, at(tin));
  if (FMT === "v") {
    tl.fromTo(bks[i], { opacity: 0 }, { opacity: 1, duration: 0.6, ease: "sine.inOut" }, at(tin));
    if (i > 0) tl.set(bks[i - 1], { autoAlpha: 0 }, at(tin + 0.75));
  }
});
TS.forEach((t, i) => {
  const b = $(`.bd${i + 1}`);
  tl.fromTo(b, { opacity: 0, rotationY: -100, z: -80, transformPerspective: 1300, transformOrigin: "50% 50%" },
    { opacity: 1, rotationY: 0, z: 0, duration: 0.9, ease: "power3.out", transformPerspective: 1300, transformOrigin: "50% 50%" }, at(t));
  tl.fromTo(b, { boxShadow: "0 6px 14px rgba(2,8,30,0.2)" }, { boxShadow: "0 30px 70px rgba(2,8,30,0.5)", duration: 0.9, ease: "power2.out" }, at(t));
});
tl.to($$(".badge"), { y: pick(-40, -20), duration: 0.8, ease: "power2.inOut" }, at(63.8));
tl.fromTo($(".shade2"), { opacity: 0 }, { opacity: pick(1, 0.6), duration: 0.8, ease: "sine.inOut" }, at(63.8));
tl.fromTo($(".vie .l1"), { clipPath: "inset(-30% 100% -30% 0%)" }, { clipPath: "inset(-30% 0% -30% 0%)", duration: 0.7, ease: "none" }, at(64.1));
tl.fromTo($(".vie .l2"), { clipPath: "inset(-30% 100% -30% 0%)" }, { clipPath: "inset(-30% 0% -30% 0%)", duration: 0.8, ease: "none" }, at(64.8));
// clear the stage for the signature: the studio and its light pool come back under the logo
tl.to($(".scene"), { opacity: 0, duration: 0.6, ease: "sine.inOut" }, at(65.7));
