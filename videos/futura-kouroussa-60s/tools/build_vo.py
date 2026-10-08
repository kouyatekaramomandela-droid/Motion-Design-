"""Cut the narration take into phrases and place each one on its shot of the 60 s film.

The ElevenLabs v3 take reads the whole text in one breath; the client direction asks for real
pauses between ideas and a calm pace. Each phrase is cut between words (from the transcript),
slowed by TEMPO with pitch preserved, and placed at its film time.

Outputs: assets/audio/vo.wav (48 kHz mono, 60.0 s), assets/audio/vo_meta.json, assets/captions/captions.json
Usage: python tools/build_vo.py   (from the project root)
"""
import json, os, subprocess, wave
import numpy as np

SR = 48000
FILM = 60.0
TEMPO = 0.90
SRC = "assets/audio/src/take-b.mp3"
WORDS = "assets/audio/src/take-b.words.json"

# (first word, last word, film start, caption text — verbatim script)
PHRASES = [
    (0, 0, 2.2, None),  # « Kouroussa. » — already the on-screen title
    (1, 6, 5.6, "Ici, il y a un fleuve,"),
    (7, 10, 8.1, "des quartiers qui vivent,"),
    (11, 21, 10.6, "et des familles qui travaillent chaque jour pour construire leur avenir."),
    (22, 30, 15.8, "Et sous cette terre, il y a de l'or."),
    (31, 32, 19.8, "Trois mines,"),
    (33, 41, 22.0, "et plus de deux milliards de dollars chaque année."),
    (42, 50, 28.3, "Pourtant, dans beaucoup de villages, l'eau potable manque encore."),
    (51, 55, 32.6, "Des écoles attendent d'être équipées."),
    (56, 63, 35.0, "Des centres de santé n'ont même pas d'électricité."),
    (64, 72, 38.4, "C'est pourquoi la mission parlementaire a recommandé FUTURA-Kouroussa."),
    (73, 75, 43.4, "Un fonds clair,"),
    (76, 82, 44.9, "où chaque contribution des mines est suivie,"),
    (83, 87, 47.6, "où les comptes sont audités,"),
    (88, 96, 49.4, "et où les communautés ont leur mot à dire."),
    (97, 103, 55.8, None),  # signature — already on screen
]

def decode(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()

def stretch(seg):
    p = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-i", "-",
                        "-af", f"atempo={TEMPO}", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                       input=seg.astype(np.float32).tobytes(), capture_output=True, check=True)
    return np.frombuffer(p.stdout, dtype=np.float32).copy()

def main():
    src = decode(SRC)
    words = json.load(open(WORDS))["words"]
    out = np.zeros(int(FILM * SR), dtype=np.float32)
    meta, cues = [], []
    for i, (a, b, at, text) in enumerate(PHRASES):
        # cut halfway into the gaps around the phrase so no word is clipped
        t0 = words[a]["start"] - (0.06 if a == 0 else min(0.12, (words[a]["start"] - words[a - 1]["end"]) / 2))
        t1 = words[b]["end"] + (0.25 if b == len(words) - 1 else min(0.15, (words[b + 1]["start"] - words[b]["end"]) / 2))
        seg = src[int(t0 * SR):int(t1 * SR)].copy()
        f = int(0.015 * SR); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
        seg = stretch(seg)
        s = int(at * SR)
        out[s:s + len(seg)] += seg[:max(0, len(out) - s)]
        lead = (words[a]["start"] - t0) / TEMPO
        fw = [{"w": w["text"], "s": round(at + lead + (w["start"] - words[a]["start"]) / TEMPO, 3),
               "e": round(at + lead + (w["end"] - words[a]["start"]) / TEMPO, 3)} for w in words[a:b + 1]]
        end = round(at + len(seg) / SR, 3)
        meta.append({"phrase": i, "start": at, "end": end, "words": fw})
        if text:
            cues.append({"text": text, "start": round(fw[0]["s"] - 0.1, 3), "end": round(fw[-1]["e"] + 0.6, 3)})
        print(f"{at:6.2f} → {end:6.2f}  {' '.join(w['w'] for w in fw)}")
    for x, y in zip(cues, cues[1:]):
        if x["end"] > y["start"] - 0.04: x["end"] = round(y["start"] - 0.04, 3)
    peak = float(np.max(np.abs(out))); out *= (10 ** (-1.5 / 20)) / peak
    with wave.open("assets/audio/vo.raw.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "assets/audio/vo.raw.wav", "-af",
                    "acompressor=threshold=-26dB:ratio=2.5:attack=8:release=160:makeup=4dB,"
                    "alimiter=limit=0.84:attack=3:release=60,loudnorm=I=-16:TP=-1.5:LRA=8",
                    "-ar", str(SR), "-ac", "1", "assets/audio/vo.wav"], check=True)
    os.remove("assets/audio/vo.raw.wav")
    json.dump({"source": "ElevenLabs voix créée 296ArNMXC82lzWBz0g98, eleven_v3, take B", "tempo": TEMPO,
               "phrases": meta}, open("assets/audio/vo_meta.json", "w"), ensure_ascii=False, indent=1)
    os.makedirs("assets/captions", exist_ok=True)
    json.dump(cues, open("assets/captions/captions.json", "w"), ensure_ascii=False, indent=1)

main()
