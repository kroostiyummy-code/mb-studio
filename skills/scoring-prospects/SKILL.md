---
name: scoring-prospects
description: "Génère 3 listes triées de prospects restaurants chartrains à démarcher en porte-à-porte (avec site eatbu / avec site autre / sans site), chacune scorée 0-100 avec tier A/B/C combinant 'valeur qu'on peut apporter' et 'probabilité que le patron accepte'. Source de vérité : prospects/restaurants.yml (liste vivante enrichie run après run). Sources de données : Overpass OpenStreetMap + Google PageSpeed API + Wayback Machine + Google Places API (officielle). Output : prospects/restaurants.yml mis à jour + vues régénérées (CSV plat + fiches markdown datées avec top 3 arguments factuels). Tourne UNE fois pour démarrer, puis ponctuellement (tous les 3-6 mois). MANDATORY TRIGGERS: 'score les prospects', 'scoring prospects', 'génère la liste des prospects', 'qui je démarche en premier', 'prospects chartres'. STRONG TRIGGERS (avec contexte): 'fais-moi la liste des restos à visiter', 'j'ai besoin de prioriser mes visites', 'qui pitcher en premier à Chartres'. Ne pas déclencher pour : audit d'un site spécifique (c'est audit-eatbu), préparation d'une visite déjà décidée (c'est maquette-flash)."
---

# Scoring Prospects

Skill MB Studio **priorité 1** : produit la liste triée des restos chartrains à démarcher, AVANT la première visite terrain. Sans lui, Mike choisit au feeling et risque un taux de conversion 1/5 démoralisant sur ses premières visites. Avec lui, il attaque les cibles faciles en premier (effet boule de neige : 3 signatures sur 5 = témoignages + photos Insta + confiance).

L'output : 3 fiches markdown triées + 1 CSV récap. Chaque fiche porte un score, 2 sous-scores, et les **3 arguments les plus forts à pitcher** basés sur des métriques objectives mesurées sur LE site du patron.

---

## Quand déclencher ce skill

**Bons cas :** "score les prospects", "qui je démarche en premier", "fais-moi la liste des restos à visiter à Chartres".

**Mauvais cas (ne pas déclencher) :**
- Audit d'un site précis → `audit-eatbu`
- Préparer une visite déjà décidée → `maquette-flash`

---

## Inputs requis au démarrage

Demander à Mike, en une passe :

> "OK on lance le scoring. Donne-moi :
> 1. La ville (défaut : Chartres) + rayon en km (défaut : 5 km autour du centre).
> 2. Une clé API Google PageSpeed (procédure 1-fois ci-dessous si tu n'en as pas). Sans elle, je tourne en mode dégradé (score moins précis, pas de mesure de vitesse).
> 3. Une clé API Google Places, optionnelle (procédure 1-fois ci-dessous). Sans elle, pas d'enrichissement GMB auto : je te demande quelques URLs à la main.
> 4. Tu as déjà fait tourner ce skill ? Si oui je réutilise le cache et j'enrichis la liste existante."

Si Mike dit "pas de clé, tant pis" → continuer en **mode dégradé** (voir `references/scoring-formula.md` section dédiée) en l'annonçant clairement.

### Procédure 1-fois pour la clé Google PageSpeed

À afficher à Mike s'il n'a pas de clé :

```
1. https://console.cloud.google.com/
2. Créer un projet "MB Studio Scoring"
3. Activer l'API "PageSpeed Insights API"
4. Identifiants → Créer → Clé API
5. Restreindre la clé à l'API PageSpeed Insights (sécurité)
6. La stocker dans ~/.mb-studio/secrets.env :
   GOOGLE_PAGESPEED_API_KEY=AIza...
Gratuit jusqu'à 25 000 req/jour (on en utilise ~450 max).
```

Lire la clé via : `grep GOOGLE_PAGESPEED_API_KEY ~/.mb-studio/secrets.env` (Bash) ou équivalent. Ne JAMAIS écrire la clé dans le repo, les fiches, ou un commit.

### Procédure 1-fois pour la clé Google Places (optionnelle)

À afficher à Mike s'il veut l'enrichissement GMB automatique :

```
1. Même projet Google Cloud que PageSpeed
2. Activer l'API "Places API (New)"
3. Identifiants → Créer → Clé API → restreindre à Places API
4. La stocker dans ~/.mb-studio/secrets.env :
   GOOGLE_PLACES_API_KEY=AIza...
```

⚠️ **Places API est facturée à l'usage** (un crédit mensuel offert existe mais évolue — **vérifier le tarif courant chez Google avant tout run en masse**, honnêteté radicale). Pour maîtriser le coût : Places n'est appelé QUE pour les restos où une donnée clé manque (URL, note, nb avis), en lot, et **mis en cache 30 j**. C'est l'API **officielle** Google (≠ scraping Maps interdit par le garde-fou #4) : autorisée.

---

## Outils à utiliser (adaptation au réel)

- **Appels API JSON** (Overpass, Nominatim, PageSpeed, Wayback CDX) : utiliser **Bash `curl`** (ou PowerShell `Invoke-RestMethod`), PAS WebFetch — WebFetch résume/altère le JSON brut, on a besoin du JSON exact pour parser.
- **Cache** : fichiers JSON sous `prospects/cache/`. Vérifier le TTL avant chaque appel réseau (si cache frais, ne pas re-appeler).
- **Écriture** : source de vérité `prospects/restaurants.yml` (upsert), puis vues régénérées (`prospects/restaurants.csv` + snapshot daté `prospects/{ville}-{YYYY-MM-DD}/`).
- `prospects/` est **versionné** dans le repo MB Studio (privé) sauf `prospects/cache/` (gitignoré). Confidentialité = ne jamais publier HORS de ce repo. Commit **fichier par fichier**, **jamais `git add prospects/`** en bloc (garde-fou #7, cf `prospects/README.md`).

---

## Pipeline en 7 étapes

### Étape 1 — Récupération des restos via Overpass (OSM)

Centre Chartres : `48.4439, 1.4892`. Rayon défaut 5000 m.

```bash
curl -s -G "https://overpass-api.de/api/interpreter" \
  -H "User-Agent: MB-Studio-Scoring/1.0 (contact: kroostiyummy@gmail.com)" \
  --data-urlencode 'data=[out:json][timeout:25];(node["amenity"~"restaurant|cafe|fast_food|bar|pub"]["name"](around:5000,48.4439,1.4892);way["amenity"~"restaurant|cafe|fast_food|bar|pub"]["name"](around:5000,48.4439,1.4892););out center tags;' \
  -o prospects/cache/overpass-chartres-5000.json
```

**⚠️ Adaptation réelle vérifiée le 2026-05-15 :** le header `User-Agent` identifiable est **OBLIGATOIRE** sur `overpass-api.de` — sans lui, réponse `406 Not Acceptable` (HTML, pas du JSON). Toujours inclure `-H "User-Agent: MB-Studio-Scoring/1.0 (contact: kroostiyummy@gmail.com)"`. Idem pour Nominatim (étape 2) et recommandé pour Wayback. Dry-run validé : 104 POI sur Chartres centre 1,5 km, montée cohérente attendue à ~150 sur 5 km.

Pour chaque POI : `name`, `addr:street`, `addr:housenumber`, `addr:postcode`, `addr:city`, `cuisine`, `website`, `phone`, `opening_hours`, lat/lon (champ `center` pour les `way`).

Volume attendu Chartres 5 km : 80-150 POI. ~70-80 % des restos réels (limite OSM connue, acceptable).

**Cache** : `prospects/cache/overpass-{ville}-{rayon}.json`, TTL 30 jours (ne pas re-fetch si fichier < 30 j).

### Étape 2 — Détection du site (classification en 3 buckets)

Pour chaque resto :
1. Si tag OSM `website` présent → URL connue.
2. Sinon → requête Nominatim (gratuit) sur le nom + ville pour récupérer plus de tags :
   `curl -s "https://nominatim.openstreetmap.org/search?q={nom}+{ville}&format=json&extratags=1&limit=1" -H "User-Agent: MB-Studio-Scoring/1.0"`
   (Nominatim exige un User-Agent identifiable, sinon 403.)
3. Sinon, **si `GOOGLE_PLACES_API_KEY` présente** → Places API officielle (Text Search puis Place Details) pour récupérer `website`, `formatted_phone_number`, `rating`, `user_ratings_total`, `opening_hours`, nombre de photos, présence description/catégories. Ces signaux GMB alimentent aussi le sous-score « probabilité » (étape 6). Appels **plafonnés** aux restos sans donnée + **cache** `prospects/cache/places/{slug}.json`, TTL 30 j.
4. Sinon (pas de clé Places, rien trouvé) → marquer "site inconnu". Lister ces restos et **demander à Mike** en un seul batch les URLs qu'il connaît (cap à 20 max à vérifier manuellement — au-delà, laisser en `pas-de-site`).

Buckets :
- **`eatbu`** : URL contient `eatbu.com`
- **`autre-site`** : URL existe, pas eatbu **et pas une plateforme agrégateur**
- **`pas-de-site`** : aucune URL **OU** URL pointant uniquement vers une plateforme agrégateur/livraison/linktree

> **Règle agrégateurs (décision Mike 2026-05-17).** Un lien vers UberEats, Deliveroo, Just Eat, TheFork/LaFourchette, Privateaser, linktr.ee, bento.me, beacons.ai, allmylinks, une page Facebook/Instagram… **n'est PAS un site à soi** : le patron ne possède rien, ne maîtrise rien. Ces restos vont en **`pas-de-site`** (valeur 90, cible prime), jamais en `autre-site`. Effet de bord bénéfique : corrige aussi les faux matchs Nominatim (une même URL agrégateur partagée à tort entre plusieurs restos). Liste de domaines maintenue dans le script (`AGGREGATEURS`).

### Étape 3 — Lighthouse via PageSpeed API (batch parallèle)

Pour chaque resto des buckets `eatbu` + `autre-site` :

```bash
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={URL}&strategy=mobile&category=PERFORMANCE&category=ACCESSIBILITY&category=SEO&category=BEST_PRACTICES&key={KEY}"
```

Extraire : 4 scores (Performance / Accessibilité / SEO / Bonnes pratiques, ×100), LCP, CLS, INP/FID, FCP, poids total transféré (`lighthouseResult.audits['total-byte-weight']`).

**Parallélisation : 4 requêtes max en parallèle** (politesse + anti rate-limit). En pratique : traiter par lots de 4, attendre, lot suivant.

**Cache** : `prospects/cache/lighthouse/{slug}.json`, TTL 30 j.

**Mode dégradé** (pas de clé) : skip cette étape entièrement, scores Lighthouse = `null`, formule recalculée (cf `references/scoring-formula.md`).

### Étape 4 — Ancienneté du site (Wayback CDX)

Pour chaque site trouvé :

```bash
curl -s "https://web.archive.org/cdx/search/cdx?url={URL}&output=json&limit=1&from=2010"
```

Première capture → `âge_site` en années. Si Wayback vide → `âge_site = null` → la formule utilise le défaut médian 2 ans (cf scoring-formula.md, tableau "Données manquantes").

**Cache** : `prospects/cache/wayback/{slug}.json`, TTL 90 j.

### Étape 5 — Filtres d'exclusion (AVANT scoring)

Exclure et router vers `prospects-exclus.md` (avec la raison) :

1. **Chaînes nationales** : nom matche `references/chaines-nationales.md` (règles de matching dans ce fichier : insensible casse, match nom de marque comme segment, ne pas sur-matcher, en cas de doute NE PAS exclure).
2. **Sites custom modernes** : `bucket == autre-site` ET `lighthouse_perf ≥ 85` ET `lighthouse_seo ≥ 85` (le patron a déjà investi, aucune valeur à apporter).

Transparent : Mike peut overrider une exclusion via `mike_override` dans le CSV (conservé entre runs).

### Étape 6 — Calcul du score (architecture normalisée, refonte 2026-05-18)

Appliquer **strictement** `references/scoring-formula.md` (Rapport_classement,
décision Mike 2026-05-18). Ne PAS recopier la formule ici — `scoring-formula.md`
est la source unique de vérité.

Principe : chaque composante normalisée dans **[0,1]** ; donnée **inconnue →
0,50** (jamais 0) et **non observée** (baisse la Confidence).

- **Valeur apportable /100** = `25·presence_gap + 20·performance_gap +
  20·conversion_gap + 15·seo_gap + 10·local_profile_gap +
  10·reputation_misalignment`
- **Probabilité /100** = `35·business_proof + 20·switchability +
  15·contactability + 15·timing + 10·independence_class + 5·complexity_class`
- **`score_final = 0,55·V + 0,45·P`** (ou `mike_override` s'il existe, qui prime)
- **Confidence** = `100 · Σ poids observés / 200` (poids = coeffs V+P)
- **Tiers** : A (`final≥75 ET conf≥60`) · B (`65≤final<75`) · C
  (`55≤final<65`) · D (`final<55`)
- **Étape 5bis — DOM fetch léger** (homepage + `/robots.txt` + `/sitemap.xml`)
  pour `conversion_gap` + `seo_checks` + email/social, **caché 30 j**
  (`prospects/cache/dom/`), buckets eatbu/autre-site seulement, échec → 0,50 +
  Confidence baissée.
- **Bandes d'action par rang** (tri global `final ↓ puis confidence ↓`) :
  top ~10 = `Priorité semaine` · ~15 suivants = `Priorité mois` · reste =
  `Réserve` · `confidence < 50` → `À surveiller`.

> **TODO planifié (PAS fait dans le run 2026-05-18)** : re-enrichissement
> Places **ciblé** `photos_count` + `hours` sur les ~148 restos de la liste
> vivante (≈148 Place Details, dans le cap gratuit mensuel + plafond dur
> 500/j ≈ 0 $). Refresh ciblé sur liste existante = **autorisé** (≠ découverte
> massive). Objectif : fiabiliser `local_profile_gap` (aujourd'hui marqué
> **non-observé**, honnête, car ces signaux n'étaient pas persistés au cache).
> Ne pas perdre ce TODO.

### Étape 7 — Sync liste vivante + génération des vues

**Source de vérité unique : `prospects/restaurants.yml`** (cf `prospects/README.md`). Ne JAMAIS l'écraser.

Pour chaque resto scanné :
- `id` = slug stable du resto (jamais renommé/réutilisé). Créer l'entrée si absente.
- Mettre à jour **uniquement** les blocs `scan` et `scoring`.
- **Ne jamais toucher** `tunnel` ni `notes_mike` (écrits par `pilote-client` / Mike).
- **Ne jamais écraser** un `scoring.mike_override` existant : s'il est là, il prime ; recalculer le score à côté sans effacer l'override.

Puis **régénérer les vues** (toutes dérivées du YAML, jamais éditées à la main) :

1. `prospects/restaurants.csv` — vue plate vivante, 1 ligne/resto, colonnes du fichier existant, prête infographie / Google Sheets.
2. `prospects/{ville}-{YYYY-MM-DD}/` (snapshot daté de la campagne) — **3 listes SÉPARÉES, jamais de classement global mélangé** (décision Mike 2026-05-17) :
   - `liste-eatbu.md` + `liste-eatbu.txt` — bucket eatbu
   - `liste-autre-site.md` + `.txt` — bucket autre-site
   - `liste-sans-site.md` + `.txt` — bucket pas-de-site
   - `prospects-exclus.md` — exclus + raison (chaîne nationale / site custom moderne)
   - `tableau-recap.csv` — export brut riche de la campagne (colonnes = en-tête de `templates/tableau-recap.csv`)

   Chaque liste : un `.md` **et** un `.txt` lisible sans outil technique (ou `.docx` si pandoc dispo). Chaque liste s'ouvre par un bloc **« 📋 Critères de cette liste »** (définition de la catégorie + angle stratégique + **tri annoncé explicitement**) puis les fiches. **Tri propre à chaque liste :**
   - `liste-eatbu` / `liste-autre-site` : du site **le plus mauvais au moins mauvais** (sous-score « ce qu'on peut lui apporter » décroissant).
   - `liste-sans-site` : par **nombre d'avis Google décroissant** (popularité = resto établi + capacité à payer).

Le format exact de l'en-tête et des fiches est gravé dans `templates/fiche-prospect.md` (libellés français). Le "Top 3 arguments" est piochée dans `references/argument-library.md` selon la **pire métrique mesurée** sur CE resto (1er argument = point le plus douloureux et le plus prouvable). Drapeau rouge ajouté selon les règles de l'argument-library.

En fin de run, afficher à Mike un récap (**une tête par liste selon son propre tri, JAMAIS de top global mélangé**) :
```
✅ Scoring terminé — {ville}, rayon {km} km
   {N} restos analysés, {X} exclus
   eatbu : {a} · autre-site : {b} · pas-de-site : {c}
   tiers : A={..} B={..} C={..}
   {mode normal | ⚠️ MODE DÉGRADÉ — clé PageSpeed absente}
📁 prospects/{ville}-{date}/  (3 listes séparées .md + .txt)
🎯 Tête de chaque liste (selon le tri de la liste) :
   [eatbu] {nom} — valeur {v}/100, proba {p}/100, Tier {t}
   [autre-site] {nom} — …
   [sans-site] {nom} — …
👉 Prochaine action : choisis ta cible à la stratégie (pas au tier brut), puis lance `maquette-flash` dessus avant d'aller la voir.
```

---

## 🛑 GATE D'ALERTE DÉVIATION (méta-règle — prioritaire sur tout le reste)

**Tant que l'exécution suit la méthode documentée** (pipeline 7 étapes, formule de `scoring-formula.md`, règles d'exclusion, tri/tier produit) : **avancer en autonomie, sans demander de validation.** Ne pas solliciter Mike pour ce qui est conforme.

**Dès qu'on s'écarte** — override d'un score, exclusion/inclusion hors règles, choix d'une cible **au jugement** au lieu du tri/tier, saut d'étape, emplacement de sortie différent de la spec — l'**interdit n'est pas d'avancer, c'est de dévier en silence**. Le skill DOIT **informer Mike clairement** : la déviation, sa raison, sa conséquence. Pour un écart structurant (choix de cible, décision stratégique), informer **avant** d'acter pour qu'il puisse réagir ; pour un écart mineur/réversible, informer dans la foulée.

Jamais de fait accompli **silencieux**. Une décision peut être juste ET devoir être signalée : la transparence sur l'écart est non négociable, la demande de permission systématique sur le conforme ne l'est pas.

---

## Garde-fous critiques (NON négociables)

1. **Aucun email/téléphone scrappé pour du cold outreach automatisé.** Les fiches servent à des visites en personne. Pas de spam, pas d'envoi auto.
2. **Pas de comparaison nominative entre prospects** dans les listes. Chaque fiche est autonome (le n°3 ne mentionne jamais le n°1).
3. **Le skill ne juge pas la valeur humaine d'un patron.** Score bas = "pas le bon timing/la bonne cible aujourd'hui", jamais "mauvais resto".
4. **Sources autorisées** : OSM, Wayback, PageSpeed API, **Places API officielle Google**. **Interdit : scraping de Google Maps / scraping GMB en masse (ToS).** L'API Places sanctionnée ≠ scraping : OK, mais plafonnée et mise en cache pour le coût.
5. **Override Mike persistant** : champ `mike_override` du CSV conservé entre runs. Mike a toujours le dernier mot.
6. **Le score n'est pas un oracle.** Outil d'aide à la priorisation. Le dire dans le récap.
7. **Confidentialité** : ne JAMAIS publier ces données hors du repo MB Studio (privé). `prospects/` est **versionné** dans ce repo privé (sauf `prospects/cache/`) : commit **fichier par fichier**, **jamais `git add prospects/`** en bloc. Ne jamais coller le contenu d'une fiche dans un canal externe.

---

## Décisions Mike validées (NE PAS reposer ces questions)

- Source : Overpass OSM auto + complément GMB manuel ciblé
- ~~Score 0-100, tiers A (≥75)/B/C~~ → **remplacé** par archi normalisée + tiers A/B/C/D (2026-05-18, voir plus bas)
- Exclusions auto : chaînes nationales + sites custom modernes (Lighthouse ≥85 et pas eatbu)
- 3 listes (eatbu / autre-site / pas-de-site) **+ classement global** (2026-05-18)
- ~~Pondération 50/50~~ → **remplacé** par `0,55·V + 0,45·P` (2026-05-18)
- Clé PageSpeed obligatoire en mode normal, mode dégradé documenté et accepté comme fallback
- (2026-05-16) Source de vérité = liste vivante `prospects/restaurants.yml`, vues régénérées ; `prospects/` versionné dans le repo privé (sauf cache) ; Google Places API officielle ajoutée comme source d'enrichissement optionnelle
- (2026-05-17) Lien agrégateur/livraison/linktree (UberEats, Deliveroo, Just Eat, TheFork, Privateaser, linktr.ee, bento.me, Facebook/Instagram…) = **`pas-de-site`**, jamais `autre-site` (le patron ne possède rien) — cf règle agrégateurs étape 2. Bruit OSM non-commercial (cantines scolaires, administrations) géré via `prospects/opt-out.txt` (pas de règle d'exclusion dans la spec : opt-out ponctuel suffit)
- (2026-05-17) **Format des sorties** : 3 listes SÉPARÉES (`liste-eatbu` / `liste-autre-site` / `liste-sans-site`), `.md` + `.txt` lisible, bloc « 📋 Critères de cette liste » en tête, fiches à libellés français. Format gravé dans `templates/fiche-prospect.md`. _(Le « jamais de classement global » de cette décision est **levé** par 2026-05-18 ci-dessous.)_
- **(2026-05-18) Refonte scoring — architecture normalisée (Rapport_classement).** Remplace les barèmes antérieurs. Composantes normalisées [0,1] (`presence_gap`, `performance_gap`, `conversion_gap`, `seo_gap`, `local_profile_gap`, `business_proof`, `switchability`, `contactability`, `timing`, `independence/complexity_class`, `reputation_misalignment`), `V` et `P` pondérés, **`score_final = 0,55·V + 0,45·P`**, **Confidence Score** (poids observés/200 ; inconnu = 0,50 jamais 0), **tiers A/B/C/D**, **classement global unique** trié `final ↓ puis confidence ↓` + filtres eatbu/autre/sans + quick-wins (= bande Priorité semaine). `source_list` = filtre/pitch only. DOM fetch léger caché pour conversion/seo.
- (2026-05-18) **Téléphone OSM gardé** dans `contactability` (vrai signal de joignabilité ; un `phone_known=1` remonte légitimement la proba — assumé).
- (2026-05-18) **eatbu = vue stratégique, formule NON distordue.** Un eatbu a un déficit brut < un sans-site → score objectif plus bas, c'est normal et assumé. On ne truque pas le score : on compense par le bloc « Critères » de `liste-eatbu` qui la cadre en cœur de cible / liste de travail 1er rang (pitch le plus fort + transformation la plus visible). À travailler EN PARALLÈLE du classement global.
- (2026-05-18) **`independence_class`/`complexity_class`** : valent 1,0 si le resto a un site à inspecter, sinon **non-observés → 0,50** (`pas-de-site`). Seule lecture qui fait tomber les 3 cas-test d'acceptation pile.
- (2026-05-18) **TODO planifié, PAS fait dans ce run** : re-enrich Places ciblé `photos_count`/`hours` sur la liste vivante (~148 Place Details, ≈0 $, refresh ciblé ≠ découverte massive = autorisé) pour fiabiliser `local_profile_gap` (aujourd'hui non-observé, honnête).

---

## Hors-scope (NE PAS implémenter)

- Cold emailing / cold calling automatisé
- Détection du patron sur LinkedIn
- Score d'évolution dans le temps (un seul snapshot suffit pour démarrer)
- Intégration CRM (le CSV suffit pour les 20 premiers clients)
- Géocodage avancé / clustering de tournées (Mike connaît Chartres par cœur)
- Scoring "déjà client d'une autre agence" (indétectable de façon fiable)

---

## Resources

- `references/chaines-nationales.md` — liste statique des chaînes à exclure + règles de matching
- `references/scoring-formula.md` — formule de score détaillée (source unique de vérité, mode dégradé inclus)
- `references/argument-library.md` — bibliothèque de phrases d'arguments + drapeaux rouges
- `templates/fiche-prospect.md` — squelette de fiche
- `templates/tableau-recap.csv` — en-tête du CSV récap riche (snapshot campagne)
- `prospects/README.md` + `prospects/restaurants.yml` — contrat de la liste vivante (source de vérité, ce qu'on n'écrase jamais)

---

## Exemple d'invocation

```
Mike : Score les prospects. Chartres, 5 km. J'ai mis ma clé PageSpeed dans secrets.env.
```

Le skill : récupère ~110 restos via Overpass → classe en 3 buckets (Places API pour les URLs manquantes) → lance Lighthouse sur les ~70 avec site (lots de 4) → âge via Wayback → exclut 12 chaînes + 4 sites modernes → score les ~95 restants → **upsert dans `prospects/restaurants.yml`** (sans toucher `tunnel`/`notes_mike`/`mike_override`) → régénère `prospects/restaurants.csv` + le snapshot `prospects/chartres-2026-05-15/` (4 .md + recap CSV) → affiche le top 3 toutes listes + invite à lancer `maquette-flash` sur la cible n°1.
