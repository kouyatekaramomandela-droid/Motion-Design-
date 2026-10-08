// Scene 4 — Le socle légal (41.4–58.6). The book opens, the articles light up, the lines come back and converge.
tl.fromTo($(".s4 .lattice"), { opacity: 0 }, { opacity: 0.1, duration: 1.6 }, at(41.8));
tl.fromTo($(".s4-glow"), { opacity: 0 }, { opacity: 0.9, duration: 1.6 }, at(42.2));
const right = $(".page.right"), left = $(".page.left");
tl.fromTo(right, { x: pick(900, 700), opacity: 0 }, { x: 0, opacity: 1, duration: 1.3, ease: "power3.out" }, at(41.3));
tl.fromTo(left, { rotationY: -105, opacity: 0, transformOrigin: "100% 50%" }, { rotationY: 0, opacity: 1, duration: 1.4, ease: "power2.out", transformOrigin: "100% 50%", transformPerspective: 2200 }, at(42.3));
tl.fromTo($(".s4 .spine"), { opacity: 0 }, { opacity: 1, duration: 0.6 }, at(42.8));
tl.fromTo($$(".s4 .bars i"), { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: 0.6, ease: "power2.out", stagger: 0.03, transformOrigin: "0% 50%" }, at(43.0));
tl.fromTo($(".s4 .page.left .t-label"), { opacity: 0 }, { opacity: 1, duration: 0.6 }, at(43.1));

function lightUp(block, g) {
  tl.fromTo(block, { backgroundColor: "rgba(245,197,24,0)", boxShadow: "0 0 0px rgba(245,197,24,0)" },
    { backgroundColor: "rgba(245,197,24,0.10)", boxShadow: "0 0 60px rgba(245,197,24,0.18)", duration: 1.0, ease: "sine.inOut" }, at(g));
}
const a130 = $(".art130"), a165 = $(".art165");
lightUp(a130, 44.3);
tl.fromTo(a130.querySelector(".art-title"), { opacity: 0.18 }, { opacity: 1, duration: 0.7 }, at(44.5));
tl.fromTo(a130.querySelector(".art-sub"), { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.7, ease: "power2.out" }, at(45.0));
tl.fromTo(a130.querySelector(".art-pct"), { opacity: 0, scale: 0.7, transformOrigin: "0% 70%" }, { opacity: 1, scale: 1, duration: 0.8, ease: "back.out(1.8)", transformOrigin: "0% 70%" }, at(45.6));
tl.fromTo(a130.querySelector(".art-desc"), { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.7, ease: "power2.out" }, at(46.0));
lightUp(a165, 47.6);
tl.fromTo(a165.querySelector(".art-title"), { opacity: 0.18 }, { opacity: 1, duration: 0.7 }, at(47.8));

// the gold lines turn back and converge on one point
const conv = $(".s4-converge.only-" + FMT);
const backs = Array.from(conv.querySelectorAll(".back"));
prepDraw(backs);
tl.fromTo(backs, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 2.6, ease: "power2.inOut", stagger: 0.3 }, at(49.8));
tl.fromTo(conv.querySelector(".focus"), { scale: 0, transformOrigin: "50% 50%" }, { scale: 1, duration: 1.0, ease: "back.out(2)", transformOrigin: "50% 50%" }, at(52.8));
tl.fromTo(conv.querySelector(".focus-halo"), { scale: 0, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 0.25, duration: 1.2, ease: "power2.out", transformOrigin: "50% 50%" }, at(53.0));
tl.to(conv.querySelector(".focus"), { scale: 2.0, duration: 2.4, ease: "sine.inOut", transformOrigin: "50% 50%" }, at(54.2));
tl.to(conv.querySelector(".focus-halo"), { scale: 2.4, opacity: 0.4, duration: 2.4, ease: "sine.inOut", transformOrigin: "50% 50%" }, at(54.2));
tl.to($(".s4-book"), { opacity: 0.3, scale: 0.95, duration: 3.0, ease: "sine.inOut" }, at(52.0));
// exit: everything is drawn into the point (inhale 55.6–57.4)
tl.to($$(".s4-book, .s4 .lattice, .s4-glow"), { opacity: 0, duration: 1.0, ease: "power2.in" }, at(56.6));
tl.to(backs, { opacity: 0, duration: 0.8, ease: "power2.in" }, at(56.8));
tl.to(conv.querySelector(".focus-halo"), { scale: 0.6, opacity: 0, duration: 0.8, ease: "power2.in", transformOrigin: "50% 50%" }, at(57.0));
tl.to(conv.querySelector(".focus"), { scale: 1.2, duration: 0.6, ease: "power2.in", transformOrigin: "50% 50%" }, at(57.0));
tl.to(conv.querySelector(".focus"), { opacity: 0, duration: 0.3 }, at(58.0));
