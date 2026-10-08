// Scene 6 — Une gouvernance partagée (74.4–95.6). The halo becomes the ring, four colleges, three circles of control.
const svg = $("svg.s6-ring");
const q = (s) => svg.querySelector(s), qa = (s) => Array.from(svg.querySelectorAll(s));
tl.fromTo($(".s6 .lattice"), { opacity: 0 }, { opacity: 0.1, duration: 1.0 }, at(74.6));
tl.fromTo($(".s6-glow"), { opacity: 0 }, { opacity: 1, duration: 1.4 }, at(75.0));
tl.fromTo(q(".core"), { opacity: 0 }, { opacity: 1, duration: 0.4 }, at(75.0));
const halo = q(".halo-ring");
prepDraw(halo);
tl.fromTo(halo, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 1.0, ease: "power2.inOut" }, at(75.0));
tl.to(halo, { opacity: 0, duration: 0.5 }, at(75.9));
tl.fromTo(qa(".arc"), { opacity: 0, scale: 0.96, svgOrigin: "0 0" }, { opacity: 1, scale: 1, duration: 0.6, ease: "back.out(1.6)", stagger: 0.12, svgOrigin: "0 0" }, at(75.8));
tl.fromTo(qa(".arc-pct"), { opacity: 0 }, { opacity: 1, duration: 0.5, stagger: 0.1 }, at(76.3));
const rows = $$(".colleges .row");
const fromRow = H_ ? { opacity: 0, x: 40 } : { opacity: 0, y: 30 };
tl.fromTo(rows, fromRow, { opacity: 1, x: 0, y: 0, duration: 0.7, ease: "power3.out", stagger: 0.25 }, at(76.2));
// « la majorité » (79.1)
tl.to(q(".arc.a1"), { scale: 1.05, duration: 0.5, ease: "power2.out", svgOrigin: "0 0" }, at(79.0));
tl.to(rows.slice(1), { opacity: 0.4, duration: 0.4 }, at(79.0));
tl.to(rows[0], { scale: 1.05, duration: 0.5, ease: "power2.out", transformOrigin: "0% 50%" }, at(79.0));
tl.to(q(".arc.a1"), { scale: 1, duration: 0.6, ease: "power2.inOut", svgOrigin: "0 0" }, at(80.4));
tl.to(rows, { opacity: 0, x: H_ ? -30 : 0, duration: 0.5, ease: "power2.in", stagger: 0.08 }, at(80.3));

// circles of control, on « encadrée » (81.3), « auditée » (83.5), « publique » (85.8)
tl.fromTo(qa(".ctl"), { opacity: 0, scale: 0.9, svgOrigin: "0 0" }, { opacity: 0.7, scale: 1, duration: 0.8, ease: "power2.out", stagger: 0.1, svgOrigin: "0 0" }, at(80.2));
const ctlRows = $$(".controls .ctl-row"), ons = qa(".ctl-on"), gates = qa(".gate"), oks = $$(".controls .ok");
prepDraw(ons);
const ticks = gates.map((g) => g.querySelector(".tick"));
prepDraw(ticks);
[[80.6, 81.0, 81.7], [82.7, 83.2, 83.9], [84.9, 85.4, 86.1]].forEach(([rowT, ringT, gateT], i) => {
  tl.fromTo(ctlRows[i], H_ ? { opacity: 0, x: 40 } : { opacity: 0, y: 24 }, { opacity: 1, x: 0, y: 0, duration: 0.7, ease: "power3.out" }, at(rowT));
  tl.fromTo(ons[i], { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 1.0, ease: "power2.inOut" }, at(ringT));
  tl.fromTo(gates[i], { opacity: 0, scale: 0, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2.5)", transformOrigin: "50% 50%" }, at(gateT));
});
tl.fromTo(oks, { opacity: 0, scale: 0.6 }, { opacity: 0, scale: 0.6, duration: 0.01 }, 0);

// the token passes three validation steps (chimes 88.6 / 90.1 / 91.6)
const token = q(".token"), tpath = q(".token-path");
const A = -Math.PI / 6, T = { r: 120 };
const place = () => { token.setAttribute("cx", (T.r * Math.cos(A)).toFixed(1)); token.setAttribute("cy", (T.r * Math.sin(A)).toFixed(1)); };
tl.fromTo(tpath, { opacity: 0 }, { opacity: 0.6, duration: 0.6 }, at(87.2));
tl.fromTo(token, { opacity: 0 }, { opacity: 1, duration: 0.4 }, at(87.4));
tl.fromTo(T, { r: 120 }, { r: 300, duration: 1.0, ease: "power1.inOut", onUpdate: place, immediateRender: true }, at(87.6));
tl.to(T, { r: 350, duration: 1.0, ease: "power1.inOut", onUpdate: place }, at(89.1));
tl.to(T, { r: 400, duration: 1.0, ease: "power1.inOut", onUpdate: place }, at(90.6));
tl.to(T, { r: 470, duration: 0.8, ease: "power1.in", onUpdate: place }, at(92.0));
[88.6, 90.1, 91.6].forEach((g, i) => {
  tl.fromTo(ticks[i], { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.35, ease: "power2.out" }, at(g));
  tl.to(gates[i], { scale: 1.35, duration: 0.18, ease: "power2.out", yoyo: true, repeat: 1, transformOrigin: "50% 50%" }, at(g));
  tl.to(oks[i], { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2.4)" }, at(g));
});
tl.to(q(".core circle"), { opacity: 0.22, duration: 1.2, ease: "sine.inOut", yoyo: true, repeat: 5 }, at(81.0));

// exit: the token drops toward the land
tl.to(token, { attr: { cy: 900 }, duration: 1.0, ease: "power2.in" }, at(93.6));
tl.to($$(".controls .ctl-row"), { opacity: 0, duration: 0.5, stagger: 0.08 }, at(93.4));
tl.to(svg, { opacity: 0, scale: 0.92, duration: 1.2, ease: "power2.in", transformOrigin: "50% 50%" }, at(94.0));
tl.to($$(".s6-glow, .s6 .lattice"), { opacity: 0, duration: 1.0 }, at(94.4));
