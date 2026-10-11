#!/bin/bash
# Quality control of a delivered film: one frame per second (+ the last frame), contact sheets of 15,
# duration, streams and loudness.
# usage: tools/qc.sh <film.mp4> <out dir>
set -euo pipefail
in="$1"; out="$2"; mkdir -p "$out"; rm -f "$out"/f-*.jpg "$out"/sheet-*.jpg
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$in")
ffmpeg -v error -y -i "$in" -vf "fps=1,scale=640:-2" -q:v 3 "$out/f-%03d.jpg"
i=0
for f in "$out"/f-*.jpg; do
  t=$((10#$(basename "$f" .jpg | cut -d- -f2) - 1))
  convert "$f" -gravity northwest -fill white -undercolor '#000a' -pointsize 22 -annotate +6+6 "${t}s" "$f"
done
ls "$out"/f-*.jpg | split -l 15 - "$out/list-"
n=0; for l in "$out"/list-*; do montage $(cat "$l") -geometry +3+3 -tile 5x -background '#222' "$out/sheet-$n.jpg"; rm "$l"; n=$((n+1)); done
echo "duration: $dur s"
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,sample_rate,channels -of compact "$in"
ffmpeg -v info -i "$in" -af ebur128=peak=true:framelog=quiet -f null - 2>&1 | grep -E "^\s+(I|LRA|Peak):" | tr -s ' '
