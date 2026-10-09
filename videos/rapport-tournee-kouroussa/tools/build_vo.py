"""Cut the narration take into its phrases and place each one on its scene of the 75 s film.

Source: ElevenLabs eleven_v4, voice « Florian » (FL0d5832ACnJkBaedeKX), take B (audio/src/take-b.mp3).
The take's 22 pauses (silencedetect -40 dB, 0.18 s) fall exactly on the punctuation of the script, so
every unit below is cut between two pauses (no transcription needed). Each axis word lands at the start
of its axis in S4; « l'eau potable / la santé / l'agriculture » light the three counters of S3;
« transmettre / plaider / suivre » drop the three columns of S5.

Outputs: audio/vo.wav (48 kHz mono, 75 s), audio/vo_meta.json (unit times), assets/captions/captions.json,
         exports/rapport_tournee.srt
Usage: python3 tools/build_vo.py   (from the project root)
"""
import json, os, subprocess, wave
import numpy as np

SR = 48000
FILM = 75.0
TEMPO = 0.96
SRC = "audio/src/take-b.mp3"

# speech units of take B: (src start, src end, text) — between the detected pauses
UNITS = [
    (0.000, 3.947, "Du dix-huit au vingt-sept septembre, nous sommes allés à la rencontre de Kouroussa."),
    (4.422, 5.232, "Quinze localités."),
    (5.598, 6.642, "Des centaines de voix."),
    (7.101, 7.613, "Partout,"),
    (7.910, 9.087, "trois urgences reviennent :"),
    (9.493, 10.209, "l'eau potable,"),
    (10.408, None, "la santé,"),          # split inside the unit at the quietest point (see split())
    (None, 12.032, "l'agriculture."),
    (12.637, 14.651, "De ces échanges sont nées huit priorités :"),
    (15.081, 15.921, "désenclavement,"),
    (16.185, 16.434, "eau,"),
    (16.654, 17.209, "santé,"),
    (17.462, 18.178, "éducation,"),
    (18.417, 19.213, "agriculture,"),
    (19.418, 20.103, "jeunesse,"),
    (20.294, 20.739, "femmes,"),
    (21.034, 22.559, "électricité et numérique."),
    (23.032, 24.159, "Elles guideront notre action :"),
    (24.559, 25.201, "transmettre,"),
    (25.464, 25.914, "plaider,"),
    (26.108, 26.689, "suivre,"),
    (26.904, 27.687, "et rendre compte."),
    (28.153, 29.249, "Kouroussa a parlé."),
    (29.696, 30.600, "Nous portons sa voix."),
]
# film time of each unit's first sound (index → seconds); consecutive units without an entry follow their
# predecessor with the take's own pause (scaled by TEMPO)
PLACE = {0: 0.8, 1: 7.0, 2: 9.6, 3: 18.4, 5: 20.9, 6: 22.2, 7: 23.4, 8: 25.2,
         9: 28.5, 10: 31.5, 11: 34.5, 12: 37.5, 13: 40.5, 14: 43.5, 15: 46.5, 16: 49.5,
         17: 53.0, 18: 55.2, 19: 57.6, 20: 60.0, 22: 67.6, 23: 69.6}

# burned-in caption cues (one line each, <= 34 characters); (first unit, text, share of the unit's
# length where the cue starts — for cues inside the long first unit)
CUES = [
    (0, "Du 18 au 27 septembre,", 0.0), (0, "nous sommes allés à la rencontre", 0.41), (0, "de Kouroussa.", 0.82),
    (1, "Quinze localités.", 0), (2, "Des centaines de voix.", 0), (3, "Partout,", 0), (4, "trois urgences reviennent :", 0),
    (5, "l’eau potable,", 0), (6, "la santé,", 0), (7, "l’agriculture.", 0),
    (8, "De ces échanges sont nées", 0.0), (8, "huit priorités :", 0.62),
    (9, "désenclavement,", 0), (10, "eau,", 0), (11, "santé,", 0), (12, "éducation,", 0), (13, "agriculture,", 0),
    (14, "jeunesse,", 0), (15, "femmes,", 0), (16, "électricité et numérique.", 0),
    (17, "Elles guideront notre action :", 0), (18, "transmettre,", 0), (19, "plaider,", 0),
    (20, "suivre, et rendre compte.", 0),
    (22, "Kouroussa a parlé.", 0, "srt-only"), (23, "Nous portons sa voix.", 0, "srt-only"),
]


def decode(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def stretch(seg):
    if abs(TEMPO - 1) < 1e-6: return seg
    p = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-i", "-",
                        "-af", f"atempo={TEMPO}", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                       input=seg.astype(np.float32).tobytes(), capture_output=True, check=True)
    return np.frombuffer(p.stdout, dtype=np.float32).copy()


def split(src, a, b, lo, hi):
    """Quietest 40 ms point between lo and hi (source seconds)."""
    w = int(0.04 * SR); best, bt = 1e9, lo
    for t in np.arange(lo, hi, 0.01):
        e = float(np.mean(src[int(t * SR):int(t * SR) + w] ** 2))
        if e < best: best, bt = e, t
    return round(float(bt + 0.02), 3)


def srt_time(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main():
    src = decode(SRC)
    units = [list(u) for u in UNITS]
    cut = split(src, units[6][0], units[7][1], units[6][0] + 0.4, units[7][1] - 0.6)
    units[6][1] = cut; units[7][0] = cut
    out = np.zeros(int(FILM * SR), dtype=np.float32)
    meta, t_prev_end, s_prev_end = [], None, None
    for i, (a, b, text) in enumerate(units):
        pa, pb = max(0.0, a - 0.06), b + 0.10
        seg = src[int(pa * SR):int(pb * SR)].copy()
        f = int(0.012 * SR); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
        seg = stretch(seg)
        at = PLACE[i] if i in PLACE else t_prev_end + (a - s_prev_end) / TEMPO
        s0 = int((at - (a - pa) / TEMPO) * SR)
        out[s0:s0 + len(seg)] += seg[:max(0, len(out) - s0)]
        end = at + (b - a) / TEMPO
        meta.append({"i": i, "text": text, "start": round(at, 3), "end": round(end, 3)})
        t_prev_end, s_prev_end = end, b
        print(f"{at:6.2f} → {end:6.2f}  {text}")
    peak = float(np.max(np.abs(out))); out *= (10 ** (-1.5 / 20)) / peak
    os.makedirs("audio", exist_ok=True)
    with wave.open("audio/vo.raw.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "audio/vo.raw.wav", "-af",
                    "highpass=f=70,acompressor=threshold=-24dB:ratio=2.2:attack=8:release=180:makeup=3dB,"
                    "alimiter=limit=0.85:attack=3:release=60,loudnorm=I=-16:TP=-1.5:LRA=9",
                    "-ar", str(SR), "-ac", "1", "audio/vo.wav"], check=True)
    os.remove("audio/vo.raw.wav")
    json.dump({"source": "ElevenLabs eleven_v4, voix « Florian » (FL0d5832ACnJkBaedeKX), prise B", "tempo": TEMPO,
               "units": meta}, open("audio/vo_meta.json", "w"), ensure_ascii=False, indent=1)
    cues, srt = [], []
    for c in CUES:
        u, text, share = c[0], c[1], c[2]
        m = meta[u]; start = m["start"] + share * (m["end"] - m["start"]) - 0.08
        cues.append({"text": text, "start": round(start, 3), "end": None, "unit": u, "burn": len(c) < 4})
    for k, c in enumerate(cues):
        nxt = cues[k + 1]["start"] if k + 1 < len(cues) else FILM
        own_end = meta[c["unit"]]["end"] + 0.9
        c["end"] = round(min(own_end, nxt - 0.04), 3)
    os.makedirs("assets/captions", exist_ok=True)
    json.dump([c for c in cues if c["burn"]], open("assets/captions/captions.json", "w"), ensure_ascii=False, indent=1)
    os.makedirs("exports", exist_ok=True)
    with open("exports/rapport_tournee.srt", "w") as f:
        for k, c in enumerate(cues, 1):
            f.write(f"{k}\n{srt_time(c['start'])} --> {srt_time(c['end'])}\n{c['text']}\n\n")


main()
