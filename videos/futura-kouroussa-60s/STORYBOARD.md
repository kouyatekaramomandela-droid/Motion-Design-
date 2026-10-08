---
format: 1920x1080
format_variants: [1080x1920, 1080x1080]
fps: 30
duration: 60s
message: "L'or de Kouroussa, au service de Kouroussa : un fonds clair, suivi, audité, où les communautés ont leur mot à dire."
arc: Lieu → Gens → Or → Manque → Réponse → Promesse
audience: habitants de Kouroussa et partenaires institutionnels
mode: collaborative
version: v4
---

# FUTURA-Kouroussa 60 s — storyboard v4 (toutes les photos du client)

## Décisions

- **Message** : un fonds clair, suivi, audité, où les communautés ont leur mot à dire ; signature
  « L'or de Kouroussa, au service de Kouroussa. »
- **Format** : 16:9 1920×1080 (maître), 9:16 1080×1920, 1:1 1080×1080 ; 30 fps ; 60,0 s. Voix off
  (voix créée sur mesure, « Voix A »), musique 96 BPM, sous-titres incrustés partout (texte ≥ 36 px ;
  sous-titres 42 px en 16:9, 46 px en 9:16, 40 px en 1:1).
- **Fil conducteur** : **les lignes d'or**. Elles naissent de l'éclat de l'ouverture, dessinent le
  fleuve, sortent de la mine, quittent l'écran pendant le contraste, reviennent dessiner le logo,
  puis se posent en bande tricolore. Chaque transition est un balayage ou un morphing de ces lignes.
- **Traitement photo (2.5D)** : chaque photo en trois plans : fond (photo entière, légèrement
  floutée et agrandie), sujet détouré (pont, engins, personnes) qui glisse plus vite, avant-plan
  (particules d'or, balayage de lumière). Caméra lente. Étalonnage par le système HyperFrames
  (tools/grades.json, validé par `hyperframes media-treatment`) : noirs profonds, hautes lumières
  dorées ; mine en or chaud contrasté, communautés en tons doux ; désaturation pendant le contraste,
  recoloration dorée à la signature. Ce conteneur n'a pas de GPU : l'étalonnage temps réel bloque le
  rendu, il est donc calculé une fois par HyperFrames sur chaque photo (tools/bake_grades.py) et les
  changements d'étalonnage se font par fondu entre deux versions. Grain de film léger ajouté à
  l'encodage final (tools/finish.sh).
- **Images** : uniquement des photos du client (lots 1 à 3). Les photos de groupe (Maison des Jeunes,
  assemblée de femmes, assemblée des anciens) ont un mouvement de caméra lent sans plan détouré.
- **Trois mines** : trois photos du client (fosse avec engins, usine de traitement, vue aérienne),
  présentées une à une avec le compteur « 1 mine · 2 mines · 3 mines ».
- **Rythme** : ample et lent (0–15 s), plus vif (15–38 s), apaisé (52–60 s).
- **Interdits** : foules, pelleteuses menaçantes (engins vus de haut, plan calme, sans poussée
  dramatique), noms ou logos de sociétés (logo du gilet et marquages des engins masqués), plaques,
  répartition du capital, chiffres non cités, texte < 36 px.
- **Vérité** : « plus de 2 milliards USD par an » tel que fourni ; carte stylisée ; photos du client
  avec autorisations des personnes visibles.

## Frame 1 — Ouverture

- duration: 5s
- start: 0
- status: built
- src: compositions/f1.html (source : scenes/f1.frag.html + scenes/f1.anim.js)
- voiceover: "Kouroussa."

Noir. Un éclat d'or s'allume (0,4 s), des particules s'en échappent. Le pont sur le Niger apparaît en
plongée lente (photo A, 2.5D : le pont glisse sur l'eau). « KOUROUSSA » se grave en or au centre
(Playfair 900, 168 px en 16:9), un reflet de lumière le traverse. VO « Kouroussa. » à 2,2 s.

## Frame 2 — La terre et les gens

- duration: 10s
- start: 5
- status: built
- src: compositions/f2.html (source : scenes/f2.frag.html + scenes/f2.anim.js)
- voiceover: "Ici, il y a un fleuve, des quartiers qui vivent, et des familles qui travaillent chaque jour pour construire leur avenir."

Trois plans en parallaxe douce, chacun sur son mot :
1. **4,6–7,7** photo A recadrée sur l'eau scintillante : « Un fleuve. »
2. **7,7–10,2** photo : la Maison des Jeunes de Kouroussa : « Des quartiers. »
3. **10,2–15,0** photo : une assemblée de femmes : « Des familles. »
Transitions : une ligne d'or balaie le cadre et révèle le plan suivant.

## Frame 3 — L'or

- duration: 13s
- start: 15
- status: built
- src: compositions/f3.html (source : scenes/f3.frag.html + scenes/f3.anim.js)
- voiceover: "Et sous cette terre, il y a de l'or. Trois mines, et plus de deux milliards de dollars chaque année."

Photo de la mine 1 (étalonnage or chaud contrasté, zoom lent, engins en plan détouré, calmes). Sur
« Trois mines », la photo s'assombrit et les trois sites apparaissent en trois vignettes numérotées à
18,9 / 19,4 / 19,9 s (tintements) avec le compteur ; « 3 mines » tenu 2 s. Puis la vue aérienne de la
mine 3 remplit l'écran, assombrie, sous « plus de 2 milliards USD par an » (compteur 0 → 2 de 22,1 à
23,3 s), tenu jusqu'à 27 s.

## Frame 4 — Le contraste

- duration: 10s
- start: 28
- status: built
- src: compositions/f4.html (source : scenes/f4.frag.html + scenes/f4.anim.js)
- voiceover: "Pourtant, dans beaucoup de villages, l'eau potable manque encore. Des écoles attendent d'être équipées. Des centres de santé n'ont même pas d'électricité."

Les lignes d'or ont quitté l'écran. « dans beaucoup de villages » : le village (cases dans les
champs, tons doux). « l'eau potable manque encore » : le forage perd sa couleur. « Des écoles… » :
la salle de classe, en gris. « Des centres de santé… » : l'hôpital, en gris. « Et les communautés ? »
(Playfair 700) en haut de l'image, tenu ≥ 2 s en fin de scène.

## Frame 5 — La réponse

- duration: 14s
- start: 38
- status: built
- src: compositions/f5.html (source : scenes/f5.frag.html + scenes/f5.anim.js)
- voiceover: "C'est pourquoi la mission parlementaire a recommandé FUTURA-Kouroussa. Un fonds clair, où chaque contribution des mines est suivie, où les comptes sont audités, et où les communautés ont leur mot à dire."

Les lignes d'or reviennent et dessinent le logo (pépite, main, rayons) sur « FUTURA-Kouroussa ».
Badges « Issu du rapport de mission parlementaire » et « Société Anonyme OHADA ». Puis la photo de
réunion (R) en fond doux, et trois icônes s'allument une à une sur les mots : « Contributions
suivies » (suivie), « Comptes audités » (audités), « Communautés associées » (communautés) ; sur ce
dernier mot, le fond passe à l'assemblée des anciens.

## Frame 6 — Signature

- duration: 8s
- start: 52
- status: built
- src: compositions/f6.html (source : scenes/f6.frag.html + scenes/f6.anim.js)
- voiceover: "L'or de Kouroussa, au service de Kouroussa."

52–55,5 : triptyque qui se recolore en or chaud : le forage (photo D) où coule une eau dorée, la
salle de classe et l'hôpital (photos du lot 2), chacun passant du gris à l'or. 55,5–60 : les lignes d'or se posent en bande tricolore
(rouge, jaune, vert) en bas ; logo centré ; « L'or de Kouroussa, au service de Kouroussa. » tenu
jusqu'à 60 s.
