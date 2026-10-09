# Rapport de la tournée des Députés de Kouroussa — film institutionnel 75 s

Film de présentation du rapport de la tournée des Honorables Députés Lamine KOUYATÉ et Dre Hadja Djoran KEITA
dans la commune urbaine et les 14 sous-préfectures de Kouroussa (18 – 27 septembre 2026). Brief : `BRIEF.md`.
Plan validé : `STORYBOARD.md` et la planche `storyboard.html` (image : `sketches/storyboard-v1.jpg`).

## Livrables (`exports/`)

| Fichier | Contenu |
| --- | --- |
| `rapport_tournee_16x9.mp4` | 1920×1080, 30 i/s, 75 s, H.264 + AAC, sous-titres incrustés |
| `rapport_tournee_9x16.mp4` | 1080×1920, recomposé pour Facebook / WhatsApp, sous-titres incrustés |
| `rapport_tournee_sans_texte.mp4` | 16:9 sans titres, chiffres ni sous-titres (logos, carte, images et son conservés) |
| `rapport_tournee.srt` | sous-titres français (y compris la phrase finale, non incrustée car écrite à l'écran) |

## Projets

- `.` : 16:9 (source unique des scènes) ; `../rapport-tournee-kouroussa-9x16` et
  `../rapport-tournee-kouroussa-sans-texte` sont générés par `tools/build.py` (ne pas éditer à la main).
- `scenes/sN.frag.html` (mise en page 16:9 et 9:16) + `scenes/sN.anim.js` (mouvement, temps global du film).
- `assets/mission/` : médias réels de la mission, 01_ … 20_ (ordre alphabétique). `assets/illustration/` : images
  fournies par le client pour les axes sans photo de mission (eau, santé, agriculture, électricité ; « Image
  d'illustration » à l'écran). `assets/logos/` : logos fournis et leur version détourée (`prep/`).

## Chaîne de fabrication

```bash
V=<venv avec numpy, scipy, opencv, pillow>
$V/bin/python -I tools/prep_logos.py $PWD          # logos : fond blanc retiré, rien de redessiné
python3 -I tools/make_map.py <dossier geojson>      # carte : contour et sous-préfectures réels
$V/bin/python -I tools/prep_media.py $PWD           # nettoyage, extraits vidéo, correction + étalonnage
$V/bin/python -I tools/soften.py $PWD               # versions floues des fonds très doux
python3 tools/build_vo.py                           # voix off placée + sous-titres + .srt
$V/bin/python tools/synth_score.py                  # musique générée (80 BPM), baissée sous la voix
tools/mix_audio.sh                                  # mixage -14 LUFS
python3 tools/build.py                              # assemble les 3 projets
npx --yes hyperframes@0.8.141 render --fps 30 --quality delivery -o renders/x.mp4   # dans chaque projet
tools/finish.sh renders/x.mp4 exports/<nom>.mp4     # grain léger + encodage de livraison
tools/qc.sh exports/<nom>.mp4 renders/qc-<nom>      # 1 image/s, durée, flux, sonie
```

## Traitement des images

- Nettoyage limité à ce qui n'est ni un visage, ni une foule, ni un lieu, ni une tenue : tampons « Galaxy A54 5G »
  (04, 06, 07), plaque AQ 5334 (03), plaques vertes « AN » du convoi (détectées et floutées image par image),
  logo CapCut de la vidéo 20 (recadré). Les logos imprimés sur des vêtements sont laissés tels quels.
- Correction : `hyperframes media-treatment --analyze` par image ; étalonnage chaud commun (`tools/grades.json`)
  rendu par le shader HyperFrames sur une table Hald, puis appliqué par ffmpeg (`haldclut`) aux photos et aux
  extraits : même rendu sur images fixes et vidéo, sans WebGL au rendu. Écart vérifié avec le rendu direct :
  1,3/255 en moyenne.

## Sources

- Voix off : ElevenLabs, modèle eleven_v4, voix « Florian » (FL0d5832ACnJkBaedeKX), prise B ; phrases placées
  entre les pauses de la prise (tempo 0,96).
- Musique : générée localement par `tools/synth_score.py` (cordes, basse, kora par synthèse Karplus-Strong,
  percussions mandingues légères) : aucune œuvre tierce, libre de droits.
- Ambiances : aucune. Le son des vidéos 19 et 20 est une musique ajoutée au montage (niveau constant, pulsation et
  tonalité marquées), donc non réutilisable.
- Carte : limites administratives OCHA / PAM via geoBoundaries (gbOpen GIN ADM2/ADM3, CC BY 3.0 IGO, crédit à
  l'écran). Ce découpage est antérieur aux sous-préfectures de 2021 : Fadoussaba (10,998° N, 10,529° O) et
  Kouroukoro (10,92° N, 10,75° O) sont placées d'après OpenStreetMap / Wikipédia ; Kanséréya, sans source, est
  placée de façon indicative à la demande du client. Les autres points marquent le centre de chaque territoire.
- Polices : Playfair Display et Inter (SIL Open Font License, `assets/fonts/LICENSE-*`).
