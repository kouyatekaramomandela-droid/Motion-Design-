"""Procedural score for the 75 s report film (75.0 s, 48 kHz, deterministic, generated locally: royalty-free).

Outputs (project-relative):
  audio/music.wav   stereo bed, already ducked ~15 dB under every narration phrase
                    (strings pad, bass, kora by Karplus-Strong, very light Manding percussion)
  audio/cues.json   chord grid and the duck envelope

Light orchestral bed with kora touches, sober (client brief). 80 BPM: one bar = 3.0 s = one axis of S4,
bar lines at 1.0 + 3k s, so every axis word (28.5 + 3k) falls just after a downbeat.
S1 drone → S2 gentle kora → S3 low and serious (D minor) → S4 steady pulse → S5 lift → S6 resolution in F.
Usage: python tools/synth_score.py   (needs numpy + scipy; run from the project root, after build_vo.py)
"""
import json, wave
import numpy as np
from scipy.signal import butter, sosfilt, sosfilt_zi, fftconvolve

SR = 48000
DUR = 75.0
N = int(SR * DUR)
RNG = np.random.default_rng(20261008)
BEAT = 60 / 80  # 80 BPM, one bar = 3.0 s
DUCK_DB = -15.0

def midi(m): return 440.0 * 2 ** ((m - 69) / 12)

def interp(points, t):
    xs, ys = zip(*points)
    return np.interp(t, xs, ys)

t_all = np.arange(N) / SR

# ---------------------------------------------------------------- intensity curve
INTENSITY = [(0, 0.0), (0.5, 0.06), (4.0, 0.14), (7.0, 0.22), (17.5, 0.28), (19.0, 0.18), (27.0, 0.22),
             (28.0, 0.40), (40.0, 0.46), (51.5, 0.52), (52.5, 0.62), (64.0, 0.70), (67.0, 0.56), (71.5, 0.6),
             (74.0, 0.25), (75.0, 0.0)]
I = interp(INTENSITY, t_all)

# ---------------------------------------------------------------- harmony
CH = {
    "Dm": [50, 53, 57, 62], "Bb": [46, 50, 53, 58], "F": [53, 57, 60, 65], "C": [48, 55, 60, 64],
    "Gm": [43, 50, 55, 58], "Asus": [45, 50, 57, 64], "Am": [45, 52, 57, 60],
}
ROOT = {"Dm": 38, "Bb": 34, "F": 41, "C": 36, "Gm": 43, "Asus": 45, "Am": 45}
PROG = [(0.0, "F"), (7.0, "F"), (10.0, "C"), (13.0, "Dm"), (16.0, "Bb"), (19.0, "Dm"), (22.0, "Gm"),
        (25.0, "Asus"), (28.0, "F"), (31.0, "C"), (34.0, "Dm"), (37.0, "Bb"), (40.0, "F"), (43.0, "C"),
        (46.0, "Bb"), (49.0, "C"), (52.0, "F"), (55.0, "Am"), (58.0, "Bb"), (61.0, "C"), (64.0, "Bb"),
        (67.0, "F"), (70.0, "Bb"), (71.5, "F")]
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
        if s < 7: notes = [41, 48, 53, 57]                              # opening: open F
        if s >= 52: notes = notes + [notes[-1] + 12]                    # upper octave from the recommendations
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
        if s < 7: continue
        f = midi(ROOT[c])
        n = int((min(DUR, e + 1.0) - s) * SR)
        tt = np.arange(n) / SR
        env = env_ar(n, 0.3, 0.9, e - s)
        sig = (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * 2 * f * tt)) * env
        place(out, sig * (0.12 if 19 <= s < 28 else 0.17), s)
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
    for tt, m in ((1.0, 72), (2.5, 69), (4.0, 77)):          # opening: three single notes
        ev.append((tt, m, 0.45))
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
                ev.append((tt + 0.01, mm, vel * 0.6))
            k += 1; tt += step
    ostinato(7.0, 18.6, 0.30, sparse=True)
    ostinato(19.0, 27.6, 0.18, step=BEAT, sparse=True)
    ostinato(28.0, 52.0, 0.36)
    ostinato(52.0, 66.6, 0.40, melody=True)
    ostinato(67.0, 71.4, 0.30, sparse=True)
    for i, m in enumerate([53, 57, 60, 65, 69, 72, 77]):      # final F major arpeggio, ringing out
        ev.append((71.5 + i * 0.24, m, 0.46 - i * 0.03))
    return ev

def kora():
    out = np.zeros(N)
    for tt, m, vel in kora_notes():
        place(out, ks_pluck(midi(m), dur=2.6 if tt > 71 else 1.8) * vel * 0.30, tt)
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
    for t in (19.0, 22.0, 25.0):                      # S3: a lone low heartbeat per bar
        place(L, pan(dunun(0.3), -0.1), t)
    run(28.0, 52.0, 1, 0.42)
    run(52.0, 64.0, 1, 0.5)
    run(64.0, 67.0, 0, 0.4)
    place(L, pan(dunun(0.55), -0.1), 67.0)
    place(L, pan(dunun(0.45), -0.1), 71.5)
    return L

# ---------------------------------------------------------------- swells inside the bed
def swells():
    out = np.zeros((2, N))
    for t0, dur, vel in ((26.4, 1.6, 0.10), (50.6, 1.4, 0.09), (65.6, 1.4, 0.08)):
        n = int(dur * SR); tt = np.arange(n) / SR
        place(out, pan(bandpass(RNG.standard_normal(n), 300, 5000) * (tt / dur) ** 3 * vel, 0.0), t0)
    return out

# ---------------------------------------------------------------- duck under the narration
def duck_envelope():
    """-15 dB under phrases; only -8 dB under a lone short word (the axis words of S4 every 3 s, the verbs
    of S5), so the bed does not pump on each word."""
    units = json.load(open("audio/vo_meta.json"))["units"]
    segs = []
    for p in units:
        a, b, spoken = p["start"] - 0.15, p["end"] + 0.3, p["end"] - p["start"]
        if segs and a - segs[-1][1] < 0.6:   # no pumping inside a sentence
            segs[-1][1] = b; segs[-1][3] += spoken
        else: segs.append([a, b, 0.0, spoken])
    for sg in segs: sg[2] = DUCK_DB if sg[3] > 1.0 else -8.0
    segs = [sg[:3] for sg in segs]
    cr = 1000  # control rate
    tgt = np.ones(int(DUR * cr))
    for a, b, d in segs: tgt[int(a * cr):int(b * cr)] = 10 ** (d / 20)
    env = np.empty_like(tgt); g = 1.0
    att, rel = 1 - np.exp(-1 / (0.08 * cr)), 1 - np.exp(-1 / (0.40 * cr))
    for i, x in enumerate(tgt):
        g += (x - g) * (att if x < g else rel); env[i] = g
    return np.interp(t_all, np.arange(len(env)) / cr, env), segs

# ---------------------------------------------------------------- mix + write
def write_wav(path, stereo, peak_db):
    stereo = stereo / (np.max(np.abs(stereo)) + 1e-9) * 10 ** (peak_db / 20)
    pcm = (np.clip(stereo.T, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

def main():
    pad = reverb(strings_pad(), 0.38)
    kr = reverb(kora(), 0.32)
    perc = reverb(percussion(), 0.18)
    music = pad + bass() + kr * 1.05 + perc * 0.6 + reverb(swells(), 0.3)
    music *= np.clip(t_all / 1.2, 0, 1) * np.clip((74.9 - t_all) / 2.2, 0, 1)
    duck, segs = duck_envelope()
    write_wav("audio/music.wav", music * duck, -3.0)
    json.dump({"bpm": 80, "bar_s": 3.0, "duck_db": DUCK_DB, "duck_segments": [[round(a, 3), round(b, 3), d] for a, b, d in segs],
               "chords": [{"t": s, "chord": c} for s, c in PROG]}, open("audio/cues.json", "w"), indent=1)
    print("ok")

main()
