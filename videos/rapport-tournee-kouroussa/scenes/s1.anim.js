// S1 — Ouverture (0–6). Ivory and gold; the two deputies at the welcome come from blur to sharp (baked
// soft layer fading out) with a slow 5 % zoom out; the title rises line by line; then the date band.
tl.fromTo($(".duo"), { opacity: 0 }, { opacity: 1, duration: 1.0, ease: "sine.out" }, at(0.1));
tl.fromTo($(".duo"), { scale: 1.05, transformOrigin: "50% 35%" }, { scale: 1.0, duration: 6.6, ease: "none", transformOrigin: "50% 35%" }, at(0));
tl.fromTo($$(".duo .soft"), { opacity: 1 }, { opacity: 0, duration: 2.6, ease: "sine.inOut" }, at(0.5));
tl.fromTo($(".sheen-band"), { x: 0, opacity: 0 }, { x: W * 1.7, opacity: 1, duration: 3.4, ease: "sine.inOut" }, at(0.5));
tl.fromTo($(".kicker"), { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.7, ease: "power2.out" }, at(0.7));
tl.fromTo($(".title-block .gold-rule"), { scaleX: 0, transformOrigin: pick("0% 50%", "50% 50%") }, { scaleX: 1, duration: 0.7, ease: "power2.out", transformOrigin: pick("0% 50%", "50% 50%") }, at(0.9));
tl.fromTo($$(".title span"), { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.8, ease: "power2.out", stagger: 0.25 }, at(1.1));
tl.fromTo($(".sub"), { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.8, ease: "power2.out" }, at(2.4));
