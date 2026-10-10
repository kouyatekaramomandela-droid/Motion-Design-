// Studio background for the whole film: the floor light breathes very slowly, the two particle layers drift
// upward at different speeds (depth).
tl.fromTo($$(".far"), { x: 0, y: 0 }, { x: -30, y: -70, duration: DUR, ease: "none" }, 0);
tl.fromTo($$(".near"), { x: 0, y: 0 }, { x: 40, y: -160, duration: DUR, ease: "none" }, 0);
tl.fromTo($(".studio-floor"), { opacity: 0.7 }, { opacity: 1, duration: DUR / 2, ease: "sine.inOut", yoyo: true, repeat: 1 }, 0);
