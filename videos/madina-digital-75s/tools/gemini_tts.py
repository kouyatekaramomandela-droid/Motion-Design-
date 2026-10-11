"""Generate the voice-over lines with Gemini TTS (Developer Interactions API), one WAV per line.

The API key is never read here: the environment's network secret adds the `x-goog-api-key` header to requests sent
to generativelanguage.googleapis.com. Same request shape as media-use's gemini-tts adapter (3.8: structured style
annotation, WAV response). Lines already generated are kept unless --force.
Usage: python3 tools/gemini_tts.py [--force] [ID ...]    (reads audio/vo_request.json, writes assets/voice/<id>.wav)
"""
import base64, json, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
URL = "https://generativelanguage.googleapis.com/v1beta/interactions"


def pcm_to_wav(pcm, rate):
    import struct
    return (b"RIFF" + struct.pack("<I", 36 + len(pcm)) + b"WAVEfmt " + struct.pack("<IHHIIHH", 16, 1, 1, rate, rate * 2, 2, 16)
            + b"data" + struct.pack("<I", len(pcm)) + pcm)


def synth(text, voice, model, style):
    modern = model.startswith("gemini-3.8-")
    content = {"type": "text", "text": text if modern or not style else f"Read the following text with this delivery: {style}\n\n{text}"}
    if modern and style: content["annotations"] = [{"type": "speech_metadata", "style": style}]
    body = {"model": model, "input": [{"type": "user_input", "content": [content]}],
            "response_format": {"type": "audio", "mime_type": "audio/wav"} if modern else {"type": "audio"},
            "generation_config": {"speech_config": [{"voice": voice}]}, "store": False}
    p = subprocess.run(["curl", "-sS", "--max-time", "120", "-H", "Content-Type: application/json", "-X", "POST", URL,
                        "--data-binary", "@-", "-w", "\n%{http_code}"], input=json.dumps(body).encode(), capture_output=True)
    raw, _, code = p.stdout.decode().rpartition("\n")
    if code != "200":
        raise RuntimeError(f"HTTP {code}: {raw[:400]}")
    payload = json.loads(raw)
    audio = [part for step in payload.get("steps", []) if step.get("type") == "model_output"
             for part in step.get("content", []) if part.get("type") == "audio"]
    if payload.get("status") != "completed" or len(audio) != 1:
        raise RuntimeError(f"no audio ({payload.get('status')})")
    data = base64.b64decode(audio[0]["data"]); mime = audio[0].get("mime_type", "")
    if data[:4] != b"RIFF":
        import re
        m = re.search(r"rate=(\d+)", mime)
        if not mime.lower().startswith("audio/l16") or not m: raise RuntimeError(f"unsupported audio ({mime})")
        data = pcm_to_wav(data, int(m.group(1)))
    return data


def take(req, out):
    """One single take of the whole narration (one line per unit, a clear pause between lines)."""
    text = "\n".join(ln["text"] for ln in req["lines"])
    for attempt in range(3):
        try:
            out.write_bytes(synth(text, req["voice"], req["take_model"], req["take_style"])); print("ok take", out, flush=True); return
        except RuntimeError as e:
            print("retry take", str(e)[:300], flush=True); time.sleep(6 * (attempt + 1))
    raise SystemExit("take failed")


def main():
    args = sys.argv[1:]
    if "--take" in args:
        req = json.loads((ROOT / "audio/vo_request.json").read_text())
        (ROOT / "audio/src").mkdir(parents=True, exist_ok=True)
        take(req, ROOT / "audio/src/take-gemini.wav"); return; force = "--force" in args; only = {a for a in args if not a.startswith("--")}
    req = json.loads((ROOT / "audio/vo_request.json").read_text())
    out = ROOT / "assets/voice"; out.mkdir(parents=True, exist_ok=True)
    for ln in req["lines"]:
        if only and ln["id"] not in only: continue
        dest = out / f"{ln['id']}.wav"
        if dest.exists() and not force: continue
        for attempt in range(4):
            try:
                dest.write_bytes(synth(ln["text"], req["voice"], req["tts_model"], ln.get("style", req.get("style"))))
                print("ok", ln["id"], flush=True); break
            except RuntimeError as e:
                print("retry", ln["id"], str(e)[:200], flush=True); time.sleep(4 * (attempt + 1))
        else:
            print("FAILED", ln["id"], flush=True)


main()
