// S3 — Les urgences (18–28). Darkened meeting photos; the three counters climb to 15/15 on their word
// (« l'eau potable » 20.9, « la santé » 22.2, « l'agriculture » 23.4); then the two bars fill to 14/15.
tl.fromTo($(".scene"), { opacity: 0 }, { opacity: 1, duration: 0.8, ease: "sine.inOut" }, at(17.4));
const BT = [17.4, 21.0, 24.6, 28.6];
$$(".bgs .ph").forEach((ph, i) => {
  if (i > 0) tl.fromTo(ph, { opacity: 0 }, { opacity: 1, duration: 1.0, ease: "sine.inOut" }, at(BT[i]));
  tl.fromTo(ph.querySelector("img"), { scale: 1.0 }, { scale: 1.04, duration: BT[i + 1] - BT[i] + 1.0, ease: "none" }, at(BT[i]));
});
tl.fromTo($(".head"), { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.7, ease: "power2.out" }, at(18.2));
const tops = $$(".top");
tl.fromTo(tops, { opacity: 0, y: 30 }, { opacity: 0.55, y: 0, duration: 0.7, ease: "power2.out", stagger: 0.15 }, at(18.5));
[20.9, 22.2, 23.4].forEach((t, i) => {
  tl.to(tops[i], { opacity: 1, duration: 0.3, ease: "sine.out" }, at(t));
  countUp(tops[i].querySelector(".c-val"), 0, 15, at(t), 0.9, "power1.out");
  tl.fromTo(tops[i], { scale: 1 }, { scale: 1.035, duration: 0.3, ease: "power2.out", yoyo: true, repeat: 1 }, at(t + 0.75));
});
$$(".bar").forEach((b, i) => {
  const t = 24.3 + i * 0.7;
  tl.fromTo(b, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.6, ease: "power2.out" }, at(t));
  tl.fromTo(b.querySelector(".track i"), { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: 1.1, ease: "power2.inOut", transformOrigin: "0% 50%" }, at(t + 0.2));
  countUp(b.querySelector(".b-val"), 0, 14, at(t + 0.2), 1.1, "power2.inOut");
});
