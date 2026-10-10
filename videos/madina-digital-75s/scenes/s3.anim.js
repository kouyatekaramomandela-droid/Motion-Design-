// S3 — Inscription (12–22). The sign-up window floats in on an arc, the camera closes on the form; the orange
// cursor goes from field to field and each one is typed with the examples of the screen; steps 2 and 3 light up;
// « S'inscrire » is pressed; a green check appears on « c'est validé ».
const FULL = [0, 0, 1536, 1024], FORM = pick([668, 250, 1212, 740], [668, 150, 1212, 870]);
const BOX = pick([150, 70, 1620, 940], [60, 300, 960, 1400]);
const FULLBOX = pick([170, 60, 1580, 960], [40, 560, 1000, 760]);
const cam = $(".cam"), win = $(".win");
tl.fromTo($(".scene"), { opacity: 0 }, { opacity: 1, duration: 0.8, ease: "sine.inOut" }, at(11.4));
tl.fromTo(win, { rotationY: 20, rotationX: 6, transformPerspective: 2600, transformOrigin: "50% 50%" },
  { rotationY: 0, rotationX: 0, duration: 1.8, ease: "power3.out", transformPerspective: 2600, transformOrigin: "50% 50%" }, at(11.4));
camSet(cam, FULL, FULLBOX, 0);
camTo(cam, FULL, FORM, BOX, at(12.4), 1.4, "power2.inOut");
// fields: cursor arrives, focus ring, typing
const CUR = $(".cursor");
const FIELDS = [
  [".f1", ".t1", "Diallo Aissatou", 800, 411, 13.3, 1.0],
  [".f2", ".t2", "+224 621 23 45 67", 1062, 411, 14.6, 1.0],
  [".f3", ".t3", "exemple@gmail.com", 805, 499, 15.9, 0.9],
  [".f4", ".t4", "••••••••", 1062, 499, 17.0, 0.5],
  [".f5", ".t5", "••••••••", 900, 581, 17.7, 0.5],
];
tl.fromTo(CUR, { x: 0, y: 0, opacity: 0 }, { opacity: 1, duration: 0.3 }, at(12.9));
FIELDS.forEach(([f, t, text, cx, cy, start, dur]) => {
  tl.to(CUR, { x: cx - 1100, y: cy - 330, duration: 0.45, ease: "power2.inOut" }, at(start - 0.45));
  tl.fromTo($(f), { opacity: 0 }, { opacity: 1, duration: 0.2 }, at(start - 0.05));
  typeText($(t), text, at(start), dur, false);
  tl.to($(f), { opacity: 0, duration: 0.2 }, at(start + dur + 0.1));
});
// progress: step 1 pulses while typing, then 2 and 3 light up
tl.fromTo($(".p1"), { opacity: 0.9, scale: 1 }, { opacity: 0, scale: 1.9, duration: 1.0, ease: "power1.out", repeat: 4 }, at(13.0));
tl.fromTo($(".s2st"), { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, at(18.3));
tl.fromTo($(".p2"), { opacity: 0.9, scale: 1 }, { opacity: 0, scale: 2, duration: 0.7, ease: "power1.out" }, at(18.3));
tl.fromTo($(".s3st"), { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, at(18.8));
tl.fromTo($(".p3"), { opacity: 0.9, scale: 1 }, { opacity: 0, scale: 2, duration: 0.7, ease: "power1.out" }, at(18.8));
// press « S'inscrire »
tl.to(CUR, { x: 938 - 1100, y: 700 - 330, duration: 0.5, ease: "power2.inOut" }, at(18.8));
tl.fromTo($(".press"), { scale: 1, boxShadow: "0 10px 24px rgba(236,22,110,0.35)" },
  { scale: 0.955, boxShadow: "0 2px 6px rgba(236,22,110,0.25)", duration: 0.14, ease: "power2.in", yoyo: true, repeat: 1 }, at(19.4));
tl.to(CUR, { scale: 0.7, duration: 0.14, yoyo: true, repeat: 1 }, at(19.4));
// the green check grows out of the button, then its tick draws
const ok = $(".okcheck"), okp = $(".okpath");
prepDraw(okp);
tl.fromTo(ok, { opacity: 0, scale: 0.2 }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.8)" }, at(19.75));
tl.fromTo(okp, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.45, ease: "power2.out" }, at(20.0));
tl.to(CUR, { opacity: 0, duration: 0.3 }, at(19.9));
