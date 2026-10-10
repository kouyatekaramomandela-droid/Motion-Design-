// S1 — Logo (0–6). The light pool opens; the M ribbon unfolds in space from left to right with a metallic
// glint; the chevron folds in (bell when the M closes, ~2.2 s); the two dots drop; MADINA and DIGITAL come
// forward from depth; the slogan writes itself in navy script, left to right.
tl.fromTo($(".pool"), { opacity: 0 }, { opacity: 1, duration: 1.2, ease: "sine.out" }, at(0));
const lk = $(".lockup");
tl.fromTo(lk, { rotationY: -28, rotationX: 8, scale: 0.92, transformPerspective: 1400, transformOrigin: "50% 40%" },
  { rotationY: 0, rotationX: 0, scale: 1, duration: 3.2, ease: "power3.out", transformPerspective: 1400, transformOrigin: "50% 40%" }, at(0.2));
// the M unfolds: a soft-edged wipe from the left leg to the right leg
tl.fromTo($(".lg-m"), { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 1.6, ease: "power2.inOut" }, at(0.4));
tl.fromTo($(".msheen i"), { x: 0 }, { x: pick(900, 1220), duration: 1.4, ease: "power2.inOut" }, at(1.9));
tl.fromTo($(".lg-chevron"), { opacity: 0, y: -40, scale: 0.6, transformOrigin: "50% 40%" }, { opacity: 1, y: 0, scale: 1, duration: 0.7, ease: "back.out(2)", transformOrigin: "50% 40%" }, at(1.7));
tl.fromTo([$(".lg-dot-l"), $(".lg-dot-r")], { opacity: 0, y: -60 }, { opacity: 1, y: 0, duration: 0.6, ease: "bounce.out", stagger: 0.12 }, at(2.2));
tl.fromTo($(".lg-madina"), { opacity: 0, scale: 1.18, y: 18, transformOrigin: "50% 75%" }, { opacity: 1, scale: 1, y: 0, duration: 0.9, ease: "power3.out", transformOrigin: "50% 75%" }, at(2.6));
tl.fromTo($(".lg-digital"), { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.8, ease: "power2.out" }, at(3.0));
// handwriting: the line is revealed left to right like a pen stroke
tl.fromTo($(".slogan .l1"), { clipPath: "inset(-20% 100% -20% 0%)" }, { clipPath: "inset(-20% 0% -20% 0%)", duration: 1.15, ease: "none" }, at(3.6));
tl.fromTo($(".slogan .l2"), { clipPath: "inset(-20% 100% -20% 0%)" }, { clipPath: "inset(-20% 0% -20% 0%)", duration: 0.75, ease: "none" }, at(4.75));
// exit: the lockup recedes and the light pool closes before the context shot
tl.to([lk, $(".slogan")], { opacity: 0, scale: 0.94, duration: 0.7, ease: "power2.in", transformOrigin: "50% 50%" }, at(5.5));
tl.to($(".pool"), { opacity: 0, duration: 0.8, ease: "sine.in" }, at(5.6));
