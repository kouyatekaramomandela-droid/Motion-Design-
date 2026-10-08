---
name: FUTURA-Kouroussa — film institutionnel
colors:
  night: "#1A2A3A"        # fond bleu marine profond (client)
  night-deep: "#0F1A25"   # bord de vignette / ouverture noire (teinte du fond, jamais #000)
  night-raised: "#22364A" # panneaux, livre, tableau de bord
  gold-deep: "#B8860B"    # or profond (client) — traits, structure, ombres dorées
  gold: "#F5C518"         # or lumineux (client) — énergie, focal, chiffres
  gold-pale: "#F8DF7A"    # halo / reflet chaud (dérivé de gold)
  ivory: "#F3EEE3"        # blanc cassé — textes
  ivory-dim: "#A9B3BC"    # texte secondaire, traits « manque » (scènes 2 et 3)
  flag-red: "#CE1126"     # bande tricolore, scène 8 uniquement
  flag-green: "#009A44"   # bande tricolore, scène 8 uniquement
  night-black: "#070C12"  # écran noir d'ouverture (scène 1, 0–4 s)
  # couleurs du logo client (pépite et rayons), utilisées uniquement dans l'emblème
  logo-ray: "#C9A44A"
  logo-nugget: ["#D4A93A", "#E9C24A", "#E0B02A", "#D9A92A", "#C99A1E", "#A87A0B"]
typography:
  display:
    family: "Playfair Display"
    weights: [700, 900]
    use: titres, chiffres héros, signature
    tracking: "-0.02em"
  sans:
    family: "Montserrat"
    weights: [400, 700]
    use: textes, étiquettes, badges, sous-titres
  brand:
    family: "Roboto"
    weights: [400, 700]
    use: logo uniquement (« FUTURA - Kouroussa » et nom complet), fidèle au logo fourni
  label:
    family: "Montserrat"
    weight: 700
    case: uppercase
    tracking: "0.18em"
    size: "22–26px"
spacing:
  safe-margin: "5%"       # 96px en 16:9, 54px latéral / 96px vertical en 9:16
  caption-zone: "bas, au-dessus de la marge de 5 %"
radii:
  badge: "999px"
  panel: "18px"
motion:
  ease-enter: "power3.out"
  ease-move: "sine.inOut"
  ease-settle: "expo.out"
  ease-morph: "power2.inOut"
  min-number-hold: "2s"
---

## Overview

Un film d'État, pas une publicité. La lumière dorée est la seule source d'énergie du cadre :
elle naît, se perd, revient, se met en ordre. Tout le reste est nuit calme et blanc cassé.

## The Frame

- Fond uni `night` avec halo radial doré localisé (jamais de dégradé linéaire plein cadre) et
  un grain très fin. Une trame géométrique discrète (losanges, 8–12 % d'opacité) sert de sol
  aux scènes institutionnelles (4, 5, 6).
- Le **fil d'or** (particules + traits `gold`) est l'élément persistant : il relie chaque scène
  à la suivante par morphing, jamais par coupe.
- Les traits « manque » (scènes 2 et 3) sont en `ivory-dim`, sans or. Les mêmes dessins
  reviennent dorés en scène 7.

## Composition Rules

- Texte toujours ≥ 28px en 16:9 (≥ 36px en 9:16), titres ≥ 72px, chiffres héros ≥ 180px.
- Sous-titres : Montserrat 700, 40px (16:9) / 46px (9:16), `ivory` sur bandeau `night` à
  70 %, deux lignes max, centrés, dans la marge de sécurité de 5 %. Le contenu reste au-dessus
  de la zone sous-titres.
- Chaque chiffre reste lisible au moins 2 s.

## Do

- Morphing de formes, courbes douces, tintements sur les apparitions de particules.
- Personnages stylisés géométriques, sans visage ni traits.

## Don't

- Aucun visage réel, aucun logo ni nom de société minière, aucune pelleteuse, aucune foule.
- Rouge et vert hors de la bande tricolore finale.
- Aucun chiffre de résultat non cité par le client (tableau de bord sans valeurs).
- Pas de coupe sèche, pas de texte en dégradé, pas de néon.
