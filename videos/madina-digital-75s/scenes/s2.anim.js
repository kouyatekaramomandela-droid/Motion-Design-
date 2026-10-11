// S2 — Contexte Guinée (6–12). Drone shots: Conakry from the sky at sunrise, the camera pushing toward the
// lighthouse (« En Guinée… »); a fast cut to the lighthouse itself (« tout va vite ») ; on « Avec Madina Digital »
// the frame closes onto the photo of the sign-up screen (the woman on her phone, the lighthouse behind her),
// which floats on in the studio. Caption at the bottom on « à portée de main ».
const aer = $(".frame .aer"), pha = $(".frame .pha"), frame = $(".frame"), card = $(".hero");
tl.fromTo($(".scene"), { opacity: 0 }, { opacity: 1, duration: 0.7, ease: "sine.inOut" }, at(5.6));
// shot 1: aerial push toward the lighthouse on the point (left of the frame), slight drone yaw
tl.fromTo(aer, { scale: 1.04, rotation: -1.2, transformOrigin: "17% 42%" },
  { scale: 1.32, rotation: 0.6, duration: 3.1, ease: "power1.in", transformOrigin: "17% 42%" }, at(5.6));
// shot 2: whip to the lighthouse, then a slow drift
tl.fromTo(pha, { opacity: 0, xPercent: 9, scale: 1.16, transformOrigin: "70% 40%" },
  { opacity: 1, xPercent: 0, scale: 1.06, duration: 0.45, ease: "power3.out", transformOrigin: "70% 40%" }, at(8.42));
tl.to(pha, { scale: 1.0, duration: 1.6, ease: "none", transformOrigin: "70% 40%" }, at(8.87));
tl.set(aer, { autoAlpha: 0 }, at(8.9));
if (FMT === "v") {
  tl.fromTo($(".bl-pha"), { opacity: 0 }, { opacity: 1, duration: 0.45, ease: "power2.out" }, at(8.42));
  tl.set($(".bl-aer"), { autoAlpha: 0 }, at(8.9));
}
// « Avec Madina Digital » : the frame closes onto the hero card
const T_CLOSE = 9.05, D_CLOSE = 0.85;
if (FMT === "h") {
  tl.fromTo(frame, { clipPath: "inset(0px 0px 0px 0px round 0px)" },
    { clipPath: "inset(84px 714px 208px 714px round 26px)", duration: D_CLOSE, ease: "power3.inOut" }, at(T_CLOSE));
} else {
  // the card (60,260 960x1200) becomes the hero card (150,230 780x1250); the frame box is their union
  tl.fromTo(frame, { clipPath: "inset(30px 0px 20px 0px round 28px)" },
    { clipPath: "inset(0px 90px 0px 90px round 26px)", duration: D_CLOSE, ease: "power3.inOut" }, at(T_CLOSE));
  tl.fromTo($(".fshadow"), { x: 0, y: 0, scaleX: 1, scaleY: 1, transformOrigin: "0 0" },
    { x: 90, y: -30, scaleX: 780 / 960, scaleY: 1250 / 1200, duration: D_CLOSE, ease: "power3.inOut", transformOrigin: "0 0" }, at(T_CLOSE));
  tl.set($(".fshadow"), { autoAlpha: 0 }, at(T_CLOSE + D_CLOSE + 0.05));
  tl.to($(".pbg"), { opacity: 0, duration: 0.8, ease: "sine.inOut" }, at(T_CLOSE + 0.2));
}
tl.fromTo(card, { opacity: 0 }, { opacity: 1, duration: 0.45, ease: "sine.inOut" }, at(T_CLOSE + 0.45));
tl.set(frame, { autoAlpha: 0 }, at(T_CLOSE + D_CLOSE + 0.05));
// the card floats on: a slow arc, the photo settles
tl.fromTo(card, { rotationY: 0, rotationX: 0, z: 0, transformOrigin: "50% 50%" },
  { rotationY: 7, rotationX: -2, z: 40, duration: 2.7, ease: "sine.inOut", transformOrigin: "50% 50%" }, at(T_CLOSE + D_CLOSE));
tl.fromTo($(".hero img"), { scale: 1.06, transformOrigin: "50% 50%" }, { scale: 1.0, duration: 2.6, ease: "power1.out", transformOrigin: "50% 50%" }, at(T_CLOSE + 0.45));
tl.fromTo($(".over .t-over"), { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.8, ease: "power2.out" }, at(10.1));
