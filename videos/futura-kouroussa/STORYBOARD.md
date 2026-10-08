---
format: 1920x1080
format_variants: [1080x1920]
fps: 30
duration: 120s
message: "L'or de Kouroussa doit servir Kouroussa."
arc: Valeur → Manque → Perte → Loi → Instrument → Gouvernance → Résultats → Signature
audience: autorités préfectorales et communales, communautés, partenaires institutionnels, sociétés minières
mode: collaborative
version: v2
---

# FUTURA-Kouroussa — storyboard v2

## Décisions

- **Message** : « L'or de Kouroussa doit servir Kouroussa. »
- **Format** : 16:9 1920x1080, 30 fps, 120,0 s exactes ; déclinaison 9:16 1080x1920 aux mêmes
  timecodes, même bande son, mise en page recomposée. Voix off oui, musique oui, sous-titres
  français incrustés (zone basse, marge 5 %, contenu au-dessus).
- **Le fil conducteur (spine)** : **le fil d'or**. Une seule particule née en scène 1 devient le
  réseau doré de la carte, s'échappe vers l'horizon (3), fait demi-tour sous l'effet de la loi
  (4), se concentre et éclate en emblème (5), circule dans l'anneau de gouvernance (6), irrigue
  les villages (7) et se pose en bande tricolore (8). Chaque passage de scène est un morphing de
  ce fil, jamais une coupe.
- **Objet héros et rappels** : la triade forage / classe / poste de santé, dessinée « éteinte »
  en scène 2, revient aux mêmes positions et s'allume en scène 7. L'anneau extérieur de
  l'emblème (5) devient l'anneau des quatre collèges (6). L'emblème revient centré en 8.
- **Charte** : voir `frame.md` (marine #1A2A3A, or #B8860B / #F5C518, blanc cassé #F3EEE3,
  Playfair Display + Montserrat, rouge/vert réservés à la bande finale).
- **Plan fixe volontaire** : scène 3, 38,5–41,5 s. Plus rien ne bouge sauf le point
  d'interrogation qui respire ; la question tient seule.
- **Interdits** : visages réels, noms ou logos de sociétés, pelleteuses, foules, chiffres de
  résultats non cités, coupes sèches, dégradés linéaires plein cadre. Deux échecs de mouvement
  à éviter : le diaporama (chaque scène une nouvelle carte posée) et l'économiseur d'écran
  (des particules qui bougent sans rien dire).
- **Vérité** : les chiffres affichés (2,35 milliards USD/an, Art. 130 à 1 %, 40/25/25/10) sont
  repris tels que fournis par le client (Rapport de Mission Parlementaire). La carte est une
  silhouette stylisée ; la position des trois mines est indicative et non nommée.
- **Son** : partition synthétisée sur mesure (nappe de cordes, percussions mandingues douces,
  kora en fil conducteur) : montée jusqu'à 5, apogée en 6, résolution en 8. Tintements dorés
  sur les apparitions de particules, souffle grave à chaque transition. Musique creusée sous la
  voix.

## Encore ouvert

- **Article 165** : le brief ne précise pas son intitulé. Il est affiché seul (« Article 165 »)
  sauf si vous me donnez le libellé exact à faire apparaître.
- **Sous-titres en scène 8** : la voix dit exactement le texte affiché à l'écran ; je propose de
  ne pas doubler ce texte en sous-titre (évite la redite). À confirmer.

## Locked

- Planche v2 validée par le client (« Je valide ») : mises en page, textes, logo, timecodes.
- Montage final : scènes en sous-compositions qui se chevauchent de 1,2 s (morphing), 120,0 s exactes.
  Emplacements : 0–10,6 · 9,4–28,6 · 27,4–42,6 · 41,4–58,6 · 57,4–75,6 · 74,4–95,6 · 94,4–110,6 · 109,4–120.
- Ajout au build : en 5, « centraliser / redistribuer / traçable » est figuré par des points qui
  convergent vers la pépite, repartent vers six relais, et un anneau pointillé qui tourne.

## Changements depuis v1

- **Logo client** reçu : main ouverte, pépite d'or, cinq rayons, « FUTURA - Kouroussa » et
  « Fonds d'Utilisation Transparente des Ressources Aurifères pour l'Avenir de Kouroussa ».
  Redessiné en vectoriel (`assets/logo/`), version négative (traits blanc cassé) sur fond marine.
  Le nom complet affiché suit le logo (« pour l'Avenir »). Typo du logo : Roboto.
- La rosace v1 est remplacée : en 5, le point de convergence **devient la pépite**, la main se
  dessine dessous pour la recevoir, les rayons jaillissent. En 6, le halo de la pépite devient
  l'anneau des collèges (la pépite reste au cœur de l'anneau). En 8, logo officiel centré.
- Voix off réelle (prise A, ElevenLabs Florian) : lignes placées à 1,2 · 13,0 · 29,0 · 44,0 ·
  59,5 · 77,0 · 96,5 · 111,5 s. Les apparitions sont calées sur les mots (voir `assets/audio/vo_meta.json`).
- Pages du livre (4) : bleu nuit relevé, pas blanc cassé (cohérence de la charte).
- Article 165 affiché seul ; pas de sous-titre en scène 8 (texte déjà à l'écran).

## Frame 1 — L'accroche

- scene: Une particule d'or s'allume dans le noir, se multiplie en milliers, et un compteur monte jusqu'à « 2,35 milliards USD par an ».
- duration: 10s
- start: 0
- poster: 7s
- transition_in: none
- status: animated
- src: compositions/s1-accroche.html
- blueprint: dataviz-countup (cold-open counter burst)
- rules: particle-burst, counting-dynamic-scale, ambient-glow-bloom
- voiceover: "Chaque année, l'or de Kouroussa représente plus de deux milliards de dollars."

**Concept.** Le noir d'avant. Une seule étincelle, puis l'or se révèle par sa quantité : on
mesure d'abord la richesse, sans la juger.

- 0,0–0,8 : noir (`night-deep`). 0,8 : une particule `gold` s'allume au centre, halo qui
  respire. Tintement.
- 1,6–4,5 : la particule se dédouble en spirale, puis des milliers (champ de particules
  déterministe) dérivent vers l'extérieur ; le fond remonte vers `night`.
- 2,6–5,6 : compteur Playfair 900 `gold` 220px, centré légèrement au-dessus du milieu :
  « 0,00 » → « 2,35 », puis « milliards USD » (Montserrat 700, 54px) et « par an »
  (étiquette, 26px). Chiffre final tenu de 5,6 à 9,4 s (3,8 s).
- 5,8 : ligne Montserrat 400 40px `ivory` sous le compteur : « C'est la valeur de l'or extrait
  chaque année à Kouroussa. »
- **Sortie 9,0–10,4** : le compteur se dissout en particules qui s'alignent en un trait
  horizontal doré : ce trait devient le fleuve et le contour de la carte (scène 2). Souffle.
- **Pourquoi** : pose l'enjeu (la valeur) avant le manque. Le chiffre est l'argument.
- **Non** : pas de lingots, pas de pièces, pas de pluie d'or tape-à-l'œil.

## Frame 2 — Le territoire

- scene: Carte stylisée de la préfecture, trois points lumineux pulsent ; la caméra descend vers un forage vide, une classe sans équipement, un poste de santé sans électricité.
- duration: 18s
- start: 10
- poster: 22s
- transition_in: morph (trait doré → contour de carte)
- status: animated
- src: compositions/s2-territoire.html
- blueprint: grid-card-assemble (triptyque) ; carte composée de règles
- rules: svg-path-draw, sine-wave-loop, viewport-change, waterfall-entry
- voiceover: "Et pourtant, sur cette même terre, des familles attendent encore l'eau potable, des écoles équipées, des centres de santé alimentés en énergie."

**Concept.** On passe de la valeur au lieu. La même terre porte l'or et le manque.

- 10,0–13,0 : le trait doré dessine le contour de la préfecture (silhouette stylisée, moitié
  gauche du cadre) et le cours du Niger. Étiquettes : « PRÉFECTURE DE KOUROUSSA » ·
  « GUINÉE ».
- 13,0–16,0 : trois points `gold` s'allument l'un après l'autre et pulsent (anneaux), avec
  trois tintements. Légende à droite : « Trois mines ».
- 16,0–18,5 : la caméra plonge vers un point de la carte ; le contour se dissout en fines
  hachures de terrain.
- 18,5–27,0 : triptyque en trait `ivory-dim`, sans or, aligné sur les mots de la voix :
  1. **Forage** : pompe à main, seau vide, une silhouette stylisée qui attend : « Eau potable » ;
  2. **Classe** : tableau vide, bancs nus, un enfant stylisé : « École équipée » ;
  3. **Poste de santé** : bâtiment à croix, ampoule éteinte : « Centre de santé ».
- **Sortie 27,0–28,5** : le triptyque s'efface vers le haut, la carte revient en plan large ;
  souffle.
- **Pourquoi** : le contraste or / manque fonde la nécessité du fonds.
- **Non** : pas de misérabilisme, pas de foule, pas de visage, pas de couleur hors charte.

## Frame 3 — Le fil perdu

- scene: Des lignes d'or quittent la carte et s'effacent vers l'horizon ; un point d'interrogation se forme dans le vide : « Où va la part des communautés ? »
- duration: 14s
- start: 28
- poster: 38s
- transition_in: morph (la carte réduit, les mines émettent les lignes)
- status: animated
- src: compositions/s3-fil-perdu.html
- blueprint: kinetic-type-beats (question isolée) ; lignes composées de règles
- rules: svg-path-draw, depth-scatter-assemble, sine-wave-loop
- voiceover: "Le Code minier prévoit des obligations envers les communautés locales. Mais sans cadre dédié, leur suivi reste difficile à vérifier."

**Concept.** L'or part, et personne ne sait dire où. Ce n'est pas une accusation, c'est un
vide.

- 28,0–33,0 : carte réduite à gauche ; depuis les trois mines, des lignes d'or filent vers une
  ligne d'horizon à droite et s'amenuisent jusqu'à disparaître (opacité dégressive, flux de
  pointillés).
- 33,0–36,0 : dans le vide laissé, des particules résiduelles se rassemblent en un grand
  point d'interrogation (Playfair, contour pointillé `gold-deep`), à droite.
- 34,5 : texte Playfair 700 72px `ivory` : « Où va la part des communautés ? »
- **38,5–41,5 : plan fixe**, seul le point d'interrogation respire.
- **Sortie 41,0–42,5** : une page glisse depuis la droite et recouvre le vide :
  c'est la couverture du livre (scène 4). Souffle.
- **Pourquoi** : nomme le problème de traçabilité que FUTURA résout.
- **Non** : pas de flèches vers un coupable, pas de cartes de flux financier inventées.

## Frame 4 — Le socle légal

- scene: Un livre s'ouvre, les articles s'illuminent en or (« Article 130 : Contribution au Développement Local, 1 % du chiffre d'affaires pour l'or », « Article 165 ») ; les lignes d'or font demi-tour et convergent.
- duration: 16s
- start: 42
- poster: 50s
- transition_in: morph (la page devient la couverture)
- status: animated
- src: compositions/s4-socle-legal.html
- blueprint: titlecard-reveal (adapté : carte = livre) ; convergence composée de règles
- rules: ambient-glow-bloom, svg-path-draw, center-outward-expansion (inversé)
- voiceover: "La loi fixe le principe. Il manquait l'instrument pour l'appliquer, avec rigueur et transparence."

**Concept.** La loi existe déjà : elle éclaire. Elle ne fait pas encore revenir l'or, elle
lui indique le chemin.

- 42,0–45,0 : livre vectoriel (couverture `night-raised`, tranche `gold-deep`, titre
  « CODE MINIER ») s'ouvre en 3D vers la caméra ; trame géométrique au sol.
- 45,0–49,5 : page de gauche : lignes de texte en `ivory-dim` ; un bloc s'illumine en or :
  « Article 130 », « Contribution au Développement Local », et en héros « 1 % »
  (Playfair 900 160px `gold`) « du chiffre d'affaires pour l'or ». Lisible de 46,5 à 55,0.
- 49,5–51,5 : page de droite : « Article 165 » s'illumine.
- 51,5–57,0 : les lignes d'or reviennent depuis l'horizon (sens inverse de la scène 3),
  traversent les pages et convergent vers un point central qui se densifie ; le livre recule
  et s'assombrit.
- **Sortie 57,0–58,5** : tout converge en un point lumineux unique au centre. Souffle grave
  aspiré.
- **Pourquoi** : légitimité juridique ; « il manquait l'instrument » prépare la naissance.
- **Non** : pas de marteau de juge, pas de balance, pas de texte de loi inventé à l'écran.

## Frame 5 — La naissance de FUTURA-Kouroussa

- scene: Le point central éclate en couronne géométrique : l'emblème se construit, le nom s'écrit lettre par lettre, deux badges apparaissent.
- duration: 17s
- start: 58
- poster: 70s
- transition_in: morph (point → éclatement)
- status: animated
- src: compositions/s5-naissance.html
- blueprint: logo-assemble-lockup (Product_Intro)
- rules: svg-path-draw, particle-burst, waterfall-entry, spring-pop-entrance
- voiceover: "FUTURA-Kouroussa : un fonds constitué sous forme de société anonyme OHADA, né du rapport de la mission parlementaire, pour centraliser et redistribuer ces ressources de manière traçable."

**Concept.** L'instrument naît de la convergence : le point d'or devient la pépite du logo,
et une main ouverte se dessine pour la recevoir. L'or est tenu, offert, pas extrait.

- 58,0–58,6 : le point se charge au centre, puis glisse vers la gauche et éclate (particle-burst) ;
  tintements + souffle (58,6 s).
- 58,8–61,0 : la pépite se cristallise (facettes), la main se dessine dessous (tracé de la ligne),
  la pépite s'y pose à 61,0 (tintement) ; les cinq rayons jaillissent.
- 59,5 : sur « Futura Kouroussa », « FUTURA - Kouroussa » (Roboto 700 90px) s'écrit lettre par lettre.
- 61,6–63,5 : nom complet (Roboto 400 38px) : « Fonds d'Utilisation Transparente des Ressources
  Aurifères pour l'Avenir de Kouroussa ».
- 64,4 (« OHADA ») : badge « Société Anonyme OHADA » ; 65,4 (« né du rapport ») : badge « Issu
  du Rapport de Mission Parlementaire ».
- 68,2–71,8 (« centraliser et redistribuer… traçable ») : de fins pointillés d'or partent de la
  pépite et reviennent, comme des flux tracés.
- **Sortie 73,4–75,5** : textes et badges s'effacent ; le halo de la pépite s'élargit en anneau
  au centre-gauche : il devient l'anneau de gouvernance, la pépite en son cœur.
- **Pourquoi** : c'est la réponse, le cœur du film.
- **Non** : pas de logo d'entreprise, pas d'effet chromé, pas de texte en dégradé.

## Frame 6 — Une gouvernance partagée

- scene: L'anneau se divise en quatre collèges (40 / 25 / 25 / 10 %) ; trois couches de contrôle s'allument ; les montants passent des paliers de validation.
- duration: 20s
- start: 75
- poster: 84s
- transition_in: morph (anneau de l'emblème → anneau des collèges)
- status: animated
- src: compositions/s6-gouvernance.html
- blueprint: dataviz-countup (anneau, adapté sans caméra) + constellation-hub (couches concentriques)
- rules: stat-bars-and-fills, svg-path-draw, spring-pop-entrance, ambient-glow-bloom
- voiceover: "Les collectivités y détiennent la majorité. Chaque décision est encadrée, chaque dépense est auditée, chaque comptabilité est publique."

**Concept.** La transparence est une architecture : un anneau partagé, protégé par des
cercles de contrôle. Apogée musicale.

- 75,0–80,0 : l'anneau (centre x≈640) se divise en quatre arcs proportionnels ; à droite,
  la légende arrive ligne par ligne (Playfair 900 72px pour le %, Montserrat 700 34px) :
  « 40 % Collectivités locales » (`gold`), « 25 % Société civile », « 25 % Partenaires
  institutionnels », « 10 % Partenaires miniers » (nuances `gold-deep`, `gold-pale`, `ivory`).
  Sur « la majorité », l'arc 40 % s'illumine. Chiffres tenus jusqu'à 85,0 (≥ 5 s).
- 83,0–90,0 : trois anneaux concentriques s'allument autour, synchronisés avec la voix :
  « Conseil d'administration » (« encadrée »), « Comité d'audit » (« auditée »),
  « Commissaire aux comptes » (« publique »). La légende de droite bascule sur ces trois
  couches.
- 89,0–94,0 : un jeton d'or part du cœur et traverse les trois anneaux ; à chaque passage une
  coche s'allume (« Validé »). Tintement par palier.
- **Sortie 94,0–95,5** : le jeton sort de l'anneau et descend vers le bas du cadre : il
  « retombe » sur le territoire. Souffle.
- **Pourquoi** : prouve que le fonds est gouverné localement et contrôlé.
- **Non** : pas de montants ni de devises sur les jetons, pas de logos d'institutions.

## Frame 7 — Les résultats attendus

- scene: Le triptyque de la scène 2 s'allume : le forage coule, la classe s'équipe, le poste de santé s'éclaire ; un tableau de bord affiche des indicateurs qui montent. « Chaque franc suivi. Chaque résultat visible. »
- duration: 15s
- start: 95
- poster: 104s
- transition_in: morph (jeton → goutte qui tombe dans le forage)
- status: animated
- src: compositions/s7-resultats.html
- blueprint: grid-card-assemble (rappel du triptyque) + titlecard-reveal
- rules: stat-bars-and-fills, ambient-glow-bloom, spring-pop-entrance
- voiceover: "De l'eau, des écoles, des soins : des résultats que chaque communauté pourra suivre et vérifier."

**Concept.** Rappel exact de la scène 2 : mêmes dessins, mêmes places, mais l'or y coule
désormais.

- 95,0–96,0 : le triptyque réapparaît aux positions de la scène 2, encore éteint.
- 96,0–101,0 : sur « De l'eau » : l'eau jaillit du forage, le seau se remplit (gouttes
  `ivory` à reflet or) ; « des écoles » : livres et tablettes apparaissent, tableau écrit ;
  « des soins » : l'ampoule s'allume, halo `gold`. Les traits passent de `ivory-dim` à `gold`.
- 101,0–106,0 : le triptyque monte et se réduit ; un tableau de bord stylisé glisse en
  dessous : trois indicateurs (« Accès à l'eau », « Équipement scolaire », « Accès aux
  soins ») avec courbes et flèches montantes, **sans valeur chiffrée**, puce « Suivi public ».
- 103,5 : titre Playfair 700 64px : « Chaque franc suivi. Chaque résultat visible. »
- **Sortie 108,5–110,5** : les courbes des indicateurs s'aplanissent en ondes dorées
  horizontales qui traversent le cadre.
- **Pourquoi** : la promesse rendue concrète, vérifiable, sans surpromettre.
- **Non** : pas de pourcentages ni de chiffres de résultats, pas de photos.

## Frame 8 — La signature

- scene: Les ondes d'or se calent en bande tricolore rouge-jaune-vert au bas de l'écran ; emblème centré ; « L'or de Kouroussa, au service de Kouroussa. »
- duration: 10s
- start: 110
- poster: 116s
- transition_in: morph (ondes → bande)
- status: animated
- src: compositions/s8-signature.html
- blueprint: logo-assemble-lockup (Brand_Outro) + titlecard-reveal (tenue finale)
- rules: svg-path-draw, ambient-glow-bloom
- voiceover: "FUTURA-Kouroussa. L'or de Kouroussa, au service de Kouroussa."

**Concept.** Le fil d'or se pose : il devient le pays. Résolution calme.

- 110,0–112,5 : les ondes dorées ralentissent et se posent en bas du cadre, puis prennent
  leurs couleurs : rouge #CE1126, jaune #F5C518, vert #009A44 (bande pleine largeur, 14px,
  dans la marge basse).
- 111,5 (« Futura Kouroussa ») : logo officiel centré (main + pépite + rayons, 400px), puis
  « FUTURA - Kouroussa » (Roboto 700 92px) et le nom complet en deux lignes.
- 113,9 : signature Playfair 700 62px `ivory` : « L'or de Kouroussa, au service de
  Kouroussa. » (« Kouroussa » final en `gold`).
- 116,5–120,0 : tenue finale, seul le halo respire ; la musique se résout.
- **Pourquoi** : rappel du message, mot de la fin.
- **Non** : pas de fondu au noir avant 120 s, pas d'appel à l'action commercial.
