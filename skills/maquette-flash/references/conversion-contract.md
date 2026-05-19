# Contrat de conversion Stitch → Astro — pièce 2/2 du moteur

> Posé le 2026-05-19 (pivot validé). Place dans le pipeline :
>
> fiche d'âme → brief Stitch → Stitch → sélection à l'œil → **[CE FICHIER]** → vrai site Astro → captures = maquette
>
> Rôle : le **plancher technique et garde-fou**. Stitch monte le plafond ; ce contrat garantit que le design choisi devient un site **rapide, éditable, possédé, non-jumeau, livrable seul**. Rien ne sort tant que ce contrat n'est pas vert. C'est ce qui empêche « 2 h pour Kroosti » de devenir « 2 jours à se battre contre un Stitch injouable » au client #4.

## Principe

Le design Stitch choisi pilote **le style et l'intensité À L'INTÉRIEUR des primitives Astro fixes**. Il ne crée **jamais** de composant sur-mesure. Un site = toujours le template `templates/site-resto/`, jamais un flocon.

---

## 1. Mapping écran Stitch → composant fixe (obligatoire)

Chaque écran Stitch se mappe sur **un** composant existant de `templates/site-resto/src/components/sections/` :

`hero → Hero.astro` (variante `direct|editorial|cinematique`) · `avis → Avis` · `menu → Menu` · `reservation → Reservation` · `histoire → Histoire` · `exigence → Exigence` · `localisation → Localisation` · `reseaux → Reseaux` · bandeau/footer/sticky = ancrés.

Règles :
- Stitch invente une section sans primitive → on **mappe sur la plus proche** ou c'est **hors périmètre** (pas de nouveau composant bespoke).
- L'**ordre** = `partition.ordre` ; le **CTA** = le spine. Stitch ne les renégocie pas.
- Le design Stitch influence : palette d'accent, intensité typo, densité, mise en scène photo, rythme — **via les variables/props existantes**, pas via du CSS flocon par client.

## 2. Plancher non négociable (TOUT doit passer avant « captures = maquette »)

- [ ] **Perf** : LCP mobile < 2,5 s ; image hero optimisée (< ~250 Ko servie) ; **≤ 2 familles de police**, auto-hébergées, `preload` + `font-display: swap` ; **0 requête tierce bloquante** ; JS minimal ; `npm run build` vert.
- [ ] **SEO local** : conforme **par construction** aux 8 points de `checklist-seo-local.md` (racine du repo). Ne pas dupliquer la liste — l'appliquer.
- [ ] **Accessibilité** : contraste AA, `:focus-visible` visible, cibles ≥ 44 px, `prefers-reduced-motion` respecté, hiérarchie Hn sémantique.
- [ ] **Édition patron (Decap)** : le patron édite **uniquement** horaires · photos · menu · certains textes · CTA. **Tout le reste verrouillé** (structure, design, perf, SEO technique). La conversion ne doit pas casser cette liste.
- [ ] **Propriété** : 1 repo/client, déployable Cloudflare Pages, **archivable sous 48 h**. Rien d'introduit qui casse la transférabilité (pas de dépendance payante, pas de service fermé).
- [ ] **Anti-jumeau** : enregistrer l'**empreinte** (`spine + intensité + variante hero + ordre dominant des sections + famille de palette`) dans le registre de `audit-livraison` (étape 7bis). Collision même ville → re-orchestration **en amont** (on rejoue le brief Stitch avec une intensité/structure différente — **jamais** en rabotant le plancher).
- [ ] **Honnêteté** : ce qu'on montre au patron = **captures du vrai site buildé**. `final ≥ maquette` (le brief réel + photos ne font qu'améliorer).

## 3. Lignes rouges — ce que Stitch n'a JAMAIS le droit de casser

Voile de couleur sur la photo · > 2 polices ou police non subsetable · effet lourd (parallaxe, vidéo fond, scroll-jack, carrousel auto) · composant bespoke hors primitives · champ verrouillé rendu éditable (ou inverse) · dépendance payante / service fermé · contenu inventé. Une seule de ces lignes franchie = la conversion est refusée, on retourne au brief Stitch.

## 4. Définition de « fini »

Vrai build Astro qui **passe tout le §2** **ET** franchit le **gate œil de Mike** : *« ce resto a monté en gamme ET l'énergie est fidèle au lieu — je le vends 490 € sans rougir »*. Les deux conditions, pas une seule. Sinon : itérer sur le brief Stitch (plafond), jamais sur le plancher.

---

## Note de cohérence (dette à traiter)

Ce pivot rend obsolètes des passages encore écrits « 3 signatures » dans `CLAUDE.md`, `differenciation-clients.md` (couches 1-3), et les skills `brief-client` / `site-from-brief` / `audit-livraison`. La décision est loguée dans `differenciation-clients.md` (section « Pivot 2026-05-19 »). La mise en cohérence complète de ces fichiers est un chantier à part, **à ne pas faire silencieusement** : à cadrer explicitement avec Mike avant.
