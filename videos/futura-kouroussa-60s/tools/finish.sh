#!/bin/bash
# Final pass on a rendered master: light animated film grain (luma only, temporal, deterministic seed),
# then a delivery encode. The grain is added here because the photo grades are baked as stills
# (see tools/bake_grades.py): baked grain would freeze on screen.
# usage: tools/finish.sh <rendered.mp4> <delivery.mp4>
set -euo pipefail
in="$1"; out="$2"
ffmpeg -v error -y -i "$in" \
  -vf "noise=c0s=5:c0f=t+u:all_seed=20261008,format=yuv420p" \
  -c:v libx264 -preset slow -crf 17 -profile:v high -movflags +faststart \
  -c:a copy "$out"
echo "finished: $out ($(ffprobe -v error -show_entries format=duration -of csv=p=0 "$out") s)"
