#!/bin/bash
# Render the 16:9 and 9:16 versions one after the other, finish them into exports/, then run the QC on each.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p exports
for v in "16x9:." "9x16:../madina-digital-75s-9x16"; do
  name=${v%%:*}; dir=${v#*:}
  if [ $# -gt 0 ] && [[ ! " $* " == *" $name "* ]]; then continue; fi
  echo "== render $name $(date +%T)"
  (cd "$dir" && npx --yes hyperframes@0.8.145 render --fps 30 --quality delivery -o renders/master.mp4)
  tools/finish.sh "$dir/renders/master.mp4" "exports/madina_digital_$name.mp4"
  tools/qc.sh "exports/madina_digital_$name.mp4" "renders/qc-$name"
  echo "== done $name $(date +%T)"
done
