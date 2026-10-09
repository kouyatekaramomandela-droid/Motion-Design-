// S2 — La tournée (6–18). The prefecture outline draws in gold, the 15 localities light one by one in the
// report's order (0.6 s apart, from 7.2 s), each name shown in turn; « 15 localités » counts the lit points;
// the meeting photos follow one another in the gold frame.
tl.fromTo($(".scene"), { opacity: 0 }, { opacity: 1, duration: 0.8, ease: "sine.inOut" }, at(5.4));
const outline = $(".mapsvg .outline");
prepDraw(outline);
tl.fromTo(outline, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 1.6, ease: "power2.inOut" }, at(5.8));
tl.fromTo($(".mapsvg .units"), { opacity: 0 }, { opacity: 1, duration: 1.0, ease: "sine.inOut" }, at(6.3));
const T_PT = 7.2, STEP = 0.6;
$$(".pt").forEach((p, i) => {
  const t = at(T_PT + i * STEP);
  tl.fromTo(p.querySelectorAll(".ring, .dot"), { scale: 0, transformOrigin: "50% 50%" }, { scale: 1, duration: 0.5, ease: "back.out(2.2)", transformOrigin: "50% 50%" }, t);
  tl.fromTo(p.querySelector(".halo"), { scale: 0.3, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.5, ease: "power2.out", transformOrigin: "50% 50%" }, t);
  tl.to(p.querySelector(".halo"), { opacity: 0.35, duration: 0.8, ease: "sine.inOut" }, t + 0.7);
});
const labels = $$(".plabel span");
labels.forEach((l, i) => {
  const t = at(T_PT + i * STEP);
  tl.fromTo(l, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.22, ease: "power2.out" }, t);
  tl.to(l, { opacity: 0, duration: 0.18, ease: "power1.in" }, i === labels.length - 1 ? at(17.2) : t + STEP - 0.12);
});
// counters
tl.fromTo($(".counters"), { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.7, ease: "power2.out" }, at(6.2));
countUp($(".n-jours"), 0, 10, at(6.4), 1.0, "power1.out", [$(".n-jours + .t-label"), "jour", "jours"]);
stepCount($(".n-loc"), 15, at(T_PT), STEP, [$(".n-loc + .t-label"), "localité", "localités"]);
// photo card: each photo covers the previous one, with a slow 4 % push-in
const KT = [5.4, 7.6, 9.6, 11.4, 13.4, 15.4, 18.6];
$$(".card .ph").forEach((ph, i) => {
  if (i > 0) tl.fromTo(ph, { opacity: 0 }, { opacity: 1, duration: 0.7, ease: "sine.inOut" }, at(KT[i]));
  tl.fromTo(ph.querySelector("img, video"), { scale: 1.0 }, { scale: 1.04, duration: KT[i + 1] - KT[i] + 0.7, ease: "none" }, at(KT[i]));
});
