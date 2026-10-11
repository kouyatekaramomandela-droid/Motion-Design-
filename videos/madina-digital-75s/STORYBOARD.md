---
format: 1920x1080 + 1080x1920
duration: 75s
message: "Madina Digital réunit 12 services du quotidien dans une seule application, simple et sûre, partout en Guinée."
arc: Logo → Contexte Guinée → Inscription → Connexion et accueil → 12 modules → Bénéfices → Signature
audience: grand public guinéen, partenaires, site et réseaux sociaux
mode: collaborative
---

Planche : `storyboard.html` (image : `sketches/storyboard-v1.jpg`), tirée des compositions déjà montées.
Fil conducteur : la lumière orange (curseur, particules, halos) qui guide l'œil de séquence en séquence.

## Still open

- Planche v1 envoyée ; film v1 livré.
- Voix off : Gemini TTS (voix Puck), validée par le client.
- v2 (demande du client : « aller au-delà des images fournies ») : 18 illustrations générées dans Canva, validées
  sur planche (`renders/apercus/planche_images_v2.jpg`, liste et prompts dans `assets/generated/canva_media.json`).
  S2, S5, S6 et S7 refaits avec elles ; voix et musique inchangées.

## Frame 1 — Logo
- duration: 6s
- status: animated
- src: scenes/s1.frag.html
- voiceover: "Madina Digital."

## Frame 2 — Contexte Guinée
- duration: 6s
- status: animated
- src: scenes/s2.frag.html
- voiceover: "En Guinée, tout va vite. Avec Madina Digital, tout est à portée de main."
- v2: plan drone sur Conakry au lever du soleil (poussée vers le phare), coupe rapide sur le phare de Kaloum
  (« tout va vite »), puis le cadre se referme sur la photo de l'écran d'inscription (« Avec Madina Digital »).

## Frame 3 — Inscription
- duration: 10s
- status: animated
- src: scenes/s3.frag.html
- voiceover: "Créer votre compte ? Quelques secondes suffisent. Votre nom, votre numéro, votre e-mail, un mot de passe… et c'est validé !"

## Frame 4 — Connexion et accueil
- duration: 8s
- status: animated
- src: scenes/s4.frag.html
- voiceover: "Connectez-vous… et tout s'ouvre à vous : plus qu'une super-application, une vie plus simple !"

## Frame 5 — Les 12 modules
- duration: 27s
- status: animated
- src: scenes/s5.frag.html
- voiceover: "Douze modules, une seule application. Makiti pour vos courses, … et Move, pour vous déplacer et vous faire livrer."
- v2: les 12 tuiles sortent de l'accueil et forment un rail (une rangée en 16:9, deux rangées de six en 9:16) ;
  chaque module ouvre sa photo (plein cadre en 16:9, carte sur fond flouté en 9:16) par un cercle, une poussée ou
  un zoom, pendant que sa tuile se soulève et s'allume.

## Frame 6 — Bénéfices
- duration: 9s
- status: animated
- src: scenes/s6.frag.html
- voiceover: "Paiement sécurisé. Livraison rapide. Un service client vingt-quatre heures sur vingt-quatre. Une expérience unique. Votre vie, plus simple !"
- v2: une photo par bénéfice derrière les badges (paiement sans contact, colis livré, conseillère, famille).

## Frame 7 — Signature
- duration: 9s
- status: animated
- src: scenes/s7.frag.html
- voiceover: "Madina Digital : commander, recevoir, vivre mieux… partout en Guinée."
- v2: Conakry en bleu nuit, très discrète, derrière le logo et les chiffres.
