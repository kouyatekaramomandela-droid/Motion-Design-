"""Procedural score + sound design for FUTURA-Kouroussa 60 s (60.0 s, 48 kHz, deterministic).

Outputs (project-relative):
  assets/audio/music.wav   stereo bed, already ducked ~15 dB under every narration phrase
                           (strings pad, bass, kora by Karplus-Strong, light Manding percussion)
  assets/audio/sfx.wav     stereo: gold chimes on counters and reveals, light whooshes on transitions
  assets/audio/cues.json   SFX times and the duck envelope, so the picture can sync to the sound

Dramaturgy (client brief): slow (0-15 s) -> lively (15-38 s, the gold) -> calm (52-60 s).
96 BPM. D minor (the lack) resolving to F major (the promise). Rises between lines and on the signature.
Usage: python tools/synth_score.py   (needs numpy + scipy; run from the project root, after build_vo.py)
"""
import json, wave
import numpy as np
from scipy.signal import butter, sosfilt, sosfilt_zi, fftconvolve

SR = 48000
DUR = 60.0
N = int(SR * DUR)
RNG = np.random.default_rng(20261008)
BEAT = 60 / 96  # 96 BPM, one bar = 2.5 s
DUCK_DB = -15.0

def midi(m): return 440.0 * 2 ** ((m - 69) / 12)

def interp(points, t):
    xs, ys = zip(*points)
    return np.interp(t, xs, ys)

t_all = np.arange(N) / SR

# ---------------------------------------------------------------- intensity curve
INTENSITY = [(0, 0.0), (0.4, 0.05), (3.0, 0.12), (5.0, 0.18), (13.5, 0.24), (15.2, 0.52), (27.0, 0.64),
             (28.2, 0.20), (37.4, 0.18), (38.4, 0.36), (45.0, 0.5), (51.6, 0.6), (52.3, 0.86), (57.5, 0.9),
             (59.4, 0.35), (60.0, 0.0)]
I = interp(INTENSITY, t_all)

# ---------------------------------------------------------------- harmony
CH = {
    "Dm": [50, 53, 57, 62], "Bb": [46, 50, 53, 58], "F": [53, 57, 60, 65], "C": [48, 55, 60, 64],
    "Gm": [43, 50, 55, 58], "Asus": [45, 50, 57, 64],
}
ROOT = {"Dm": 38, "Bb": 34, "F": 41, "C": 36, "Gm": 43, "Asus": 45}
PROG = [(0.0, "Dm"), (5.0, "F"), (7.5, "C"), (10.0, "Dm"), (12.5, "Bb"), (15.0, "F"), (17.5, "C"),
        (20.0, "Dm"), (22.5, "Bb"), (25.0, "F"), (26.25, "C"), (28.0, "Dm"), (30.5, "Gm"), (33.0, "Dm"),
        (35.5, "Bb"), (37.0, "Asus"), (38.0, "F"), (40.5, "C"), (43.0, "Dm"), (45.5, "Bb"), (48.0, "F"),
        (50.5, "C"), (52.0, "F"), (54.5, "Bb"), (56.0, "C"), (57.5, "F")]
SPANS = [(s, PROG[i + 1][0] if i + 1 < len(PROG) else DUR, c) for i, (s, c) in enumerate(PROG)]

def chord_at(t):
    for s, e, c in SPANS:
        if s <= t < e: return c
    return PROG[-1][1]

# ---------------------------------------------------------------- helpers
def polyblep_saw(freq, n, phase0=0.0):
    dt = freq / SR
    ph = (phase0 + np.cumsum(np.full(n, dt))) % 1.0
    y = 2 * ph - 1
    m = ph < dt; x = ph[m] / dt; y[m] -= x + x - x * x - 1
    m = ph > 1 - dt; x = (ph[m] - 1) / dt; y[m] -= x * x + x + x + 1
    return y

def env_ar(n, a, r, sustain_len):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    e[:na] = np.linspace(0, 1, na) ** 1.6
    rs = min(int(sustain_len * SR), n)
    if rs < n:
        tail = np.linspace(1, 0, min(nr, n - rs)) ** 2
        e[rs:rs + len(tail)] *= tail
        e[rs + len(tail):] = 0
    return e

def lowpass_varying(x, cut, block=2048):
    out = np.zeros_like(x); zi = None
    for i in range(0, len(x), block):
        fc = float(np.clip(cut[min(i + block // 2, len(cut) - 1)], 80, 16000))
        sos = butter(2, fc, btype="low", fs=SR, output="sos")
        if zi is None: zi = sosfilt_zi(sos) * 0
        out[i:i + block], zi = sosfilt(sos, x[i:i + block], zi=zi)
    return out

def bandpass(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], btype="band", fs=SR, output="sos"), x)

def make_ir(seconds=2.6, predelay=0.02):
    n = int(seconds * SR)
    t = np.arange(n) / SR
    decay = np.exp(-t * 6.9 / seconds)
    irs = []
    for ch in range(2):
        noise = RNG.standard_normal(n) * decay
        noise = sosfilt(butter(1, [180, 7000], btype="band", fs=SR, output="sos"), noise)
        noise = np.concatenate([np.zeros(int(predelay * SR)), noise])
        irs.append(noise / np.sqrt(np.sum(noise ** 2)))
    return irs

IR = make_ir()

def reverb(stereo, wet):
    out = np.zeros_like(stereo)
    for ch in range(2):
        out[ch] = fftconvolve(stereo[ch], IR[ch])[:stereo.shape[1]]
    return stereo * (1 - wet * 0.5) + out * wet

def pan(mono, p):  # p in [-1, 1]
    a = (p + 1) * np.pi / 4
    return np.vstack([mono * np.cos(a), mono * np.sin(a)])

def place(buf, sig, t0):
    s = int(t0 * SR)
    if s >= buf.shape[-1]: return
    e = min(buf.shape[-1], s + sig.shape[-1])
    buf[..., s:e] += sig[..., :e - s]

# ---------------------------------------------------------------- strings pad
def strings_pad():
    L = np.zeros(N); R = np.zeros(N)
    for s, e, c in SPANS:
        notes = list(CH[c])
        if s < 5: notes = [38, 45, 50]                                  # opening drone only
        if s >= 52: notes = notes + [notes[-1] + 12]                    # upper octave on the signature
        start = max(0.0, s - 0.5); stop = min(DUR, e + 2.0)
        n = int((stop - start) * SR)
        env = env_ar(n, 1.4 if s > 0 else 3.0, 2.2, (e - start))
        for k, m in enumerate(notes):
            f = midi(m)
            for d, side in ((-0.09, 0), (0.0, 0), (0.08, 1), (0.15, 1), (-0.14, 0)):
                ff = f * 2 ** (d / 12)
                vib = 1 + 0.0025 * np.sin(2 * np.pi * (4.6 + 0.3 * k) * np.arange(n) / SR + k)
                ph = np.cumsum(ff * vib / SR)
                tone = 2 * (ph % 1.0) - 1
                seg = tone * env * (0.055 / (1 + 0.25 * k))
                tgt = L if side == 0 else R
                a = int(start * SR); tgt[a:a + n] += seg[:N - a]
    cut = 420 + 3200 * I ** 1.3
    L = lowpass_varying(L, cut); R = lowpass_varying(R, cut)
    g = 0.35 + 0.65 * I
    return np.vstack([L * g, R * g])

# ---------------------------------------------------------------- bass
def bass():
    out = np.zeros(N)
    for s, e, c in SPANS:
        if s < 15: continue
        f = midi(ROOT[c])
        n = int((min(DUR, e + 1.0) - s) * SR)
        tt = np.arange(n) / SR
        env = env_ar(n, 0.3, 0.9, e - s)
        sig = (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * 2 * f * tt)) * env
        place(out, sig * (0.10 if 28 <= s < 38 else 0.20), s)
    return pan(out * (0.4 + 0.6 * I), 0.0)

# ---------------------------------------------------------------- kora (Karplus-Strong)
def ks_pluck(freq, dur=2.2, bright=0.55, decay=0.996):
    n = int(dur * SR)
    p = int(round(SR / freq))
    burst = RNG.uniform(-1, 1, p)
    burst = bright * burst + (1 - bright) * np.convolve(burst, np.ones(4) / 4, mode="same")
    y = np.zeros(n + p + 1)
    y[:p] = burst
    for i in range(p, n, p):  # block-vectorised KS: each period depends on the previous one
        j = min(i + p, n)
        prev = y[i - p:j - p]; prev2 = y[i - p - 1:j - p - 1] if i - p - 1 >= 0 else np.concatenate([[0], y[i - p:j - p - 1]])
        y[i:j] = decay * 0.5 * (prev + prev2[:len(prev)])
    y = y[:n]
    y *= np.exp(-np.arange(n) / SR * 1.2)
    body = bandpass(y, 180, 2400) * 0.6 + y * 0.4
    att = np.minimum(1, np.arange(n) / (0.002 * SR))
    return body * att

def kora_notes():
    ev = []  # (time, midi, vel)
    for tt, m in ((0.5, 74), (1.9, 69), (3.3, 77)):          # opening: single notes around the spark
        ev.append((tt, m, 0.5))
    def ostinato(t0, t1, vel, step=BEAT / 2, sparse=False, melody=False):
        k = 0; tt = t0
        while tt < t1 - 0.05:
            c = chord_at(tt)
            tones = sorted({(n % 12) for n in CH[c]})
            pool = [m for m in range(50, 82) if (m % 12) in tones]
            pattern = [0, 4, 2, 5, 1, 4, 3, 6]
            idx = pattern[k % 8] + (2 if (k // 8) % 2 else 0)
            m = pool[min(idx, len(pool) - 1)]
            if not (sparse and k % 2):
                ev.append((tt, m, vel * (1.0 if k % 2 == 0 else 0.78)))
            if melody and k % 2 == 0:
                hi = [p for p in pool if p >= 72]
                mm = hi[[2, 1, 0, 1][(k // 2) % 4] % len(hi)]
                ev.append((tt + 0.01, mm, vel * 0.62))
            k += 1; tt += step
    ostinato(5.0, 15.0, 0.34, sparse=True)
    ostinato(15.0, 20.0, 0.44)
    ostinato(20.0, 27.6, 0.48, melody=True)
    ostinato(28.4, 37.8, 0.24, step=BEAT, sparse=True)
    ostinato(38.0, 44.0, 0.38)
    ostinato(44.0, 52.0, 0.44, melody=True)
    ostinato(52.0, 57.4, 0.50, melody=True)
    for i, m in enumerate([53, 57, 60, 65, 69, 72, 77]):      # final F major arpeggio, ringing out
        ev.append((57.5 + i * 0.22, m, 0.52 - i * 0.03))
    return ev

def kora():
    out = np.zeros(N)
    for tt, m, vel in kora_notes():
        place(out, ks_pluck(midi(m), dur=2.4 if tt > 57 else 1.8) * vel * 0.30, tt)
    return pan(out * (0.75 + 0.25 * I), 0.28)

# ---------------------------------------------------------------- percussion (light, Manding feel)
def dunun(vel=1.0):
    n = int(0.6 * SR); tt = np.arange(n) / SR
    f = 52 + 70 * np.exp(-tt * 28)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 7.5)
    click = bandpass(RNG.standard_normal(n), 900, 3000) * np.exp(-tt * 90) * 0.15
    return (body + click) * vel

def djembe_tone(vel=1.0):
    n = int(0.35 * SR); tt = np.arange(n) / SR
    body = np.sin(2 * np.pi * 330 * tt) * np.exp(-tt * 22) * 0.6
    skin = bandpass(RNG.standard_normal(n), 400, 2600) * np.exp(-tt * 40) * 0.55
    return (body + skin) * vel

def shaker(vel=1.0):
    n = int(0.12 * SR); tt = np.arange(n) / SR
    e = np.minimum(1, tt / 0.01) * np.exp(-tt * 38)
    return bandpass(RNG.standard_normal(n), 5000, 12000) * e * vel

def percussion():
    L = np.zeros((2, N))
    trip = BEAT / 3
    def bar(t0, kind, vel):
        # 12/8 grid: 4 beats x 3 triplets. kind 0 = shaker, 1 = + dunun, 2 = + djembe
        for b in range(4):
            tb = t0 + b * BEAT
            if kind >= 1 and b in (0, 2): place(L, pan(dunun(0.9 * vel), -0.1), tb)
            if kind >= 1 and b == 1: place(L, pan(dunun(0.45 * vel), -0.1), tb + 2 * trip)
            if kind >= 2 and b in (1, 3): place(L, pan(djembe_tone(0.55 * vel), 0.25), tb)
            if kind >= 2 and b == 3: place(L, pan(djembe_tone(0.35 * vel), 0.25), tb + 2 * trip)
            for k in range(3):
                place(L, pan(shaker((0.5 if k == 0 else 0.3) * vel), 0.45), tb + k * trip)
    def run(t0, t1, kind, vel):
        t = t0
        while t < t1 - 0.1: bar(t, kind, vel); t += 4 * BEAT
    run(7.5, 15.0, 0, 0.45)
    run(15.0, 27.5, 2, 0.85)
    for t in (30.5, 33.0, 35.5):                       # the lack: a lone heartbeat per bar
        place(L, pan(dunun(0.35), -0.1), t)
    run(40.5, 45.5, 0, 0.5)
    run(45.5, 52.0, 1, 0.6)
    run(52.0, 57.5, 1, 0.72)
    place(L, pan(dunun(0.75), -0.1), 57.5)
    return L

# ---------------------------------------------------------------- swells inside the bed
def swells():
    out = np.zeros((2, N))
    for t0, dur, vel in ((13.3, 1.9, 0.2), (50.6, 1.6, 0.16)):
        n = int(dur * SR); tt = np.arange(n) / SR
        place(out, pan(bandpass(RNG.standard_normal(n), 300, 6000) * (tt / dur) ** 3 * vel, 0.0), t0)
    n = int(2.5 * SR); tt = np.arange(n) / SR
    boom = np.sin(2 * np.pi * np.cumsum(40 + 50 * np.exp(-tt * 6)) / SR) * np.exp(-tt * 1.8) * 0.35
    place(out, pan(boom, 0.0), 15.2)
    return out

# ---------------------------------------------------------------- duck under the narration
def duck_envelope():
    phrases = json.load(open("assets/audio/vo_meta.json"))["phrases"]
    segs = []
    for p in phrases:
        a, b = p["words"][0]["s"] - 0.12, p["words"][-1]["e"] + 0.25
        if segs and a - segs[-1][1] < 0.6: segs[-1][1] = b   # no pumping inside a sentence
        else: segs.append([a, b])
    cr = 1000  # control rate
    tgt = np.ones(int(DUR * cr))
    for a, b in segs: tgt[int(a * cr):int(b * cr)] = 10 ** (DUCK_DB / 20)
    env = np.empty_like(tgt); g = 1.0
    att, rel = 1 - np.exp(-1 / (0.08 * cr)), 1 - np.exp(-1 / (0.40 * cr))
    for i, x in enumerate(tgt):
        g += (x - g) * (att if x < g else rel); env[i] = g
    return np.interp(t_all, np.arange(len(env)) / cr, env), segs

# ---------------------------------------------------------------- SFX: chimes + whooshes
def chime(f0=1568.0, vel=1.0, dur=3.0):
    n = int(dur * SR); tt = np.arange(n) / SR
    sig = np.zeros(n)
    for ratio, amp, dec in ((1.0, 1.0, 1.6), (2.76, 0.45, 3.2), (5.40, 0.22, 5.5), (8.93, 0.10, 8.0)):
        sig += amp * np.sin(2 * np.pi * f0 * ratio * tt) * np.exp(-tt * dec)
    sig *= np.minimum(1, tt / 0.003)
    return sig * vel * 0.16

def whoosh(dur=1.8, rev=False, vel=1.0):
    n = int(dur * SR); tt = np.arange(n) / SR
    shape = np.sin(np.pi * np.clip(tt / dur, 0, 1)) ** 2
    noise = RNG.standard_normal(n)
    lo = bandpass(noise, 120, 900) * shape
    sub = np.sin(2 * np.pi * np.cumsum(70 - 25 * tt / dur) / SR) * shape * 0.35
    sig = (lo * 0.32 + sub) * vel
    return sig[::-1].copy() if rev else sig

NOTES_GOLD = [1396.9, 1568.0, 1760.0, 2093.0, 2349.3, 1174.7]
CHIMES = [  # (time, pitch index, velocity, label)
    (0.4, 1, 0.9, "f1 spark"),
    (18.9, 0, 0.7, "f3 mine 1"), (19.4, 1, 0.7, "f3 mine 2"), (19.9, 2, 0.75, "f3 mine 3"),
    (23.3, 3, 0.9, "f3 counter lands"),
    (42.0, 1, 0.85, "f5 logo complete"),
    (46.98, 0, 0.6, "f5 contributions"), (48.6, 1, 0.6, "f5 audits"), (49.84, 2, 0.65, "f5 communities"),
    (52.4, 0, 0.6, "f6 water"), (53.2, 2, 0.6, "f6 school"), (54.0, 3, 0.6, "f6 health post"),
    (55.6, 1, 0.8, "f6 logo"),
]
WHOOSHES = [  # (time, reversed, velocity, label)
    (4.5, False, 0.55, "f1→f2"), (7.6, False, 0.3, "f2 river→quarter"), (10.1, False, 0.3, "f2 quarter→market"),
    (14.5, False, 0.6, "f2→f3"), (27.4, False, 0.55, "f3→f4 gold lines leave"), (37.4, True, 0.6, "f4→f5 lines return"),
    (51.5, False, 0.55, "f5→f6"), (54.9, False, 0.45, "f6 band"),
]

def sfx():
    out = np.zeros((2, N))
    for i, (tt, p, v, _) in enumerate(CHIMES):
        place(out, pan(chime(NOTES_GOLD[p], v), [-0.35, 0.3, -0.1, 0.4, -0.25][i % 5]), tt)
    for tt, rev, v, _ in WHOOSHES:
        place(out, pan(whoosh(1.4, rev, v), 0.0), tt)
    return reverb(out, 0.45)

# ---------------------------------------------------------------- mix + write
def write_wav(path, stereo, peak_db):
    stereo = stereo / (np.max(np.abs(stereo)) + 1e-9) * 10 ** (peak_db / 20)
    pcm = (np.clip(stereo.T, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

def main():
    pad = reverb(strings_pad(), 0.35)
    kr = reverb(kora(), 0.30)
    perc = reverb(percussion(), 0.15)
    music = pad + bass() + kr * 1.1 + perc * 0.8 + reverb(swells(), 0.3)
    music *= np.clip(t_all / 0.8, 0, 1) * np.clip((59.95 - t_all) / 1.0, 0, 1)
    duck, segs = duck_envelope()
    write_wav("assets/audio/music.wav", music * duck, -3.0)
    write_wav("assets/audio/sfx.wav", sfx(), -4.0)
    json.dump({"chimes": [{"t": c[0], "label": c[3]} for c in CHIMES],
               "whooshes": [{"t": w[0], "label": w[3], "reversed": w[1]} for w in WHOOSHES],
               "duck_db": DUCK_DB, "duck_segments": [[round(a, 3), round(b, 3)] for a, b in segs],
               "chords": [{"t": s, "chord": c} for s, c in PROG]},
              open("assets/audio/cues.json", "w"), indent=1)
    print("ok")

main()
