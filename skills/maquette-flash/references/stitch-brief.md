# Générateur de brief Stitch contraint — pièce 1/2 du moteur

> Posé le 2026-05-19 (pivot validé). Place dans le pipeline :
>
> **fiche d'âme → [CE FICHIER : brief Stitch contraint] → Stitch (Mike) → sélection à l'œil (Mike) → [conversion-contract.md] → vrai site Astro → captures = maquette**
>
> Rôle : Stitch est le **moteur du plafond créatif** (personnalité, énergie, marque). Ce fichier garantit qu'il explore **dans les Lego qu'on sait livrer vite**, pas sur une toile blanche. Sans cette contrainte, le pivot rouvre le « full custom artisanal ingérable seul ».

## Règle d'or

**Stitch ne reçoit jamais une toile blanche. Il reçoit : une direction émotionnelle forte + l'inventaire fixe des sections à designer + les lignes rouges du plancher.** Le plafond est libre *à l'intérieur* du plancher.

Claude **génère** ce brief depuis `ame/{slug}.yml`. Mike le **colle dans Stitch**. L'œil de Mike **sélectionne**. Claude ne décide jamais le ressenti.

---

## Directives permanentes — standard 2026-05-19 (à injecter dans TOUT prompt Stitch)

> Non négociable. Ces blocs vont dans **chaque** prompt généré, quel que soit le resto. Raison : sans eux, les IA retombent en patterns SaaS / template resto / app de livraison / minimalisme agency trop propre. On ne génère pas « un site » → on génère une **mobile-first editorial brand experience**.

**Reframe d'ouverture (toujours en tête de prompt) :**
`Design a mobile-first editorial brand experience (start 390px), not a website, not a template. A living, memorable real-world food brand with identifiable energy.`

**Bloc anti-minimalisme agency :**
```
Avoid quiet agency minimalism. Avoid luxury editorial emptiness.
The brand must feel alive, fast, proud and commercially confident.
Strong personality is preferred over sterile elegance.
```
**Bloc rythme du scroll :**
```
SCROLL RHYTHM: Fast rhythm. Alternate impact sections and breathing zones.
No passive long reading blocks. Each screen must create a visual punch in
under 2 seconds. The user must constantly feel movement and momentum.
```
**Bloc énergie typographique :**
```
TYPOGRAPHIC ENERGY: Typography is a core part of the brand identity.
Strong scale contrast. Some headlines almost poster-like. Large confident
type over decorative UI tricks. Bold hierarchy creates energy, not gimmicks.
```
**Bloc interdits app/SaaS :**
```
This is NOT a delivery app UI. NOT a SaaS dashboard. NOT a generic
restaurant template. This is a real-world food brand experience.
```
**Bloc ancrage physique :**
```
The design must feel rooted in the real physical place (truck / room /
street presence). A real local brand that already exists physically —
not a fictional startup concept.
```
**Règle de priorité (toujours rappelée) :** le but n'est pas « faire beau ». Un passant doit comprendre **immédiatement** : ce que c'est · combien · pourquoi c'est spécial · comment commander. **La clarté commerciale prime sur la décoration.**

**Contrainte de réalisme (toujours en fin de prompt) :** concepts réellement buildables, compatibles Astro, mobile-first réels, SEO-compatibles, performants, sans effets impossibles à maintenir. *Des marques fortes, pas des concepts Dribbble incodables.* (Le détail du plancher est gaté par `conversion-contract.md`.)

**Modèle mental de raisonnement (pour générer N'IMPORTE quel prompt) :**
`INPUTS humains` (type cuisine · gamme prix · énergie · ambiance · clientèle · ton patron · densité menu · présence Insta · niveau premium · rythme du lieu · identité implicite · présence physique · sensation émotionnelle) **→** `OUTPUTS créatifs` (rythme · DA · composition · densité · hiérarchie · structure · énergie typo · comportement du scroll · intensité commerciale). Objectif constant : **tuer la sensation « template IA »**.

---

## Structure du brief généré (gabarit à remplir depuis la fiche d'âme)

### 1. Capsule identité (FAITS)
`{Nom}` · `{ville}` · `{type_cuisine}` · gamme `{€/€€/€€€}` · les **3 mots du lieu** (`mot_du_lieu`, ressenti humain — c'est le cœur du ton).

### 2. Mission du site (SPINE)
- Spine : `{commander | venir | desirer}`
- Objectif unique en une phrase (ex. S1 : « faire commander/appeler en moins de 5 s, preuve sociale immédiate »).
- **CTA principal** imposé par le spine (S1 commander/appeler · S2 réserver = appel · S3 réservation en ligne).

### 3. Direction émotionnelle (RESSENTIS → vocabulaire créatif)
Traduire les enums en adjectifs + références d'énergie. Table déterministe :

| Ressenti | Donne à Stitch |
|---|---|
| ambiance vive / brute | contrastes francs, gros titres assumés, photo qui claque, énergie de rue |
| ambiance feutrée | beaucoup de noir/vide, lenteur, retenue, luxe discret |
| énergie électrique/dynamique | rythme serré, accents forts, mouvement présent (sobre) |
| énergie calme/posée | espace, silence visuel, peu d'éléments |
| sophistication populaire | direct, généreux, prix gros et fiers |
| sophistication soignée | « street premium » : énergie + soin typographique au-dessus du lot |
| sophistication haut de gamme | éditorial, grande photo désir, narratif |
| clientèle jeunes urbains | mobile-snack, Insta-friendly, marque forte |
| clientèle familles | réassurance, chaleur, avis remontés |
| ton patron fier/passionné | une zone « fierté » qui crie (le 1er, depuis X) |

### 4. Curseur INTENSITÉ (1→3) — c'est LUI qui restaure le plafond
Le moteur figé avait tué ça. Ici on l'assume :
- **1 — sobre éditorial** (gamme haute, feutré, intime)
- **2 — affirmé** (soigné, chaleureux, dynamique)
- **3 — marque agressive** (vif/brut, populaire, jeunes urbains, ton showman)

Déduit de la fiche d'âme, **tranché par l'œil de Mike**. Kroosti = **3**.

### 5. Inventaire des écrans à designer (LES LEGO — non négociable)
Stitch doit produire un écran mobile **pour chacune** de ces sections, **dans l'ordre du spine**, et **aucune section hors liste** (sinon = flocon non livrable) :

`hero ({variante}) · avis · menu · reservation · histoire · exigence · localisation · reseaux`

Pour chaque section : 1 ligne d'intention (« avis = arme de conversion, énorme, juste après le hero » ; « menu = lisible au pouce, prix gros »). L'ordre vient de `partition.ordre`.

### 6. Plancher exprimé en consignes Stitch (le garde-fou)
À écrire tel quel dans le prompt Stitch :
- **Mobile-first 390 px d'abord.** Tout doit tenir et convertir au pouce.
- **La photo réelle est la star**, jamais retouchée-colorée, jamais un voile de couleur dessus.
- **Une seule couleur d'accent = `{dominante réelle}`**, dosée (CTA, repères, 1 mot). Jamais en fond plein, jamais sur la photo.
- **2 familles de police maximum**, classiques et auto-hébergeables (pas de polices exotiques non subsetables — la vitesse est une condition d'admission).
- **Zéro effet lourd** : pas de parallaxe, pas de scroll-jacking, pas de vidéo de fond, pas de carrousel auto. Mouvement = apparitions sobres.
- **Espace généreux, hiérarchie forte.** La personnalité vient du contraste et de l'audace typo, pas de la décoration ajoutée.
- **Contraste lisible (AA)**, cibles tactiles ≥ 44 px.

### 7. Interdits Stitch (lignes rouges)
Faux contenu/avis inventés · clichés déco resto (fourchettes géantes, ardoise, scotch) · texte sur photo illisible · carrousels · sections hors inventaire · tout ce qui ne se build pas vite en Astro statique.

### 8. Sortie attendue de Stitch
Écrans mobiles, un par section de l'inventaire, dans l'ordre. C'est ce que l'œil de Mike juge, puis ce que la conversion (`conversion-contract.md`) transforme en vrai Astro.

---

## Rappels

- **Brief flou = Stitch confiant dans le médiocre.** La rigueur de la fiche d'âme est PLUS critique ici, pas moins.
- Le « 2 h » de Kroosti = Mike connaissait sa marque par cœur. Pour un prospect vu une fois, la fiche d'âme **remplace** ce savoir tacite. Ne pas sauter l'étape ressentis terrain.
- Claude génère le brief, **jamais** le ressenti ni la sélection. L'œil humain reste directeur artistique.
