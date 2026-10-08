"""Procedural score + sound design for FUTURA-Kouroussa (120.0 s, 48 kHz, deterministic).

Outputs (project-relative):
  assets/audio/music.wav   stereo bed: strings pad, bass, kora (Karplus-Strong), soft percussion
  assets/audio/sfx.wav     stereo: gold chimes on particle appearances, low whooshes on transitions
  assets/audio/cues.json   every SFX time, so the picture can sync to the sound

Dramaturgy (client brief): rises to scene 5 (58 s), peaks in scene 6 (75–95 s), resolves softly
in scene 8 (110–120 s). D minor (the lack) resolving to F major (the promise).
Usage: python tools/synth_score.py   (needs numpy + scipy; run from the project root)
"""
import json, wave
import numpy as np
from scipy.signal import butter, sosfilt, sosfilt_zi, fftconvolve

SR = 48000
DUR = 120.0
N = int(SR * DUR)
RNG = np.random.default_rng(20261008)
BEAT = 60 / 72  # 72 BPM

def midi(m): return 440.0 * 2 ** ((m - 69) / 12)

def interp(points, t):
    xs, ys = zip(*points)
    return np.interp(t, xs, ys)

t_all = np.arange(N) / SR

# ---------------------------------------------------------------- intensity curve
INTENSITY = [(0, 0.0), (1.0, 0.08), (10, 0.15), (20, 0.25), (28, 0.22), (38.5, 0.18), (42, 0.3),
             (50, 0.42), (57.5, 0.6), (58.5, 0.72), (74, 0.82), (75.5, 1.0), (93, 1.0), (95, 0.66),
             (108, 0.6), (110, 0.5), (115, 0.42), (118.5, 0.18), (119.8, 0.0), (120, 0.0)]
I = interp(INTENSITY, t_all)

# ---------------------------------------------------------------- harmony
CH = {
    "Dm": [50, 53, 57, 62], "Bb": [46, 50, 53, 58], "F": [53, 57, 60, 65], "C": [48, 55, 60, 64],
    "Gm": [43, 50, 55, 58], "A": [45, 52, 57, 61], "Asus": [45, 50, 57, 64],
}
ROOT = {"Dm": 38, "Bb": 34, "F": 41, "C": 36, "Gm": 43, "A": 45, "Asus": 45}
PROG = [(0.0, "Dm"), (14.5, "Bb"), (19.0, "F"), (23.5, "C"), (28.0, "Gm"), (31.5, "Dm"), (35.0, "Bb"),
        (38.5, "Asus"), (42.0, "Dm"), (46.0, "Bb"), (50.0, "C"), (54.0, "A"), (58.5, "F"), (62.5, "C"),
        (66.5, "Dm"), (70.5, "Bb"), (75.0, "F"), (78.3, "C"), (81.6, "Dm"), (85.0, "Bb"), (88.3, "F"),
        (91.6, "C"), (95.0, "F"), (98.7, "Bb"), (102.4, "Dm"), (106.1, "C"), (110.0, "Bb"), (112.5, "C"),
        (115.0, "F")]
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
    for idx, (s, e, c) in enumerate(SPANS):
        notes = list(CH[c])
        if s >= 75 and s < 95: notes = notes + [notes[-1] + 12]       # upper octave at the peak
        if s < 10: notes = [38, 45, 50]                                 # opening drone only
        start = max(0.0, s - 0.6); stop = min(DUR, e + 2.2)
        n = int((stop - start) * SR)
        env = env_ar(n, 1.6 if s > 0 else 3.5, 2.6, (e - start))
        for k, m in enumerate(notes):
            f = midi(m)
            for d, side in ((-0.09, 0), (0.0, 0), (0.08, 1), (0.15, 1), (-0.14, 0)):
                ff = f * 2 ** (d / 12)
                vib = 1 + 0.0025 * np.sin(2 * np.pi * (4.6 + 0.3 * k) * np.arange(n) / SR + k)
                ph = np.cumsum(ff * vib / SR)
                tone = 2 * (ph % 1.0) - 1
                gain = 0.055 / (1 + 0.25 * k)
                seg = tone * env * gain
                tgt = L if side == 0 else R
                a = int(start * SR); tgt[a:a + n] += seg
    cut = 420 + 3200 * I ** 1.3
    L = lowpass_varying(L, cut); R = lowpass_varying(R, cut)
    g = 0.35 + 0.65 * I
    return np.vstack([L * g, R * g])

# ---------------------------------------------------------------- bass
def bass():
    out = np.zeros(N)
    for s, e, c in SPANS:
        if s < 42: continue
        f = midi(ROOT[c])
        n = int((min(DUR, e + 1.0) - s) * SR)
        tt = np.arange(n) / SR
        env = env_ar(n, 0.35, 1.0, e - s)
        sig = (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * 2 * f * tt)) * env
        place(out, sig * 0.20, s)
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
    # scene 1: sparse single notes around the first particles
    for tt, m in ((0.8, 74), (2.4, 69), (3.9, 77), (5.6, 74), (7.6, 69)):
        ev.append((tt, m, 0.55))
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
    ostinato(10.0, 38.5, 0.42)
    ostinato(38.5, 42.0, 0.30, sparse=True)
    ostinato(42.0, 58.3, 0.48)
    ostinato(58.6, 75.0, 0.55, melody=True)
    ostinato(75.0, 95.0, 0.60, melody=True)
    ostinato(95.0, 110.0, 0.50)
    ostinato(110.0, 113.8, 0.40, sparse=True)
    # final arpeggio in F major, rising and ringing out
    for i, m in enumerate([53, 57, 60, 65, 69, 72, 77]):
        ev.append((115.0 + i * 0.28, m, 0.55 - i * 0.03))
    return ev

def kora():
    out = np.zeros(N)
    for tt, m, vel in kora_notes():
        place(out, ks_pluck(midi(m), dur=2.4 if tt > 114 else 1.8) * vel * 0.30, tt)
    g = 0.75 + 0.25 * I
    g = np.where(t_all > 116.5, g * np.clip((120 - t_all) / 3.5, 0, 1), g)
    return pan(out * g, 0.28)

# ---------------------------------------------------------------- percussion (soft, Manding feel)
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
    def bar_pattern(t0, kind, vel):
        # 12/8 grid: 4 beats x 3 triplets
        for b in range(4):
            tb = t0 + b * BEAT
            if kind >= 1 and b in (0, 2): place(L, pan(dunun(0.9 * vel), -0.1), tb)
            if kind >= 1 and b == 1: place(L, pan(dunun(0.45 * vel), -0.1), tb + 2 * trip)
            if kind >= 2 and b in (1, 3): place(L, pan(djembe_tone(0.55 * vel), 0.25), tb)
            if kind >= 2 and b == 3: place(L, pan(djembe_tone(0.35 * vel), 0.25), tb + 2 * trip)
            if kind >= 1:
                for k in range(3):
                    place(L, pan(shaker((0.5 if k == 0 else 0.3) * vel), 0.45), tb + k * trip)
    bar = 4 * BEAT
    t = 46.0
    while t < 58.0:                     # heartbeat pulse building into the birth
        place(L, pan(dunun(0.45 + 0.04 * (t - 46)), -0.1), t); t += bar / 2
    t = 58.6
    while t < 75.0 - 0.1: bar_pattern(t, 1, 0.75); t += bar
    t = 75.0
    while t < 94.5 - 0.1: bar_pattern(t, 2, 0.95); t += bar
    t = 95.0
    while t < 109.0 - 0.1: bar_pattern(t, 1, 0.55); t += bar
    place(L, pan(dunun(0.7), -0.1), 115.0)
    return L

# ---------------------------------------------------------------- risers / impacts inside the bed
def birth_swell():
    out = np.zeros((2, N))
    n = int(4.0 * SR); tt = np.arange(n) / SR
    sw = bandpass(RNG.standard_normal(n), 300, 6000) * (tt / 4.0) ** 3 * 0.22
    place(out, pan(sw, 0.0), 54.5)
    n2 = int(3.0 * SR); tt2 = np.arange(n2) / SR
    boom = np.sin(2 * np.pi * np.cumsum(40 + 50 * np.exp(-tt2 * 6)) / SR) * np.exp(-tt2 * 1.6) * 0.5
    place(out, pan(boom, 0.0), 58.5)
    return out

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
    (0.8, 1, 1.0, "s1 first particle"), (1.9, 3, 0.5, "s1 particles multiply"), (2.3, 4, 0.45, "s1"),
    (2.8, 2, 0.4, "s1"), (5.6, 0, 0.55, "s1 counter lands"),
    (14.0, 1, 0.7, "s2 mine 1"), (14.7, 2, 0.7, "s2 mine 2"), (15.4, 3, 0.7, "s2 mine 3"),
    (58.6, 3, 1.0, "s5 burst"), (58.75, 1, 0.8, "s5 burst"), (58.9, 4, 0.7, "s5 burst"),
    (61.0, 2, 0.6, "s5 nugget lands in the hand"),
    (88.6, 1, 0.75, "s6 validation 1"), (90.1, 2, 0.75, "s6 validation 2"), (91.6, 3, 0.85, "s6 validation 3"),
    (96.6, 0, 0.7, "s7 water"), (97.35, 2, 0.7, "s7 school"), (98.35, 3, 0.7, "s7 health post"),
    (111.5, 1, 0.9, "s8 logo"),
]
WHOOSHES = [  # (time, reversed, velocity, label)
    (8.9, False, 0.8, "s1→s2"), (26.8, False, 0.7, "s2→s3"), (40.8, False, 0.6, "s3→s4"),
    (55.6, True, 0.9, "s4 convergence (inhale)"), (73.4, False, 0.8, "s5→s6"), (93.6, False, 0.8, "s6→s7"),
    (108.6, False, 0.7, "s7→s8"),
]

def sfx():
    out = np.zeros((2, N))
    for i, (tt, p, v, _) in enumerate(CHIMES):
        place(out, pan(chime(NOTES_GOLD[p], v), [-0.35, 0.3, -0.1, 0.4, -0.25][i % 5]), tt)
    for tt, rev, v, _ in WHOOSHES:
        place(out, pan(whoosh(1.8, rev, v), 0.0), tt)
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
    music = pad * 1.0 + bass() + kr * 1.1 + perc * 0.9 + reverb(birth_swell(), 0.3)
    fade_in = np.clip(t_all / 1.0, 0, 1); fade_out = np.clip((119.9 - t_all) / 1.2, 0, 1)
    music *= fade_in * fade_out
    write_wav("assets/audio/music.wav", music, -3.0)
    write_wav("assets/audio/sfx.wav", sfx(), -4.0)
    json.dump({"chimes": [{"t": c[0], "label": c[3]} for c in CHIMES],
               "whooshes": [{"t": w[0], "label": w[3], "reversed": w[1]} for w in WHOOSHES],
               "chords": [{"t": s, "chord": c} for s, c in PROG]},
              open("assets/audio/cues.json", "w"), indent=1)
    print("ok")

main()
