// S6 — Kouroussa a parlé (66–75). The women's assembly, slow 5 % push-in; the sentence in two beats on its
// band (« Kouroussa a parlé. » 67.6, « Nous portons sa voix. » 69.6); then the signature on ivory, the two
// deputies one after the other. The fade to white (74–75) is on the logo layer, above everything.
tl.fromTo($(".final"), { opacity: 0 }, { opacity: 1, duration: 0.8, ease: "sine.inOut" }, at(65.4));
tl.fromTo($(".final img"), { scale: 1.0 }, { scale: 1.05, duration: 6.4, ease: "none" }, at(65.4));
tl.fromTo($(".quote"), { opacity: 0 }, { opacity: 1, duration: 0.6, ease: "sine.out" }, at(67.35));
tl.fromTo($(".q1"), { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.7, ease: "power2.out" }, at(67.4));
tl.fromTo($(".q2"), { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.7, ease: "power2.out" }, at(69.4));
tl.to($(".quote"), { opacity: 0, duration: 0.5, ease: "sine.in" }, at(70.8));
tl.fromTo($(".sign"), { opacity: 0 }, { opacity: 1, duration: 0.8, ease: "sine.inOut" }, at(71.0));
tl.fromTo($$(".who"), { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.8, ease: "power2.out", stagger: 0.4 }, at(71.5));
tl.fromTo($$(".who img"), { scale: 1.04 }, { scale: 1.0, duration: 3.5, ease: "none" }, at(71.5));
tl.fromTo($(".role"), { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.7, ease: "power2.out" }, at(72.6));
