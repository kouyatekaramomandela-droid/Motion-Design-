/* FUTURA-Kouroussa — deterministic gold particle field.
   Every draw is a pure function of (t, options): no Math.random, no clocks, seek-safe. */
(function () {
  var FK = (window.FK = window.FK || {});

  FK.rng = function (seed) {
    var s = seed >>> 0;
    return function () {
      s = (Math.imul(s, 1664525) + 1013904223) >>> 0;
      return s / 4294967296;
    };
  };

  var GOLDS = ["245,197,24", "248,223,122", "184,134,11", "245,197,24", "243,238,227"];

  function smooth(x) { x = Math.max(0, Math.min(1, x)); return x * x * (3 - 2 * x); }
  function easeOut(x) { x = Math.max(0, Math.min(1, x)); return 1 - Math.pow(1 - x, 3); }

  /* Build the particle table once (index-seeded). */
  FK.makeField = function (n, seed) {
    var r = FK.rng(seed || 7), out = [];
    for (var i = 0; i < n; i++) {
      out.push({
        k: i / n,
        ang: i * 2.39996323 + r() * 0.35,
        rad: Math.sqrt(r()),
        size: 0.7 + Math.pow(r(), 3) * 2.6,
        tw: 0.6 + r() * 2.2,
        ph: r() * 6.283,
        col: GOLDS[(r() * GOLDS.length) | 0],
        drift: 0.4 + r() * 1.2,
        lx: r(),
        ly: r() - 0.5
      });
    }
    return out;
  };

  /* Scene 1: one spark (0.8 s) → thousands (1.6–4.6 s) → slow drift → collapse into a
     horizontal gold thread (9.0–10.4 s) that becomes the map outline of scene 2.
     o: {cx, cy, maxR, line:{x0,x1,y}} in canvas pixels. */
  FK.drawGenesis = function (ctx, field, t, o) {
    var W = ctx.canvas.width, H = ctx.canvas.height;
    ctx.clearRect(0, 0, W, H);
    if (t < 0.8) return;
    ctx.globalCompositeOperation = "lighter";
    var n = field.length;
    var born = t < 1.6 ? 1 : Math.max(1, Math.floor(n * Math.pow(Math.min(1, (t - 1.6) / 3.0), 1.7)));
    var collapse = smooth((t - 9.0) / 1.3);
    for (var i = 0; i < born; i++) {
      var p = field[i];
      var b = 1.6 + 3.0 * Math.pow(p.k, 1 / 1.7);
      var age = Math.max(0, t - b);
      var grow = easeOut(age / 2.2);
      var ang = p.ang + 0.18 * grow + 0.012 * age * p.drift;
      var rr = o.maxR * p.rad * grow + 7 * age * p.drift;
      var x = o.cx + Math.cos(ang) * rr * 1.25;
      var y = o.cy + Math.sin(ang) * rr * 0.82;
      if (collapse > 0) {
        var tx = o.line.x0 + (o.line.x1 - o.line.x0) * p.lx;
        var ty = o.line.y + p.ly * 6 * (1 - collapse);
        x += (tx - x) * collapse; y += (ty - y) * collapse;
      }
      var a = (0.45 + 0.55 * (0.5 + 0.5 * Math.sin(t * p.tw + p.ph))) * Math.min(1, age * 3 + (i === 0 ? 1 : 0));
      var s = p.size * (i === 0 ? 1.8 : 1);
      ctx.fillStyle = "rgba(" + p.col + "," + a.toFixed(3) + ")";
      ctx.beginPath(); ctx.arc(x, y, s, 0, 6.2832); ctx.fill();
    }
    // the first spark keeps a halo while it is alone
    if (t < 3.2) {
      var ha = t < 1.0 ? (t - 0.8) / 0.2 : 1 - smooth((t - 2.0) / 1.2);
      var g = ctx.createRadialGradient(o.cx, o.cy, 0, o.cx, o.cy, 90);
      g.addColorStop(0, "rgba(248,223,122," + (0.9 * ha).toFixed(3) + ")");
      g.addColorStop(0.15, "rgba(245,197,24," + (0.45 * ha).toFixed(3) + ")");
      g.addColorStop(1, "rgba(245,197,24,0)");
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(o.cx, o.cy, 90, 0, 6.2832); ctx.fill();
    }
    ctx.globalCompositeOperation = "source-over";
  };

  /* Ambient dust (any scene): slow drifting motes, pure function of t. */
  FK.drawDust = function (ctx, field, t, alpha) {
    var W = ctx.canvas.width, H = ctx.canvas.height;
    ctx.clearRect(0, 0, W, H);
    ctx.globalCompositeOperation = "lighter";
    for (var i = 0; i < field.length; i++) {
      var p = field[i];
      var x = ((p.lx * W + t * 9 * p.drift) % (W + 40)) - 20;
      var y = ((p.rad * H - t * 5 * p.drift) % H + H) % H;
      var a = alpha * (0.35 + 0.65 * (0.5 + 0.5 * Math.sin(t * p.tw * 0.6 + p.ph)));
      ctx.fillStyle = "rgba(" + p.col + "," + a.toFixed(3) + ")";
      ctx.beginPath(); ctx.arc(x, y, p.size * 0.8, 0, 6.2832); ctx.fill();
    }
    ctx.globalCompositeOperation = "source-over";
  };
})();
