// Scene 3 — Le fil perdu (27.4–42.6). Gold lines leave and fade toward the horizon; a question forms.
tl.fromTo($(".s3-map"), { opacity: 0, scale: 1.25, transformOrigin: "50% 50%" }, { opacity: 0.85, scale: 1, duration: 1.2, ease: "power2.out", transformOrigin: "50% 50%" }, at(27.6));
tl.fromTo($(".s3-horizon"), { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: 1.6, ease: "power2.out", transformOrigin: "0% 50%" }, at(28.4));
const lines = $(".s3-lines.only-" + FMT);
const flows = Array.from(lines.querySelectorAll(".flow"));
tl.fromTo(lines, { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 4.2, ease: "power1.inOut" }, at(28.9));
tl.fromTo(flows, { strokeDashoffset: 0 }, { strokeDashoffset: -560, duration: 13.6, ease: "none" }, at(28.9));
tl.to(flows, { opacity: 0.3, duration: 4.0, ease: "sine.inOut", stagger: 0.4 }, at(34.0));
tl.fromTo($(".s3-map .mines"), { opacity: 1 }, { opacity: 0.45, duration: 3.0 }, at(33.5));

// the question mark assembles in the void
const q = $("svg.s3-qmark");
tl.fromTo(q.querySelector(".q-path"), { clipPath: "inset(0% 0% 100% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 2.0, ease: "power1.inOut" }, at(33.0));
tl.fromTo(q.querySelector(".q-dot"), { scale: 0, transformOrigin: "50% 50%" }, { scale: 1, duration: 0.6, ease: "back.out(3)", transformOrigin: "50% 50%" }, at(35.0));
const words = splitWords($(".s3-q"));
tl.fromTo(words, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.8, ease: "power3.out", stagger: 0.07 }, at(34.5));
// held frame 38.5–41.5: only the question breathes
tl.fromTo(q, { scale: 1, transformOrigin: "50% 60%" }, { scale: 1.045, duration: 3.0, ease: "sine.inOut", yoyo: true, repeat: 1, transformOrigin: "50% 60%" }, at(35.6));
// exit: the void is covered by the page of scene 4
tl.to($$(".s3-map, .s3-horizon, .s3-q, svg.s3-qmark"), { opacity: 0, duration: 0.9, ease: "sine.in" }, at(41.3));
tl.to(lines, { opacity: 0, duration: 0.9, ease: "sine.in" }, at(41.3));
