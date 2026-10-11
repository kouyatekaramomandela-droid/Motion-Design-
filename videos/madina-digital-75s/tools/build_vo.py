"""Place the Gemini TTS lines of the MADINA DIGITAL voice-over on the film (75 s).

1. Generate (once a GEMINI_API_KEY is in the environment):
     node <media-use>/audio/scripts/audio.mjs --request ./audio/vo_request.json --hyperframes . --out ./audio/vo_engine.json --only tts
   -> one WAV per line in assets/voice/<id>.wav (Gemini voice « Puck », style in vo_request.json).
2. Place: python3 tools/build_vo.py
   Each line is trimmed of its leading/trailing silence and starts at its film time (audio/vo_plan.json, the beat it
   names on screen). A line longer than its slot is sped up, at most ×1.12 (pitch kept); beyond that it is reported.
Outputs: audio/vo.wav (48 kHz mono, 75 s, -16 LUFS), audio/vo_meta.json, exports/madina_digital.srt
"""
import json, subprocess, wave
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SR, FILM, MAXTEMPO = 48000, 75.0, 1.12


def decode(path, af=None):
    cmd = ["ffmpeg", "-v", "error", "-i", str(path)] + (["-af", af] if af else []) + ["-f", "f32le", "-ac", "1", "-ar", str(SR), "-"]
    return np.frombuffer(subprocess.run(cmd, check=True, capture_output=True).stdout, dtype=np.float32).copy()


def trim(x, thr_db=-42, pad=0.03):
    w = int(0.01 * SR); e = np.array([np.sqrt(np.mean(x[i:i + w] ** 2) + 1e-12) for i in range(0, len(x) - w, w)])
    on = np.where(20 * np.log10(e) > thr_db)[0]
    if not len(on): return x
    a, b = max(0, on[0] * w - int(pad * SR)), min(len(x), (on[-1] + 1) * w + int(pad * SR))
    return x[a:b]


def tempo(x, f):
    p = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-i", "-", "-af", f"atempo={f:.4f}",
                        "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], input=x.astype(np.float32).tobytes(), capture_output=True, check=True)
    return np.frombuffer(p.stdout, dtype=np.float32).copy()


def srt_time(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main():
    plan = json.loads((ROOT / "audio/vo_plan.json").read_text())
    out = np.zeros(int(FILM * SR), np.float32); meta, warn = [], []
    for ln in plan:
        src = ROOT / f"assets/voice/{ln['id']}.wav"
        if not src.exists():
            raise SystemExit(f"missing {src}: run the Gemini generation first (see the docstring)")
        x = trim(decode(src)); d = len(x) / SR; f = 1.0
        if d > ln["max"]:
            f = min(MAXTEMPO, d / ln["max"]); x = tempo(x, f); d = len(x) / SR
            if d > ln["max"] + 0.05: warn.append(f"{ln['id']}: {d:.2f}s > slot {ln['max']}s")
        fd = int(0.006 * SR); x[:fd] *= np.linspace(0, 1, fd); x[-fd:] *= np.linspace(1, 0, fd)
        s = int(ln["at"] * SR); out[s:s + len(x)] += x[:max(0, len(out) - s)]
        meta.append({"id": ln["id"], "text": ln["text"], "start": ln["at"], "end": round(ln["at"] + d, 3), "tempo": round(f, 3)})
        print(f"{ln['at']:6.2f} → {ln['at'] + d:6.2f}  ×{f:.2f}  {ln['text']}")
    out *= (10 ** (-1.5 / 20)) / (np.max(np.abs(out)) + 1e-9)
    with wave.open(str(ROOT / "audio/vo.raw.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(ROOT / "audio/vo.raw.wav"), "-af",
                    "highpass=f=70,acompressor=threshold=-24dB:ratio=2.2:attack=8:release=160:makeup=3dB,alimiter=limit=0.85,loudnorm=I=-16:TP=-1.5:LRA=9",
                    "-ar", str(SR), "-ac", "1", str(ROOT / "audio/vo.wav")], check=True)
    (ROOT / "audio/vo.raw.wav").unlink()
    (ROOT / "audio/vo_meta.json").write_text(json.dumps({"source": "Gemini TTS (gemini-3.8-flash-tts), voix Puck", "units": meta}, ensure_ascii=False, indent=1) + "\n")
    (ROOT / "exports").mkdir(exist_ok=True)
    with open(ROOT / "exports/madina_digital.srt", "w") as fh:
        for k, m in enumerate(meta, 1):
            nxt = meta[k]["start"] if k < len(meta) else FILM
            fh.write(f"{k}\n{srt_time(m['start'] - 0.05)} --> {srt_time(min(m['end'] + 0.6, nxt - 0.05))}\n{m['text']}\n\n")
    for w_ in warn: print("WARNING", w_)


main()
