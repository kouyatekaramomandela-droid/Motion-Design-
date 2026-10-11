"""Generate illustrative photos with Gemini image models (key added by the environment's network secret).
Usage: python3 tools/gen_image.py <id> <aspect 16:9|9:16|1:1|4:3> "<prompt>" [model]
Writes assets/generated/<id>.png and appends the prompt to assets/generated/prompts.json (provenance).
"""
import base64, json, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/generated"; OUT.mkdir(parents=True, exist_ok=True)
gid, aspect, prompt = sys.argv[1], sys.argv[2], sys.argv[3]
model = sys.argv[4] if len(sys.argv) > 4 else "gemini-3.1-flash-image"
url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
body = {"contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": aspect}}}
for attempt in range(3):
    p = subprocess.run(["curl", "-sS", "--max-time", "240", "-H", "Content-Type: application/json", "-X", "POST", url,
                        "--data-binary", "@-", "-w", "\n%{http_code}"], input=json.dumps(body).encode(), capture_output=True)
    raw, _, code = p.stdout.decode().rpartition("\n")
    if code == "200":
        parts = json.loads(raw)["candidates"][0]["content"]["parts"]
        img = [x for x in parts if "inlineData" in x or "inline_data" in x]
        if img:
            d = img[0].get("inlineData") or img[0].get("inline_data")
            (OUT / f"{gid}.png").write_bytes(base64.b64decode(d["data"]))
            log = OUT / "prompts.json"
            rec = json.loads(log.read_text()) if log.exists() else {}
            rec[gid] = {"model": model, "aspect": aspect, "prompt": prompt}
            log.write_text(json.dumps(rec, ensure_ascii=False, indent=1) + "\n")
            print("ok", gid); sys.exit(0)
        raw = "no image part: " + raw[:300]
    print("retry", gid, code, raw[:300], flush=True); time.sleep(5 * (attempt + 1))
sys.exit(f"FAILED {gid}")
