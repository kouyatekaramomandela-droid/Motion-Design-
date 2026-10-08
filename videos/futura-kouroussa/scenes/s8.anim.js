// Scene 8 — La signature (109.4–120). Gold waves settle into the tricolour band; the logo; the closing line.
const waves = $(".s8-waves.only-" + FMT);
const wv = Array.from(waves.querySelectorAll(".wave"));
prepDraw(wv);
tl.fromTo(wv, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 1.4, ease: "power2.out", stagger: 0.15 }, at(109.4));
tl.fromTo(waves, { x: -60 }, { x: 0, duration: 2.6, ease: "sine.out" }, at(109.4));
const drop = pick(1080 - 10 - 540, 1920 - 14 - 960);
tl.to(waves, { y: drop, scaleY: 0.04, duration: 1.4, ease: "power2.inOut", transformOrigin: "50% 50%" }, at(110.8));
tl.to(waves, { opacity: 0, duration: 0.4 }, at(112.0));
const band = $$(".s8-band i");
tl.fromTo(band, { scaleX: 0, transformOrigin: "50% 50%" }, { scaleX: 1, duration: 0.8, ease: "power3.out", stagger: 0.15, transformOrigin: "50% 50%" }, at(111.6));
tl.fromTo($(".s8-glow"), { opacity: 0 }, { opacity: 1, duration: 1.6 }, at(110.8));
tl.to($(".s8-glow"), { scale: 1.08, duration: 1.8, ease: "sine.inOut", yoyo: true, repeat: 2 }, at(113.0));

// the logo reforms on « Futura Kouroussa » (111.5)
const emb = $(".s8-emblem svg");
const nug = emb.querySelector(".nugget"), rays = Array.from(emb.querySelectorAll(".ray"));
const ho = emb.querySelector(".hand-outline"), th = emb.querySelector(".hand-thumb");
prepDraw([ho, th]);
tl.fromTo(nug, { scale: 0, rotation: -20, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, rotation: 0, opacity: 1, duration: 0.7, ease: "back.out(2)", transformOrigin: "50% 50%" }, at(111.2));
tl.fromTo(ho, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 1.3, ease: "power2.inOut" }, at(111.4));
tl.fromTo(th, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.9, ease: "power2.inOut" }, at(111.9));
tl.fromTo(rays, { scale: 0.15, opacity: 0, svgOrigin: "204 162" }, { scale: 1, opacity: 1, duration: 0.6, ease: "power3.out", stagger: 0.06, svgOrigin: "204 162" }, at(112.2));
tl.fromTo($(".s8-word"), { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }, at(111.7));
tl.fromTo($(".s8-name"), { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.8, ease: "power2.out" }, at(112.3));
// closing line on « L'or de Kouroussa… » (113.9)
const words = splitWords($(".s8-sign"));
tl.fromTo(words, { opacity: 0, y: 34 }, { opacity: 1, y: 0, duration: 0.7, ease: "power3.out", stagger: 0.06 }, at(113.9));
// final hold: only a slow breath (no fade before 120 s)
tl.fromTo($(".s8-lockup"), { scale: 1, transformOrigin: "50% 40%" }, { scale: 1.025, duration: 6.0, ease: "none", transformOrigin: "50% 40%" }, at(114.0));
