// S5 — Recommandations (52–66). Very soft photos under an ivory veil (prefecture, mining-site meeting,
// elders); the three columns drop in cascade on « transmettre » (55.2), « plaider » (57.6), « suivre » (60.0).
tl.fromTo($(".scene"), { opacity: 0 }, { opacity: 1, duration: 0.8, ease: "sine.inOut" }, at(51.4));
const BT = [51.4, 56.8, 59.6, 66.6];
$$(".bgs .ph").forEach((ph, i) => {
  if (i > 0) tl.fromTo(ph, { opacity: 0 }, { opacity: 1, duration: 0.9, ease: "sine.inOut" }, at(BT[i]));
  tl.fromTo(ph.querySelector("img"), { scale: 1.0 }, { scale: 1.04, duration: BT[i + 1] - BT[i] + 0.9, ease: "none" }, at(BT[i]));
});
tl.fromTo($(".head"), { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.7, ease: "power2.out" }, at(52.3));
tl.fromTo($(".head .gold-rule"), { scaleX: 0, transformOrigin: "50% 50%" }, { scaleX: 1, duration: 0.6, ease: "power2.out", transformOrigin: "50% 50%" }, at(52.6));
[55.1, 57.5, 59.9].forEach((t, i) => {
  const col = $$(".col")[i];
  tl.fromTo(col, { opacity: 0, y: -36 }, { opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }, at(t));
  tl.fromTo(col.querySelectorAll("li"), { opacity: 0, x: -12 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out", stagger: 0.18 }, at(t + 0.35));
});
