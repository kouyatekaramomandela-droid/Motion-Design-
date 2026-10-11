"""Procedural score + UI sound design for the MADINA DIGITAL film (75.0 s, 48 kHz, deterministic; generated
locally, royalty-free).

Outputs: audio/music.wav (stereo bed, ducked under the narration), audio/sfx.wav (stereo UI sounds), audio/cues.json
Brief: minimal orchestral pad + light synth; a digital bell when the M closes; discreet UI clicks; a rising synth on
validation; a ping on each module; resolution, a short silence, then the cut.
120 BPM, bars of 2.0 s with downbeats at 0.4 + 2k s, so every module (32.4 + 2k) lands on a downbeat.
F major, I–V–vi–IV (F C Dm Bb). Duck from audio/vo_meta.json when it exists, else from audio/vo_plan.json.
Usage: <venv>/bin/python tools/synth_score.py   (from the project root; numpy + scipy)
"""
import json, wave
from pathlib import Path
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

SR, DUR = 48000, 75.0
N = int(SR * DUR)
RNG = np.random.default_rng(20261011)
BEAT, BAR, OFF = 0.5, 2.0, 0.4
t_all = np.arange(N) / SR


def midi(m): return 440.0 * 2 ** ((m - 69) / 12)
def interp(pts, t): xs, ys = zip(*pts); return np.interp(t, xs, ys)
def bandpass(x, lo, hi): return sosfilt(butter(2, [lo, hi], btype="band", fs=SR, output="sos"), x)
def lowpass(x, fc): return sosfilt(butter(2, fc, btype="low", fs=SR, output="sos"), x)
def pan(m, p): a = (p + 1) * np.pi / 4; return np.vstack([m * np.cos(a), m * np.sin(a)])


def place(buf, sig, t0):
    s = int(t0 * SR)
    if s >= buf.shape[-1]: return
    e = min(buf.shape[-1], s + sig.shape[-1]); buf[..., s:e] += sig[..., :e - s]


def make_ir(sec=2.2):
    n = int(sec * SR); t = np.arange(n) / SR; out = []
    for _ in range(2):
        x = bandpass(RNG.standard_normal(n) * np.exp(-t * 6.9 / sec), 200, 8000)
        out.append(np.concatenate([np.zeros(int(0.018 * SR)), x / np.sqrt(np.sum(x ** 2))]))
    return out
IR = make_ir()


def reverb(st, wet):
    o = np.zeros_like(st)
    for c in range(2): o[c] = fftconvolve(st[c], IR[c])[:st.shape[1]]
    return st * (1 - wet * 0.5) + o * wet


# intensity: calm logo → light build → steady product groove → lift on the benefits → resolution
I = interp([(0, 0.0), (0.5, 0.15), (6, 0.25), (12, 0.38), (22, 0.45), (30, 0.55), (32.4, 0.7), (56, 0.78),
            (57, 0.85), (66, 0.9), (72.4, 0.6), (74.2, 0.2), (74.6, 0.0), (75, 0.0)], t_all)
CH = {"F": [53, 57, 60, 65], "C": [52, 55, 60, 64], "Dm": [50, 53, 57, 62], "Bb": [50, 53, 58, 62], "Gm": [50, 55, 58, 62]}
ROOT = {"F": 41, "C": 36, "Dm": 38, "Bb": 34, "Gm": 43}
LOOP = ["F", "C", "Dm", "Bb"]
SPANS = [(0.0, 6.4, "F"), (6.4, 12.4, "Dm")]
t = 12.4; k = 0
while t < 72.4:
    SPANS.append((t, min(72.4, t + BAR), LOOP[k % 4])); t += BAR; k += 1
SPANS.append((72.4, 75.0, "F"))


def chord_at(tt):
    for s, e, c in SPANS:
        if s <= tt < e: return c
    return "F"


def pad():
    L = np.zeros(N); R = np.zeros(N)
    for s, e, c in SPANS:
        notes = CH[c] + ([CH[c][-1] + 12] if s >= 57 else [])
        a, b = max(0, s - 0.3), min(DUR, e + 1.2); n = int((b - a) * SR); tt = np.arange(n) / SR
        env = np.minimum(1, tt / 0.6) * np.clip((e - a + 0.9 - tt) / 0.9, 0, 1)
        for i, m in enumerate(notes):
            for det, side in ((-0.07, 0), (0.06, 1), (0.0, i % 2)):
                ph = np.cumsum(midi(m) * 2 ** (det / 12) * (1 + 0.002 * np.sin(2 * np.pi * 5 * tt + i)) / SR)
                tone = 0.6 * np.sin(2 * np.pi * ph) + 0.4 * (2 * (ph % 1) - 1)
                (L if side == 0 else R)[int(a * SR):int(a * SR) + n] += (tone * env * 0.05 / (1 + 0.3 * i))[:N - int(a * SR)]
    st = np.vstack([lowpass(L, 2600), lowpass(R, 2600)])
    return st * (0.4 + 0.6 * I)


def bass():
    out = np.zeros(N)
    for s, e, c in SPANS:
        if s < 12.4 or s >= 72.4: continue
        for b in range(4):
            tb = s + b * BEAT
            if tb >= e: break
            n = int(0.45 * SR); tt = np.arange(n) / SR; f = midi(ROOT[c] + (12 if b == 3 else 0))
            sig = (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)) * np.exp(-tt * 5) * np.minimum(1, tt / 0.005)
            place(out, sig * (0.16 if s >= 30 else 0.1), tb)
    return pan(out * (0.5 + 0.5 * I), 0.0)


def pluck(f, dur=0.9, bright=0.6):
    n = int(dur * SR); tt = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * f * h * tt) * np.exp(-tt * (4 + 3 * h)) for h, a in ((1, 1.0), (2, 0.5 * bright), (3, 0.25 * bright), (4, 0.12 * bright)))
    return s * np.minimum(1, tt / 0.003)


def arps():
    out = np.zeros((2, N))
    for s, e, c in SPANS:
        if s < 6.4 or s >= 72.4: continue
        step = BEAT / 2 if s >= 30 else BEAT
        tt, k = s, 0
        pool = [m for m in range(64, 89) if m % 12 in {n % 12 for n in CH[c]}]
        while tt < e - 0.05:
            m = pool[[0, 2, 1, 3, 2, 4, 3, 1][k % 8] % len(pool)]
            place(out, pan(pluck(midi(m), 0.7) * (0.06 if s < 30 else 0.075), 0.35 if k % 2 else -0.25), tt)
            tt += step; k += 1
    return out * (0.6 + 0.4 * I)


def kick(v=1.0):
    n = int(0.4 * SR); tt = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(48 + 90 * np.exp(-tt * 30)) / SR) * np.exp(-tt * 9) * v


def hat(v=1.0):
    n = int(0.08 * SR); tt = np.arange(n) / SR
    return bandpass(RNG.standard_normal(n), 6000, 14000) * np.exp(-tt * 60) * v


def drums():
    out = np.zeros((2, N))
    for s, e, c in SPANS:
        if s < 30 or s >= 72.4: continue
        for b in range(4):
            tb = s + b * BEAT
            if b in (0, 2): place(out, pan(kick(0.38), 0), tb)
            place(out, pan(hat(0.10), 0.3), tb + BEAT / 2)
    return out


def bell(f0=1318.5, v=1.0, dur=3.0):
    n = int(dur * SR); tt = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * f0 * r * tt) * np.exp(-tt * d) for r, a, d in ((1, 1, 1.4), (2.76, 0.42, 3), (5.4, 0.2, 5.5), (8.93, 0.08, 8)))
    return s * np.minimum(1, tt / 0.002) * v * 0.18


def click(v=1.0):
    n = int(0.03 * SR); tt = np.arange(n) / SR
    return bandpass(RNG.standard_normal(n), 2500, 9000) * np.exp(-tt * 260) * v * 0.22


def whoosh(dur=0.9, v=1.0):
    n = int(dur * SR); tt = np.arange(n) / SR; sh = np.sin(np.pi * tt / dur) ** 2
    return (bandpass(RNG.standard_normal(n), 300, 4000) * sh * 0.25 + np.sin(2 * np.pi * np.cumsum(90 - 40 * tt / dur) / SR) * sh * 0.2) * v


def rise(dur=0.7, v=1.0):
    n = int(dur * SR); tt = np.arange(n) / SR
    f = 440 * 2 ** (tt / dur * 1.0)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * np.sin(4 * np.pi * np.cumsum(f) / SR)) * np.minimum(1, tt / 0.02) * np.exp(-np.maximum(0, tt - dur * 0.7) * 12) * v * 0.12


def sfx():
    out = np.zeros((2, N)); cues = []
    def add(sig, t, p=0.0, label=""):
        place(out, pan(sig, p), t); cues.append({"t": round(t, 3), "label": label})
    add(bell(1318.5, 1.0), 2.2, 0, "M se referme")
    for t0, text, dur in ((13.3, "Diallo Aissatou", 1.0), (14.6, "+224 621 23 45 67", 1.0), (15.9, "exemple@gmail.com", 0.9),
                          (17.0, "........", 0.5), (17.7, "........", 0.5), (22.6, "exemple@gmail.com", 0.9), (23.8, "........", 0.5)):
        nch = len(text)
        for i in range(nch):
            add(click(0.55 + 0.25 * ((i * 7) % 3) / 2), t0 + dur * i / nch, 0.15, "frappe" if i == 0 else "")
    for t0 in (19.4, 24.65): add(click(1.6), t0, 0, "bouton")
    add(rise(0.7, 1.0), 19.75, 0, "validation")
    add(bell(1760.0, 0.6, 2.0), 20.0, 0.1, "coche")
    add(whoosh(0.9, 0.8), 25.0, 0, "volet")
    for k in range(12):
        add(bell([1046.5, 1174.7, 1318.5, 1568.0][k % 4], 0.38, 1.4), 32.4 + 2 * k, [-0.3, 0.3][k % 2], f"module {k + 1}")
    for t0 in (57.3, 58.9, 60.5, 62.7): add(whoosh(0.55, 0.45), t0, 0, "carte")
    for i in range(18): add(click(0.35), 66.9 + i * 0.09, 0.2, "compteur" if i == 0 else "")
    add(bell(1318.5, 0.5, 1.6), 70.2, 0, "Explorer")
    add(bell(698.5, 0.7, 3.2), 72.4, 0, "logo final")
    # v2 photo transitions (added last so the noise of the earlier sounds stays the same)
    add(whoosh(0.6, 0.55), 8.2, -0.2, "plan phare")
    add(whoosh(0.9, 0.5), 8.95, 0.1, "cadre vers carte")
    for k in range(1, 12): add(whoosh(0.5, 0.22), 32.4 + 2 * k - 0.4, [0.25, -0.25][k % 2], "photo module" if k == 1 else "")
    return reverb(out, 0.3), [c for c in cues if c["label"]]


def duck_envelope(db=-13.0):
    meta = Path("audio/vo_meta.json"); plan = Path("audio/vo_plan.json")
    if meta.exists():
        segs0 = [(u["start"], u["end"]) for u in json.loads(meta.read_text())["units"]]
    else:
        segs0 = [(u["at"], u["at"] + u["max"] * 0.9) for u in json.loads(plan.read_text())]
    segs = []
    for a, b in segs0:
        a, b = a - 0.12, b + 0.25
        if segs and a - segs[-1][1] < 0.6: segs[-1][1] = b
        else: segs.append([a, b])
    cr = 1000; tgt = np.ones(int(DUR * cr))
    for a, b in segs: tgt[int(a * cr):int(b * cr)] = 10 ** (db / 20)
    env = np.empty_like(tgt); g = 1.0
    at_, rl = 1 - np.exp(-1 / (0.08 * cr)), 1 - np.exp(-1 / (0.35 * cr))
    for i, x in enumerate(tgt): g += (x - g) * (at_ if x < g else rl); env[i] = g
    return np.interp(t_all, np.arange(len(env)) / cr, env), segs, ("vo_meta" if meta.exists() else "vo_plan")


def write(path, st, peak_db):
    st = st / (np.max(np.abs(st)) + 1e-9) * 10 ** (peak_db / 20)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(st.T, -1, 1) * 32767).astype(np.int16).tobytes())


def main():
    music = reverb(pad(), 0.35) + bass() + reverb(arps(), 0.3) + reverb(drums(), 0.1) * 0.8
    music *= np.clip(t_all / 0.6, 0, 1) * np.clip((74.4 - t_all) / 1.6, 0, 1)   # short silence before the cut
    duck, segs, src = duck_envelope()
    write("audio/music.wav", music * duck, -3.0)
    fx, cues = sfx()
    fx *= np.clip((74.6 - t_all) / 0.5, 0, 1)
    write("audio/sfx.wav", fx, -4.0)
    json.dump({"bpm": 120, "bar_s": BAR, "downbeat_offset": OFF, "duck_source": src, "duck_segments": [[round(a, 3), round(b, 3)] for a, b in segs],
               "sfx": cues}, open("audio/cues.json", "w"), indent=1, ensure_ascii=False)
    print("ok", src)


main()
