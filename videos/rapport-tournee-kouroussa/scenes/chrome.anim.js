// Fixed elements (0–75): emblem and Assemblée Nationale at the top, flag + Simandou 2040 + « Guinée » at the
// bottom; they settle in during the first second and stay. Fade to white over the last second (74–75).
tl.fromTo($$(".em-rg, .em-an"), { opacity: 0, y: -10 }, { opacity: 1, y: 0, duration: 0.8, ease: "power2.out", stagger: 0.15 }, at(0.3));
tl.fromTo($(".plaque"), { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.8, ease: "power2.out" }, at(0.6));
tl.fromTo($(".fade-white"), { opacity: 0 }, { opacity: 1, duration: 1.0, ease: "sine.inOut" }, at(74.0));
