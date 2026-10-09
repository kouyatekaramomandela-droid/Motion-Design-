#!/bin/bash
# Final pass on a rendered master: very light animated film grain (luma only, temporal, deterministic seed)
# so the baked stills do not look frozen, then the delivery encode (H.264 High, AAC kept from the render).
# usage: tools/finish.sh <rendered.mp4> <delivery.mp4>
set -euo pipefail
in="$1"; out="$2"
ffmpeg -v error -y -i "$in" \
  -vf "noise=c0s=4:c0f=t+u:all_seed=20261009,format=yuv420p" \
  -c:v libx264 -preset slow -crf 17 -profile:v high -movflags +faststart \
  -c:a copy "$out"
echo "finished: $out ($(ffprobe -v error -show_entries format=duration -of csv=p=0 "$out") s)"
