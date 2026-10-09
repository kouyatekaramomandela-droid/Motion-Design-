#!/usr/bin/env bash
# Final soundtrack: narration + generated score (score -6 dB; it is already ducked under the voice),
# two-pass EBU R128 normalisation to -14 LUFS, true peak -1.5 dBTP. Output: audio/mix.wav (48 kHz stereo, 75 s)
set -euo pipefail
cd "$(dirname "$0")/.."
ffmpeg -v error -y -i audio/vo.wav -i audio/music.wav -filter_complex \
  "[0:a]aformat=channel_layouts=stereo,volume=1.0[v];[1:a]volume=0.5[m];[v][m]amix=inputs=2:normalize=0:duration=longest,atrim=0:75" \
  -ar 48000 audio/mix.raw.wav
read -r I TP LRA THRESH OFFSET < <(ffmpeg -v info -i audio/mix.raw.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 \
  | python3 -c "import sys,json,re; d=json.loads(re.search(r'\{[^{}]*\}', sys.stdin.read(), re.S).group(0)); print(d['input_i'], d['input_tp'], d['input_lra'], d['input_thresh'], d['target_offset'])")
ffmpeg -v error -y -i audio/mix.raw.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$I:measured_TP=$TP:measured_LRA=$LRA:measured_thresh=$THRESH:offset=$OFFSET:linear=true" \
  -ar 48000 -ac 2 audio/mix.wav
rm audio/mix.raw.wav
ffmpeg -v info -i audio/mix.wav -af ebur128=peak=true:framelog=quiet -f null - 2>&1 | grep -E "^\s+(I|LRA|Peak):" | tr -s ' '
