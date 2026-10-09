#!/bin/bash
# Render the three versions one after the other, finish them into exports/, then run the QC on each.
set -euo pipefail
cd "$(dirname "$0")/.."
HERE=$PWD; mkdir -p exports
for v in "16x9:." "9x16:../rapport-tournee-kouroussa-9x16" "sans_texte:../rapport-tournee-kouroussa-sans-texte"; do
  name=${v%%:*}; dir=${v#*:}
  echo "== render $name $(date +%T)"
  (cd "$dir" && npx --yes hyperframes@0.8.141 render --fps 30 --quality delivery -o renders/master.mp4)
  tools/finish.sh "$dir/renders/master.mp4" "exports/rapport_tournee_$name.mp4"
  tools/qc.sh "exports/rapport_tournee_$name.mp4" "renders/qc-$name"
  echo "== done $name $(date +%T)"
done
