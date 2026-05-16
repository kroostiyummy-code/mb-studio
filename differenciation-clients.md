# Différenciation inter-clients — standard MB Studio

> Posé en session le 2026-05-16. Répond à une question de Mike : **être sûr que deux sites livrés ne se ressemblent jamais.**
>
> Principe : dans une ville où les patrons se connaissent et comparent, deux sites « cousins » détruisent le pitch « conçu sur mesure » (bon de commande, honnêteté radicale) et le bouche-à-oreille (chaque client = ambassadeur). **L'unicité inter-clients est un engagement de fabrication non-négociable**, au même titre que le SEO local.

## État honnête du template aujourd'hui

Ce qui différencie déjà fortement deux sites :
- **3 signatures** (Brutaliste / Élégante / Tradition) : différence profonde (polices, mode de couleur, texture, densité, formes).
- **Couleur dominante** du patron, propagée partout.
- **Sections ON/OFF** + mode fixe/foodtruck + **contenu unique** (renforcé par le standard SEO local).

Le trou réel (confirmé en lisant le code) :
- L'**ordre des sections est figé en dur** (`index.astro`), identique pour tous.
- Le **Hero a une seule mise en page**.
- Il n'y a que **3 jeux typographiques**.

→ Avec 3 signatures pour 5+ clients, au moins deux clients partagent une signature **et** le même squelette. C'est le risque à fermer **avant** les 5 premiers clients.

---

## Les 4 couches de défense

### Couche 1 — Matrice d'attribution (organisationnel, applicable AUJOURD'HUI)

Règle : **jamais deux restos voisins ou de même type de cuisine sur la même combinaison.** Une combinaison = `signature + variante de Hero + pack typo + dominante`.

Tableau de suivi à tenir, un client = une ligne, avant toute production :

| Client | Quartier/Commune | Cuisine | Signature | Variante Hero | Pack typo | Dominante | Combinaison déjà prise ? |
|---|---|---|---|---|---|---|---|
| _(à remplir au fil des clients)_ | | | | | | | |

Règle de blocage : si la combinaison exacte existe déjà chez un client **dans la même ville**, on change au moins **deux** axes (pas seulement la couleur).

### Couche 2 — Variantes de structure (à construire, PC allumé)

But : même signature ≠ même squelette.

- **Hero : 3 mises en page** au choix par client (champ piloté par Mike dans `settings/site.yml`, jamais exposé Decap). Pistes : (a) photo plein cadre + titre superposé [actuel], (b) split titre / photo côte à côte, (c) typographique sans photo de fond (titre massif + filet). Chaque variante doit rester compatible avec les 3 signatures.
- **Ordre des sections paramétrable** : remplacer l'ordre figé de `index.astro` par une liste ordonnée lue depuis `settings/site.yml` (ex. `ordre: [hero, menu, histoire, avis, ...]`). Prévoir 2-3 « parcours » pré-validés pour que Mike ne parte pas de zéro, mais l'ordre reste modifiable client par client.
- Garde-fou : toute variante doit passer le standard SEO local et ne pas alourdir (cf Couche 3).

### Couche 3 — Packs typographiques (point ajouté par Mike : ne pas rester à 3 polices)

Principe : **la signature définit l'ESPRIT typographique, le pack typo varie les POLICES réelles** à l'intérieur de cet esprit.

- Chaque signature reçoit un **petit pool de 3-4 paires de polices** cohérentes avec son ADN (ex. Brutaliste : Archivo Black/Bebas, mais aussi d'autres familles « display lourde » compatibles ; Élégante : plusieurs serif raffinées ; Tradition : plusieurs slab/serif chaleureuses).
- Mike choisit le pack par client (champ `settings`, non exposé Decap), guidé par l'identité du resto au brief.
- **Budget performance non négociable** (car le SEO local impose la vitesse) : **2 familles maximum par site**, polices sous-ensemblées (subset latin), `preload` + `font-display: swap`, auto-hébergées (pas de chargement tiers bloquant). Un pack qui dégrade les Core Web Vitals est refusé. C'est l'anti-pattern « effet lourd » appliqué aux polices.
- Résultat combinatoire : 3 signatures × ~3 packs typo × 3 Hero × ordre variable × dominante → l'unicité devient structurelle, plus une question de chance.

### Couche 4 — Garde-fou anti-jumeau dans `audit-livraison`

Avant chaque livraison, le skill `audit-livraison` compare le nouveau site aux sites Chartres **déjà livrés** et **bloque** si trop proche. Spec détaillée ajoutée dans `skills/audit-livraison/SPEC.md`. La différence devient **vérifiée**, pas espérée.

---

## Ce qui est fait aujourd'hui (PC éteint) vs à câbler (PC allumé)

- **Fait maintenant** : ce document, la règle non-négociable dans `CLAUDE.md`, la matrice d'attribution (utilisable dès le 1er client), la spec du garde-fou dans `audit-livraison`.
- **À construire quand le PC sera rallumé** : variantes de Hero, ordre de sections paramétrable, packs typo (build + test visuel + test perf obligatoires — rien validé sans build).
