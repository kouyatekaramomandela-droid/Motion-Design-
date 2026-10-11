#!/bin/bash
# Render the deck to PDF (LibreOffice) and to slide images + contact sheets in qa/.
set -euo pipefail
cd "$(dirname "$0")/.."
SK=/root/.claude/skills/synced/130859c3-5cd6-400e-9bc5-cf28f1119f86_62dea71b-de69-48f4-9353-51f2675f7d29/pptx
mkdir -p qa && cp livrables/FUTURA-Kouroussa_Synthese_Maire_Prefet.pptx qa/deck.pptx
cd qa && rm -f deck.pdf slide-*.jpg sheet-*.jpg
timeout 240 python3 $SK/scripts/office/soffice.py --headless --convert-to pdf deck.pptx >/dev/null 2>&1
pdftoppm -jpeg -r ${DPI:-60} deck.pdf slide
montage slide-0[1-6].jpg -geometry +4+4 -tile 2x -background '#444' sheet-a.jpg
montage slide-0[7-9].jpg slide-1[0-2].jpg -geometry +4+4 -tile 2x -background '#444' sheet-b.jpg
montage slide-1[3-5].jpg -geometry +4+4 -tile 2x -background '#444' sheet-c.jpg
ls sheet-*.jpg
