# FUTURA-Kouroussa : synthèse stratégique pour le Maire et le Préfet

Présentation PowerPoint de 15 diapositives (16:9), projetée devant le Maire et le Préfet de Kouroussa (octobre 2026).

## Livrables

- `livrables/FUTURA-Kouroussa_Synthese_Maire_Prefet.pptx` : la présentation (1,4 Mo).
- `livrables/FUTURA-Kouroussa_Synthese_Maire_Prefet_controle.pdf` : PDF de contrôle (état final de chaque diapositive).

## Projection

- **Mode automatique (par défaut)** : Diaporama > À partir du début. Chaque diapositive avance seule après sa
  durée (Transitions > Avancer après) ; les animations s'enchaînent « Après la précédente ». Durée totale environ
  6 min 26. La dernière diapositive reste affichée (image fixe).
- **Mode manuel** : Diaporama > Configurer le diaporama > Avancement des diapositives : « Manuellement ». Les
  animations de chaque diapositive se jouent toujours seules ; un clic termine les animations en cours, le clic
  suivant passe à la diapositive suivante.
- Transitions : Fondu 0,7 s ; Morphose (1 s) à l'entrée des diapositives 4, 8 et 9 (PowerPoint 2019 ou Microsoft
  365 ; les versions plus anciennes jouent un Fondu).
- Polices : Calibri et Calibri Bold, présentes sur tout poste Windows ou Mac équipé d'Office.

## Durées

| Diapositive | Durée | | Diapositive | Durée |
|---|---|---|---|---|
| 1 Titre | 12 s | | 9 Ressources | 30 s |
| 2 Pourquoi | 25 s | | 10 Gouvernance | 30 s |
| 3 Porteurs | 20 s | | 11 Verrous | 25 s |
| 4 Mines | 30 s | | 12 Conflits d'intérêts | 25 s |
| 5 Loi | 30 s | | 13 Feuille de route | 25 s |
| 6 Mécanisme | 25 s | | 14 Proposition | 30 s |
| 7 Simulations | 25 s | | 15 Conclusion | image fixe |
| 8 Horizon financier | 30 s | | | |

## Régénérer

`python3 tools/build_deck.py` (python-pptx, lxml, Pillow) écrit le .pptx ; `tools/render_qa.sh` produit le PDF et
les vignettes de contrôle dans `qa/`. Les pictogrammes viennent de `node tools/icons.js` (react-icons, sharp).
Logos fournis par le client dans `assets/logos/source/`, rognés de leurs marges blanches (sans déformation ni
recoloration) dans `assets/logos/`.
