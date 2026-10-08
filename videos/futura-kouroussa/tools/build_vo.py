"""Place the 8 voice-over lines of take A on the 120 s film timeline.

Outputs (project-relative):
  assets/audio/vo.wav            48 kHz mono, 120.0 s, lines at their scene offsets
  assets/audio/vo_meta.json      lines + every word re-timed to film time
  assets/captions/captions.json  caption cues (text verbatim from SCRIPT.md)
Usage: python tools/build_vo.py   (run from the project root)
"""
import json, os, subprocess, wave
import numpy as np

SR = 48000
FILM = 120.0
SRC = "assets/audio/src/take-a.mp3"
WORDS = "assets/audio/src/take-a.words.json"

# film start (s) of each line; word counts per caption cue (from the take-A transcript)
LINES = [
    {"id": "L1", "scene": 1, "at": 1.2, "cues": [(12, "Chaque année, l'or de Kouroussa représente plus de deux milliards de dollars.")]},
    {"id": "L2", "scene": 2, "at": 13.0, "cues": [
        (12, "Et pourtant, sur cette même terre, des familles attendent encore l'eau potable,"),
        (10, "des écoles équipées, des centres de santé alimentés en énergie.")]},
    {"id": "L3", "scene": 3, "at": 29.0, "cues": [
        (10, "Le Code minier prévoit des obligations envers les communautés locales."),
        (10, "Mais sans cadre dédié, leur suivi reste difficile à vérifier.")]},
    {"id": "L4", "scene": 4, "at": 44.0, "cues": [
        (5, "La loi fixe le principe."),
        (9, "Il manquait l'instrument pour l'appliquer, avec rigueur et transparence.")]},
    {"id": "L5", "scene": 5, "at": 59.5, "cues": [
        (11, "FUTURA-Kouroussa : un fonds constitué sous forme de société anonyme OHADA,"),
        (7, "né du rapport de la mission parlementaire,"),
        (9, "pour centraliser et redistribuer ces ressources de manière traçable.")]},
    {"id": "L6", "scene": 6, "at": 77.0, "cues": [
        (6, "Les collectivités y détiennent la majorité."),
        (8, "Chaque décision est encadrée, chaque dépense est auditée,"),
        (4, "chaque comptabilité est publique.")]},
    {"id": "L7", "scene": 7, "at": 96.5, "cues": [
        (6, "De l'eau, des écoles, des soins :"),
        (9, "des résultats que chaque communauté pourra suivre et vérifier.")]},
    # Scene 8: the screen already shows the spoken words, so no caption (client-approved default)
    {"id": "L8", "scene": 8, "at": 111.5, "captions": False, "cues": [
        (2, "FUTURA-Kouroussa."), (7, "L'or de Kouroussa, au service de Kouroussa.")]},
]

def decode(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()

def main():
    src = decode(SRC)
    words = json.load(open(WORDS))["words"]
    out = np.zeros(int(FILM * SR), dtype=np.float32)
    meta, cues = [], []
    i = 0
    for line in LINES:
        n = sum(c[0] for c in line["cues"])
        lw = words[i:i + n]; i += n
        t0, t1 = lw[0]["start"], lw[-1]["end"]
        shift = line["at"] - t0
        a, b = max(0.0, t0 - 0.08), t1 + 0.30
        seg = src[int(a * SR):int(b * SR)].copy()
        fade = int(0.012 * SR); seg[:fade] *= np.linspace(0, 1, fade); seg[-int(0.08 * SR):] *= np.linspace(1, 0, int(0.08 * SR))
        s = int((a + shift) * SR); out[s:s + len(seg)] += seg
        film_words = [{"w": w["text"], "s": round(w["start"] + shift, 3), "e": round(w["end"] + shift, 3)} for w in lw]
        meta.append({"id": line["id"], "scene": line["scene"], "start": round(line["at"], 3),
                     "end": round(t1 + shift, 3), "words": film_words})
        if line.get("captions", True):
            k = 0
            for count, text in line["cues"]:
                cw = film_words[k:k + count]; k += count
                cues.append({"line": line["id"], "text": text, "start": round(cw[0]["s"] - 0.12, 3), "end": round(cw[-1]["e"] + 0.45, 3)})
    # cues never overlap; short gaps between cues of one line are bridged so the text does not blink
    for a, b in zip(cues, cues[1:]):
        if b["start"] - a["end"] < 0.6:
            a["end"] = round(b["start"] - 0.04, 3)
    peak = float(np.max(np.abs(out)))
    out *= (10 ** (-1.5 / 20)) / peak  # normalise VO peak to -1.5 dBFS
    pcm = (np.clip(out, -1, 1) * 32767).astype(np.int16)
    with wave.open("assets/audio/vo.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    # broadcast speech: gentle compression + limiter, then loudness to -16 LUFS / -1.5 dBTP
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "assets/audio/vo.wav", "-af",
                    "acompressor=threshold=-26dB:ratio=3:attack=8:release=150:makeup=6dB,"
                    "alimiter=limit=0.84:attack=3:release=60,loudnorm=I=-16:TP=-1.5:LRA=7",
                    "-ar", str(SR), "-ac", "1", "assets/audio/vo.tmp.wav"], check=True)
    os.replace("assets/audio/vo.tmp.wav", "assets/audio/vo.wav")
    json.dump({"source": "ElevenLabs Florian (FL0d5832ACnJkBaedeKX), eleven_multilingual_v2, take A",
               "lines": meta}, open("assets/audio/vo_meta.json", "w"), ensure_ascii=False, indent=1)
    os.makedirs("assets/captions", exist_ok=True)
    json.dump(cues, open("assets/captions/captions.json", "w"), ensure_ascii=False, indent=1)
    for m in meta: print(f'{m["id"]}  {m["start"]:7.2f} → {m["end"]:7.2f}')
    for c in cues: print(f'  {c["start"]:7.2f}–{c["end"]:7.2f}  {c["text"]}')

main()
