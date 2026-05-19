---
name: maquette-flash
description: "Produit la maquette de prospection d'un futur site resto = des CAPTURES DU VRAI SITE ASTRO DÉJÀ BUILDÉ (jamais une image/mockup). Pipeline : fiche d'âme → brief Stitch contraint (Claude génère) → Stitch (Mike) → sélection à l'œil (Mike) → contrat de conversion → vrai build Astro → captures. MANDATORY TRIGGERS: 'maquette flash', 'maquette-flash', 'génère la maquette pour', 'prépare la maquette de', 'brief stitch pour'. STRONG TRIGGERS (contexte resto): 'prépare une maquette pour [resto]', 'maquette pour ma visite chez', 'j'ai rdv chez X, sors la maquette'. Ne pas déclencher : hors-resto, hors-Chartres prioritaire."
---

# Maquette Flash — pipeline Stitch + vrai build Astro

> **Modèle figé le 2026-05-19** (cf `differenciation-clients.md` § Pivot). L'ancien flux « 3 maquettes Fast-food/Gastro/Traditionnel » est **abandonné**.

La maquette montrée au patron n'est **pas une image ni un concept** : ce sont des **captures du vrai site Astro déjà buildé**. Quand on présente, **80 % du travail est déjà fait** ; ce que le patron voit = ce qu'il recevra. C'est l'argument commercial, technique et psychologique central.

## Le pipeline (6 étapes)

```
fiche d'âme → brief Stitch contraint → Stitch → sélection œil → contrat conversion → vrai Astro → captures
   (Mike+Claude)   (Claude génère)     (Mike)    (Mike)        (Claude Code)      (build)   (= maquette)
```

### Étape 1 — Fiche d'âme
Remplir/charger `ame/{slug}.yml` : bloc **FAITS** (Claude pré-remplit depuis données publiques — voir `references/extraction-checklist.md`) + bloc **RESSENTIS** (Mike seul, terrain, enums) + bloc **mot_du_lieu** (3 mots ressentis). Les ressentis ne se devinent pas par IA.

### Étape 2 — Brief Stitch contraint (Claude génère)
Appliquer **`references/stitch-brief.md`** : transformer la fiche d'âme en prompt Stitch ultra-précis = direction émotionnelle + curseur **intensité (1-3)** + inventaire fixe des écrans (les Lego) + plancher exprimé en consignes + interdits. **Stitch ne reçoit jamais une toile blanche.** Sortie = un bloc texte que Mike colle dans Stitch.

### Étape 3 — Stitch (Mike)
Mike lance Stitch avec le brief. Exploration créative = le **plafond**. Plusieurs pistes possibles.

### Étape 4 — Sélection à l'œil (Mike)
Mike choisit la direction qui a l'énergie fidèle au lieu. **Direction artistique finale = son œil, non délégable.**

### Étape 5 — Conversion (Claude Code)
Appliquer **`references/conversion-contract.md`** : mapper chaque écran Stitch sur les **primitives fixes** de `templates/site-resto/`, piloter style/intensité via les variables/props existantes (jamais de composant flocon), puis valider **tout le plancher** (perf, `checklist-seo-local.md`, a11y, liste Decap, propriété, empreinte anti-jumeau).

### Étape 6 — Vrai build + captures
`npm run build` vert → captures mobile + desktop du vrai site. **C'est la maquette.** Restaurer l'environnement (settings) à la fin.

## Définition de « fini »

Vrai build qui passe **tout** le plancher (`conversion-contract.md` §2) **ET** le gate œil : *« ce resto a monté en gamme ET l'énergie est fidèle — je le vends 490 € sans rougir »*. Itérer = retoucher le **brief Stitch** (plafond), jamais raboter le plancher.

## Règles d'or

1. **Captures du vrai site, jamais un mockup.** `final ≥ maquette`.
2. **Stitch contraint, pas toile blanche.** Le plafond vit dans les Lego du plancher.
3. **Ne jamais inventer** (histoire, prix, avis). Placeholder honnête sinon.
4. **Vouvoiement** dans tous les textes générés.
5. **Photos manquantes** → galerie hors `partition.ordre` (cohérent avec l'auto-hide), pas de Picsum visible.
6. **Anti-jumeau structurel** : enregistrer l'empreinte ; collision même ville → re-orchestrer en amont (intensité/structure Stitch), jamais en rabotant le plancher.
7. **Restaurer l'environnement** à la fin (settings propre pour la session suivante).
8. **Livraison annoncée 10-15 j** même si la prod est rapide : perçu artisanal, marge d'ajustement, anti « bouton IA » (aligné `process.md`).

## Resources

- `references/stitch-brief.md` — pièce 1/2 : fiche d'âme → brief Stitch contraint
- `references/conversion-contract.md` — pièce 2/2 : gate dur Stitch → Astro
- `references/extraction-checklist.md` — quoi extraire des sources publiques (remplit les FAITS)
- `references/pitch-presentation.md` — pitch de présentation au patron
- `checklist-seo-local.md` (racine) — les 8 points SEO, appliqués par construction
- `templates/site-resto/` — les primitives fixes (le plancher), seule base de tout site
