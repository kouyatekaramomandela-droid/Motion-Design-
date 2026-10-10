// S7 — Signature (66–75). Back to the logo in the light pool; the key-figures band of the screens unfolds below it
// and its figures count up (+100 000 users, 12 modules, 100 % secure); « Explorer tous les modules » pulses once.
// Then the band leaves, the logo stays alone in the centre, the studio goes to black and the orange light fades last.
tl.fromTo($(".scene"), { opacity: 0 }, { opacity: 1, duration: 0.8, ease: "sine.inOut" }, at(65.4));
const lk = $(".lockup");
tl.fromTo(lk, { opacity: 0, scale: 0.9, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 1.0, ease: "power3.out", transformOrigin: "50% 50%" }, at(65.8));
const fmt = (v) => "+" + String(v).replace(/\B(?=(\d{3})+(?!\d))/g, " ");
if (FMT === "h") {
  const band = $(".band");
  tl.fromTo(band, { opacity: 0, scaleY: 0.02, scaleX: 1.55, transformOrigin: "50% 50%" }, { opacity: 1, scaleY: 1.55, scaleX: 1.55, duration: 0.8, ease: "power3.out", transformOrigin: "50% 50%" }, at(66.5));
} else {
  const blks = $$(".blk");
  blks.forEach((b) => tl.set(b, { scale: 2.6, transformOrigin: "0 0" }, 0));
  tl.fromTo(blks, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.6, ease: "power2.out", stagger: 0.12 }, at(66.5));
  tl.fromTo($(".ev"), { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.6, ease: "power2.out" }, at(67.1));
}
$$(".fu b").forEach((e) => countUp(e, 0, 100000, at(66.9), 1.6, fmt));
$$(".fm b").forEach((e) => countUp(e, 0, 12, at(67.1), 1.2));
$$(".fs b").forEach((e) => countUp(e, 0, 100, at(67.3), 1.2, (v) => v + "%"));
tl.fromTo($$(".explorer"), { scale: 1 }, { scale: 1.08, duration: 0.3, ease: "power2.out", yoyo: true, repeat: 1, transformOrigin: "50% 50%" }, at(70.2));
// the band leaves, the logo comes to the centre alone
tl.to(pick([$(".band")], [...$$(".blk"), $(".ev")]), { opacity: 0, y: 30, duration: 0.6, ease: "power2.in" }, at(72.2));
tl.to(lk, { y: pick(265, 360), scale: pick(1.25, 1.0), duration: 1.2, ease: "power2.inOut", transformOrigin: "50% 50%" }, at(72.4));
tl.fromTo($(".halo"), { opacity: 0 }, { opacity: 1, duration: 0.8, ease: "sine.inOut" }, at(72.6));
tl.fromTo($(".ember"), { opacity: 0 }, { opacity: 1, duration: 0.8, ease: "sine.inOut" }, at(72.8));
tl.fromTo($(".black"), { opacity: 0 }, { opacity: 1, duration: 1.0, ease: "sine.inOut" }, at(73.0));
tl.to([lk, $(".halo")], { opacity: 0, duration: 0.7, ease: "sine.in" }, at(74.0));
tl.to($(".ember"), { opacity: 0, duration: 0.6, ease: "sine.in" }, at(74.35));
