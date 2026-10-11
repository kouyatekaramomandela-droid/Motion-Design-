"""Find where each line of the voice-over sits in the single Gemini take, then cut it into one WAV per line.

1. Gemini (gemini-3.8-flash, audio understanding) listens to the take and returns, for each expected line, its start
   and end time and what it actually heard (to catch a missing word or spoken stage directions).
2. Every boundary is snapped to the quietest point of the silence nearest to it (ffmpeg silencedetect, -40 dB).
The key is added by the environment's network secret (header), never read here.
Outputs: assets/voice/<id>.wav, audio/src/take-align.json
Usage: python3 tools/align_take.py
"""
import base64, json, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAKE = ROOT / "audio/src/take-gemini.wav"
SMALL = ROOT / "audio/src/take-gemini-16k.mp3"   # light copy sent for listening (same timeline)
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent"


def ask(lines):
    listing = "\n".join(f'{l["id"]}: {l["text"]}' for l in lines)
    prompt = ("Voici l'enregistrement d'une voix off en français. Le texte attendu, ligne par ligne, est :\n" + listing +
              "\n\nPour chaque ligne, donne le temps (en secondes, avec 2 décimales, depuis le début du fichier) où la ligne "
              "commence et où elle se termine, et recopie exactement ce que tu entends. Réponds uniquement en JSON : une liste "
              "d'objets {\"id\", \"start\", \"end\", \"heard\"}, dans l'ordre. Si quelque chose est dit qui n'est pas dans le "
              "texte, ajoute un objet avec id \"extra\".")
    body = {"contents": [{"parts": [{"inline_data": {"mime_type": "audio/mp3", "data": base64.b64encode(SMALL.read_bytes()).decode()}},
                                    {"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0}}
    p = subprocess.run(["curl", "-sS", "--max-time", "300", "-H", "Content-Type: application/json", "-X", "POST", URL,
                        "--data-binary", "@-", "-w", "\n%{http_code}"], input=json.dumps(body).encode(), capture_output=True)
    raw, _, code = p.stdout.decode().rpartition("\n")
    if code != "200": raise SystemExit(f"HTTP {code}: {raw[:400]}")
    text = json.loads(raw)["candidates"][0]["content"]["parts"][0]["text"]
    return json.loads(text)


def silences():
    out = subprocess.run(["ffmpeg", "-v", "info", "-i", str(TAKE), "-af", "silencedetect=noise=-40dB:d=0.12", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", out)]
    en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", out)]
    return list(zip(st, en))


def main():
    lines = json.loads((ROOT / "audio/vo_request.json").read_text())["lines"]
    al = ask(lines)
    (ROOT / "audio/src/take-align.json").write_text(json.dumps(al, ensure_ascii=False, indent=1) + "\n")
    got = {a["id"]: a for a in al if a.get("id") != "extra"}
    for a in al:
        if a.get("id") == "extra": print("EXTRA heard:", a)
    sil = silences()
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(TAKE)],
                               capture_output=True, text=True).stdout)
    cuts = [0.0]
    for k in range(len(lines) - 1):
        a, b = got[lines[k]["id"]], got[lines[k + 1]["id"]]
        mid = (float(a["end"]) + float(b["start"])) / 2
        best = min(sil, key=lambda s: abs((s[0] + s[1]) / 2 - mid))
        cuts.append((best[0] + best[1]) / 2 if abs((best[0] + best[1]) / 2 - mid) < 0.8 else mid)
    cuts.append(dur)
    out = ROOT / "assets/voice"; out.mkdir(parents=True, exist_ok=True)
    for k, l in enumerate(lines):
        a, b = cuts[k], cuts[k + 1]
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(TAKE), "-ss", f"{a:.3f}", "-to", f"{b:.3f}", str(out / f"{l['id']}.wav")], check=True)
        h = got.get(l["id"], {}).get("heard", "?")
        flag = "" if re.sub(r"\W", "", h.lower()) == re.sub(r"\W", "", l["text"].lower()) else "   <-- différent"
        print(f"{a:6.2f}-{b:6.2f}  {l['id']}  {h}{flag}")


main()
