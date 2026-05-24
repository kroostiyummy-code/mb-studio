# 04 — Workflow d'orchestration MB Studio

## Vue d'ensemble du pipeline

```
INPUT
  Nom du resto + ville (+ optionnel : URL GMB, photos, infos)
    ↓
[AGENT 1] Fiche restaurant + Fiche d'âme (10 axes)
    ↓
    [VALIDATION MIKE — Y/N]
    ↓
[AGENT 2] Copywriting SEO (settings.yml prêt à coller)
    ↓
    [VALIDATION MIKE — Y/N]
    ↓
[AGENT 3] Prompt Stitch complet (en anglais, prêt à coller)
    ↓
    [VALIDATION MIKE — Y/N]
    ↓
[ÉTAPE MANUELLE] Stitch → ZIP design
    ↓
[CLAUDE CODE] Conversion ZIP → site Astro
    ↓
[ÉTAPE MANUELLE] Déploiement Cloudflare Pages
    ↓
[ÉTAPE MANUELLE] Screenshots → préparation RDV
    ↓
OUTPUT
  Site déployé + screenshots prêts pour démarchage
```

## Étape 1 — Agent fiche restaurant

### Inputs requis
- **Obligatoire** : nom exact du restaurant + ville
- **Très utile** : URL Google Maps / GMB, lien Instagram, lien menu existant
- **Optionnel** : photos disponibles, objectif business prioritaire, ambiance perçue

### Process de l'agent
1. Recherche les infos publiques disponibles (GMB, sites d'avis, réseaux sociaux)
2. Structure une fiche identité (adresse, horaires, contact, type de cuisine, fourchette de prix)
3. Identifie les forces apparentes via les avis
4. Identifie les manques critiques à confirmer avec le patron
5. Remplit la fiche d'âme selon les 10 axes (avec tags `[CONFIRMÉ]` ou `[SUPPOSÉ]`)
6. Propose 2-3 références cinématographiques cohérentes
7. Suggère une combinaison DA + Typo + Hero + Spine + Ton (à vérifier contre le registre anti-jumeau)

### Output attendu

```markdown
# Fiche restaurant — [Nom]

## Identité publique
- **Nom** : [exact] [CONFIRMÉ]
- **Adresse** : [...] [CONFIRMÉ/SUPPOSÉ]
- **Téléphone** : [...] [CONFIRMÉ/SUPPOSÉ]
- **Horaires** : [...] [CONFIRMÉ/SUPPOSÉ]
- **Note GMB** : [X.X/5 sur N avis] [CONFIRMÉ]
- **Type de cuisine** : [...]
- **Fourchette de prix** : [10-20€ / 20-40€ / 40€+]

## Forces apparentes (depuis avis GMB)
- [Force 1 avec citation d'avis si possible]
- [Force 2]
- [Force 3]

## À CONFIRMER AVEC LE PATRON
- [Manque critique 1]
- [Manque critique 2]
- [...]

## Fiche d'âme (10 axes)

1. **Température émotionnelle** : [...]
2. **Rôle social** : [...]
3. **Densité sensorielle** : [...]
4. **Preuves physiques** :
   - Photos disponibles : [...]
   - Photos manquantes critiques : [...]
5. **Moment dominant** : [...]
6. **Vitesse émotionnelle** : [...]
7. **Sensation finale recherchée** : "[phrase exacte]"
8. **Références culturelles** : [...]
9. **CE QUE LE LIEU N'EST PAS** :
   - [Anti-direction 1]
   - [Anti-direction 2]
   - [Anti-direction 3]
10. **Mémoire émotionnelle** : [...]

## Direction artistique suggérée

- **Références cinématographiques** : [2-3 références du catalogue MB Studio]
- **Combinaison anti-jumeau proposée** :
  - DA : [Dark_Lounge / Bistrot_Patine / etc.]
  - Pack typo : [Editorial / Modern_Soft / etc.]
  - Structure hero : [Direct / Editorial / Cinematique / etc.]
  - Spine commercial : [VENIR / RESERVER / APPELER / COMMANDER / DECOUVRIR]
  - Ton de copy : [Sensoriel_premium / Chaleureux_populaire / etc.]

## Vérification anti-jumeau
[À compléter automatiquement contre le registre clients]
```

### Validation Mike
Mike relit, corrige les `[SUPPOSÉ]` qui sont faux, valide ou ajuste la combinaison anti-jumeau. **Si Mike rejette la fiche, Agent 1 est relancé avec les corrections.** On ne passe à l'étape 2 que sur fiche validée.

---

## Étape 2 — Agent copywriting

### Inputs requis
- Fiche restaurant validée à l'étape 1 (passée intégralement)
- Confirmation du pack typo et de la DA choisis

### Process de l'agent
1. Lit la fiche d'âme et la combinaison anti-jumeau
2. Produit le copy section par section, calibré sur :
   - Le ton choisi (sensoriel premium / chaleureux populaire / etc.)
   - La sensation finale recherchée
   - Les références culturelles précises
   - Les anti-directions à éviter
3. Intègre naturellement le SEO local (ville + cuisine + spécialité dans hero et meta)
4. Évite les phrases mortes interdites
5. Sort un fichier YAML directement injectable dans le template Astro

### Output attendu

```yaml
# settings.yml — [Nom du resto]

meta:
  title: "[Nom] — [Type cuisine] à [Ville]" # Max 60 caractères
  description: "[Accroche émotionnelle + CTA + ancrage local]" # Max 155 caractères

hero:
  surtitre: "[Type cuisine] à [Ville]"
  titre: |
    [Headline 5-8 mots, évocateur]
    [Suite éventuelle sur 2-3 lignes max]
  texte: "[Sous-headline 15-20 mots, ancrage géo + promesse]"
  cta_principal: "[Verbe d'action + bénéfice]"

a_propos:
  titre: "[Titre éditorialisé, pas 'À propos']"
  texte: |
    [80-120 mots, ton à hauteur de la DA]
    [Histoire du lieu, valeur, sincérité]

carte:
  intro: "[30-50 mots qui donnent faim]"
  plats_signatures:
    - nom: "[...]"
      description: "[10-15 mots sensoriels]"
    - nom: "[...]"
      description: "[...]"
    # 3-5 plats max

ambiance:
  titre: "[Évocation sensorielle]"
  texte: |
    [50-80 mots sensoriels : lumière, matière, son, odeur]

venir:
  titre: "[Variation de 'Nous trouver']"
  adresse: "[À COMPLÉTER AVEC PATRON]"
  acces: "[Métro / parking / repère visuel]"
  horaires:
    [À COMPLÉTER AVEC PATRON]

ctas_secondaires:
  - "[Variation 1]"
  - "[Variation 2]"
  - "[Variation 3]"

footer:
  baseline_memoire: "[Phrase courte qui porte la mémoire émotionnelle]"

À_CONFIRMER_AVEC_PATRON:
  - "Prix exacts des plats signatures"
  - "Allergènes pour chaque plat"
  - "Horaires précis (variations week-end ?)"
  - "URL Google Avis pour CTA fonctionnel"
  - "Photos haute définition du lieu"
```

### Validation Mike
Mike relit le copy. Si une section sonne générique, le patron ne se reconnaît pas, ou la sensation finale n'est pas atteinte, l'agent est relancé. **Critère de validation** : "Le restaurateur dirait-il 'c'est mon resto' en lisant ce copy ?"

---

## Étape 3 — Agent prompt Stitch

### Inputs requis
- Fiche restaurant + fiche d'âme (étape 1 validée)
- Copywriting complet (étape 2 validée)
- Combinaison anti-jumeau confirmée

### Process de l'agent
1. Lit toute la fiche d'âme et le copy
2. Construit un prompt Stitch **en anglais** (Stitch comprend mieux l'anglais) qui :
   - Précise explicitement "All visible website copy must be in French"
   - Pose l'atmosphère AVANT toute spec UI
   - Décrit le lieu comme un endroit physique, pas comme une catégorie web
   - Intègre le copy réel (pas de lorem ipsum)
   - Spécifie les références cinématographiques choisies
   - Liste les anti-références à éviter
   - Définit mobile-first explicitement (375/768/1440)
   - Mentionne les contraintes : schema.org Restaurant, performance, accessibilité de base

### Output attendu

```
Design a mobile-first hospitality experience for "[Nom]" in [Ville].

All visible website copy must be in French (provided below).

==================================
ATMOSPHERE FIRST. FOOD SECOND. INTERFACE THIRD.
==================================

This is NOT [anti-catégorie 1], NOT [anti-catégorie 2], NOT [anti-catégorie 3].

This IS:
[Description sensorielle du lieu en 3-5 lignes — lumière, matière, son, énergie humaine]

==================================
THE VISITOR SHOULD FEEL:
==================================

After 5 seconds on mobile, the visitor must think:
"[Phrase finale exacte, en français]"

==================================
VISUAL DIRECTION
==================================

References to draw from:
- [Référence 1] for [aspect précis]
- [Référence 2] for [aspect précis]
- [Référence 3] for [aspect précis]

References to explicitly AVOID:
- No Sketch.com / Linear / Stripe aesthetic (this is hospitality, not tech)
- No [autres anti-références spécifiques]

Color palette:
- Primary: [#hex]
- Secondary: [#hex]
- Accent: [#hex]
- Background: [#hex]

Typography:
- Headlines: [Font Family] (with fallback)
- Body: [Font Family] (with fallback)

Photography style:
[Description précise du style photo : grain pellicule, golden hour, etc.]

==================================
STRUCTURE (mobile-first 375px, then 768px, then 1440px)
==================================

1. HERO — [Type structure]
   - [Description visuelle]
   - Copy:
     Surtitre: "[exact]"
     Titre: "[exact]"
     Sous-titre: "[exact]"
     CTA: "[exact]"

2. [SECTION 2]
   - [Description visuelle]
   - Copy:
     [...]

[... toutes les sections du copy ...]

==================================
TECHNICAL REQUIREMENTS
==================================

- Mobile-first (375px minimum), responsive at 768px and 1440px
- Schema.org Restaurant JSON-LD included
- Accessible color contrasts (WCAG AA)
- Lightweight, no heavy animations that hurt LCP
- French language declared in HTML
- Open Graph tags ready

==================================
THE WEBSITE MUST FEEL LIKE A PHYSICAL PLACE BEFORE IT FEELS LIKE A WEBSITE.
==================================
```

### Validation Mike
Mike relit le prompt. Vérifications clés :
- L'atmosphère est-elle posée avant les specs UI ?
- Le copy réel est-il inclus (pas lorem ipsum) ?
- Les anti-références sont-elles explicites ?
- La sensation finale est-elle clairement énoncée ?

Si OK, le prompt est copié dans le presse-papier et Mike le colle dans Stitch.

---

## Étape 4 — Stitch (manuel)

Mike colle le prompt dans Stitch, génère le design, itère si besoin (Stitch propose des variations), télécharge le ZIP final.

**Temps estimé** : 15-30 minutes selon la complexité et les itérations.

---

## Étape 5 — Claude Code conversion Astro

Mike ouvre Claude Code, lui donne le ZIP Stitch + la fiche restaurant complète + le copy YAML, et demande :

> *"Convertis ce design Stitch en site Astro fonctionnel. Utilise le template MB Studio standard. Injecte le copy YAML dans settings.yml. Génère les composants Astro nécessaires. Configure schema.org Restaurant. Optimise pour mobile-first. Sors un build prêt à déployer."*

Claude Code produit le projet Astro complet dans `prospects/[slug]/site/`.

**Temps estimé** : 30-60 minutes incluant les ajustements.

---

## Étape 6 — Déploiement Cloudflare Pages

Mike push le projet sur un repo GitHub privé dédié au client, connecte Cloudflare Pages au repo, configure le domaine temporaire `[slug].pages.dev` pour la démo.

**Temps estimé** : 10-15 minutes.

---

## Étape 7 — Screenshots pour démarchage

Mike prend des captures du site en mobile (375px) et desktop (1440px) :
- Hero
- Section ambiance
- Carte / plats signatures
- Footer mémoire

Format : PDF ou galerie photo iPhone, JAMAIS l'URL en clair (anti-siphonnage).

**Temps estimé** : 5-10 minutes.

---

## Temps total de production par site

| Étape | Temps premier site | Temps 10ème site |
|---|---|---|
| Agent 1 (fiche) | 20 min | 10 min |
| Validation Mike | 10 min | 5 min |
| Agent 2 (copy) | 20 min | 10 min |
| Validation Mike | 15 min | 5 min |
| Agent 3 (prompt Stitch) | 15 min | 10 min |
| Validation Mike | 10 min | 5 min |
| Stitch | 30 min | 15 min |
| Claude Code Astro | 60 min | 30 min |
| Déploiement Cloudflare | 15 min | 10 min |
| Screenshots | 10 min | 5 min |
| **TOTAL** | **~3h** | **~1h45** |

**Objectif** : descendre à 1h30 par site au 20ème site, en production batch de 5.

## La règle d'or de l'orchestration

**Toujours valider entre chaque étape.**

Tentation : laisser tourner les 3 agents en chaîne sans intervention. Résultat : un agent dérive, l'erreur se propage, le site final est faux à 80%.

Avec validation : 5 minutes investies par étape évitent 2h de refonte en bout de chaîne. Le ROI de la validation est de 24×.

## Le fichier de tracking par client

Pour chaque client, créer un dossier `prospects/[slug]/` contenant :

```
prospects/al-badea-chartres/
├── 01-fiche-restaurant.md       # Output Agent 1 validé
├── 02-copywriting.yml           # Output Agent 2 validé
├── 03-prompt-stitch.txt         # Output Agent 3 validé
├── 04-stitch-output.zip         # ZIP téléchargé de Stitch
├── 05-site-astro/               # Projet Astro complet
├── 06-screenshots/              # Captures pour démarchage
│   ├── mobile-hero.png
│   ├── mobile-ambiance.png
│   └── desktop-overview.png
├── 07-rdv-notes.md              # Retours du restaurateur
└── README.md                    # Statut et historique
```

Cette structure permet de reprendre n'importe quel client à n'importe quelle étape, et de documenter les apprentissages au fil des projets.
