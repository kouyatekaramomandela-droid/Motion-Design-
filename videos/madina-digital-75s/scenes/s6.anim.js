// S6 — Bénéfices (57–66). The four trust badges of the home page flip in as 3D cards, each on its words
// (« Paiement sécurisé » 57.4, « Livraison rapide » 59.0, « service client » 60.6, « expérience unique » 62.8);
// then « Votre vie, plus simple ! » traces itself in orange script.
tl.fromTo($(".scene"), { opacity: 0 }, { opacity: 1, duration: 0.6, ease: "sine.inOut" }, at(56.4));
[57.3, 58.9, 60.5, 62.7].forEach((t, i) => {
  const b = $(`.bd${i + 1}`);
  tl.fromTo(b, { opacity: 0, rotationY: -100, z: -80, transformPerspective: 1300, transformOrigin: "50% 50%" },
    { opacity: 1, rotationY: 0, z: 0, duration: 0.9, ease: "power3.out", transformPerspective: 1300, transformOrigin: "50% 50%" }, at(t));
  tl.fromTo(b, { boxShadow: "0 6px 14px rgba(2,8,30,0.2)" }, { boxShadow: "0 30px 70px rgba(2,8,30,0.5)", duration: 0.9, ease: "power2.out" }, at(t));
});
tl.to($$(".badge"), { y: pick(-40, -20), duration: 0.8, ease: "power2.inOut" }, at(63.8));
tl.fromTo($(".vie .l1"), { clipPath: "inset(-30% 100% -30% 0%)" }, { clipPath: "inset(-30% 0% -30% 0%)", duration: 0.7, ease: "none" }, at(64.1));
tl.fromTo($(".vie .l2"), { clipPath: "inset(-30% 100% -30% 0%)" }, { clipPath: "inset(-30% 0% -30% 0%)", duration: 0.8, ease: "none" }, at(64.8));
