// S2 — Contexte Guinée (6–12). Over the logo, the studio comes back; the photo of the sign-up screen (lighthouse,
// sea, city, the woman on her phone) floats in. The camera starts close on the lighthouse and the city, then pulls
// back and arcs to reveal the woman smiling at her phone. Caption at the bottom.
tl.fromTo($(".scene"), { opacity: 0 }, { opacity: 1, duration: 0.8, ease: "sine.inOut" }, at(5.8));
const card = $(".hero"), img = $(".hero img");
tl.fromTo(card, { rotationY: -14, rotationX: 4, z: -120, transformOrigin: "50% 50%" },
  { rotationY: 6, rotationX: 0, z: 0, duration: 6.6, ease: "power1.inOut", transformOrigin: "50% 50%" }, at(5.6));
// close on the lighthouse (upper left of the photo), then the whole picture
tl.fromTo(img, { scale: 1.8, xPercent: 40, yPercent: 30, transformOrigin: "50% 50%" },
  { scale: 1.0, xPercent: 0, yPercent: 0, duration: 4.4, ease: "power2.inOut", transformOrigin: "50% 50%" }, at(6.8));
tl.fromTo($(".over .t-over"), { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.8, ease: "power2.out" }, at(8.6));
