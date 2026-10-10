// S4 — Connexion et accueil (22–30). Crossfade to the log-in window already framed on its form; e-mail and password
// are typed; « Se connecter » is pressed; a blue then orange horizontal wipe opens the home page, which settles with
// a slow 3D tilt (parallax feel) while the search bar takes the focus.
const LFORM = pick([806, 160, 1340, 620], [806, 165, 1340, 860]);
const BOX = pick([150, 70, 1620, 940], [60, 300, 960, 1400]);
const HFULL = [0, 0, 1536, 1024], HHERO = pick([0, 60, 1536, 640], [0, 118, 760, 520]), HBOX = pick([140, 50, 1640, 980], [40, 640, 1000, 640]);
const login = $(".login"), home = $(".home");
const lcam = $(".login .cam"), hcam = $(".home .cam");
tl.fromTo(login, { opacity: 0 }, { opacity: 1, duration: 0.8, ease: "sine.inOut" }, at(21.4));
camTo(lcam, [806, 190, 1340, 640], LFORM, BOX, at(21.4), 1.2, "power2.out");
const CUR = $(".login .cursor");
tl.fromTo(CUR, { x: 0, y: 0, opacity: 0 }, { opacity: 1, duration: 0.3 }, at(22.0));
[[".g1", ".u1", "exemple@gmail.com", 1000, 350, 22.6, 0.9], [".g2", ".u2", "••••••••", 1000, 454, 23.8, 0.5]].forEach(([f, t, text, cx, cy, start, dur]) => {
  tl.to(CUR, { x: cx - 1200, y: cy - 250, duration: 0.4, ease: "power2.inOut" }, at(start - 0.4));
  tl.fromTo($(f), { opacity: 0 }, { opacity: 1, duration: 0.2 }, at(start - 0.05));
  typeText($(t), text, at(start), dur, false);
  tl.to($(f), { opacity: 0, duration: 0.2 }, at(start + dur + 0.1));
});
tl.to(CUR, { x: 1072 - 1200, y: 573 - 250, duration: 0.4, ease: "power2.inOut" }, at(24.2));
tl.fromTo($(".login .press"), { scale: 1, boxShadow: "0 10px 24px rgba(236,22,110,0.35)" },
  { scale: 0.955, boxShadow: "0 2px 6px rgba(236,22,110,0.25)", duration: 0.14, ease: "power2.in", yoyo: true, repeat: 1 }, at(24.65));
tl.to(CUR, { scale: 0.7, duration: 0.14, yoyo: true, repeat: 1 }, at(24.65));
// blue-orange wipe, the home page behind it
tl.fromTo($(".w1"), { x: 0 }, { x: W * 2.5, duration: 0.9, ease: "power2.inOut" }, at(25.0));
tl.fromTo($(".w2"), { x: 0 }, { x: W * 2.5, duration: 0.9, ease: "power2.inOut" }, at(25.12));
tl.set(login, { opacity: 0 }, at(25.45));
tl.fromTo(home, { opacity: 0 }, { opacity: 1, duration: 0.01 }, at(25.45));
camTo(hcam, HHERO, pick(HFULL, HHERO), HBOX, at(25.45), 4.6, "power1.inOut");
tl.fromTo($(".home .win"), { rotationY: -12, rotationX: 5, transformPerspective: 2600, transformOrigin: "50% 50%" },
  { rotationY: 0, rotationX: 0, duration: 3.6, ease: "power2.out", transformPerspective: 2600, transformOrigin: "50% 50%" }, at(25.45));
tl.fromTo($(".home .sheen"), { x: 0 }, { x: 2600, duration: 2.2, ease: "power2.inOut" }, at(26.0));
tl.fromTo($(".fs"), { opacity: 0 }, { opacity: 1, duration: 0.4 }, at(28.0));
tl.fromTo($(".caretonly"), { opacity: 0 }, { opacity: 1, duration: 0.05, repeat: 5, yoyo: true, repeatDelay: 0.3 }, at(28.1));
