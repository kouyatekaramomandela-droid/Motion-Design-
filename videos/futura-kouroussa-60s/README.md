# FUTURA-Kouroussa — film 60 s (photos réelles, motion design 2.5D)

Trois formats compilés depuis une seule source :

| Format | Projet | Taille |
| --- | --- | --- |
| 16:9 (maître) | `futura-kouroussa-60s/` | 1920×1080 |
| 9:16 | `../futura-kouroussa-60s-9x16/` (généré, `assets/` pointe ici) | 1080×1920 |
| 1:1 | `../futura-kouroussa-60s-1x1/` (généré, `assets/` pointe ici) | 1080×1080 |

Brief : `BRIEF.md` · texte : `SCRIPT.md` · plan : `STORYBOARD.md`.

## Chaîne de fabrication (depuis ce dossier)

```bash
V=<venv avec numpy, scipy, opencv-python-headless>
$V/bin/python tools/prep_photos.py    # logos effacés, agrandissement x2, plans 2.5D (fond nettoyé + premier plan détouré)
$V/bin/python tools/bake_grades.py    # étalonnages tools/grades.json calculés par HyperFrames (une image fixe par photo)
$V/bin/python tools/build_vo.py       # voix posée phrase par phrase -> assets/audio/vo.wav + sous-titres
$V/bin/python tools/synth_score.py    # musique 96 BPM baissée de 15 dB sous la voix + effets -> music.wav, sfx.wav
python3 tools/build.py                # scènes -> compositions des 3 projets
npx --yes hyperframes@0.8.141 check   # (et dans les deux projets frères)
npx --yes hyperframes@0.8.141 render --fps 30 --quality delivery -o renders/raw-16x9.mp4
tools/finish.sh renders/raw-16x9.mp4 livrables/futura-kouroussa-60s-16x9.mp4   # grain de film + encodage final
```

Les fichiers `.wav` ne sont pas versionnés : ils se régénèrent avec `build_vo.py` et `synth_score.py`
(la prise source de la voix, `assets/audio/src/take-b.mp3`, est versionnée).

## Pourquoi les étalonnages sont « cuits »

Ce conteneur n'a pas de GPU. L'étalonnage HyperFrames en temps réel (`data-color-grading`) passe alors
par SwiftShader et bloque le rendu (mesuré : ~6 s par image pour deux petites photos, aucune progression
pour des plans plein cadre). Les étalonnages étant fixes, HyperFrames les calcule une fois sur chaque
photo (`tools/bake_grades.py`, via `hyperframes snapshot`) ; les variations (assombrissement, passage
au gris, recoloration dorée) sont des fondus entre deux versions étalonnées. Le grain de film, animé,
est ajouté à l'encodage final (`tools/finish.sh`). Sur une machine avec GPU, les mêmes réglages
peuvent être reposés en temps réel avec `hyperframes media-treatment`.
