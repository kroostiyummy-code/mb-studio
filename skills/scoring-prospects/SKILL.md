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
- **`autre-site`** : URL existe, pas eatbu
- **`pas-de-site`** : aucune URL

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

### Étape 6 — Calcul du score

Appliquer **strictement** `references/scoring-formula.md` :
- Sous-score Valeur apportée (0-100), formule selon bucket
- Sous-score Probabilité d'acceptation (0-100), additif
- `score_total = 0.5·valeur + 0.5·proba`, arrondi entier
- Tier : A ≥ 75, B 50-74, C < 50
- Mode dégradé : redistribution des poids Lighthouse documentée dans scoring-formula.md
- Données manquantes : valeurs par défaut du tableau dédié

Ne PAS recopier la formule en dur ici — toujours lire `scoring-formula.md` (source unique de vérité, modifiable sans toucher au SKILL).

### Étape 7 — Sync liste vivante + génération des vues

**Source de vérité unique : `prospects/restaurants.yml`** (cf `prospects/README.md`). Ne JAMAIS l'écraser.

Pour chaque resto scanné :
- `id` = slug stable du resto (jamais renommé/réutilisé). Créer l'entrée si absente.
- Mettre à jour **uniquement** les blocs `scan` et `scoring`.
- **Ne jamais toucher** `tunnel` ni `notes_mike` (écrits par `pilote-client` / Mike).
- **Ne jamais écraser** un `scoring.mike_override` existant : s'il est là, il prime ; recalculer le score à côté sans effacer l'override.

Puis **régénérer les vues** (toutes dérivées du YAML, jamais éditées à la main) :

1. `prospects/restaurants.csv` — vue plate vivante, 1 ligne/resto, colonnes du fichier existant, prête infographie / Google Sheets.
2. `prospects/{ville}-{YYYY-MM-DD}/` (snapshot daté de la campagne) :
   - `prospects-avec-site-eatbu.md` — fiches bucket eatbu, triées score décroissant
   - `prospects-avec-site-autre.md` — fiches bucket autre-site, triées score décroissant
   - `prospects-sans-site.md` — fiches bucket pas-de-site, triées score décroissant
   - `prospects-exclus.md` — exclus + raison (chaîne nationale / site custom moderne)
   - `tableau-recap.csv` — export brut riche de la campagne (colonnes = en-tête de `templates/tableau-recap.csv`)

Chaque fiche suit `templates/fiche-prospect.md`. Le "Top 3 arguments" est généré en piochant dans `references/argument-library.md` selon la **pire métrique mesurée** sur CE resto (1er argument = point le plus douloureux et le plus prouvable). Drapeau rouge ajouté selon les règles de l'argument-library.

En fin de run, afficher à Mike un récap :
```
✅ Scoring terminé — {ville}, rayon {km} km
   {N} restos analysés, {X} exclus
   eatbu : {a} fiches (top : {nom} — {score}/100)
   autre-site : {b} fiches
   pas-de-site : {c} fiches
   {mode normal | ⚠️ MODE DÉGRADÉ — clé PageSpeed absente}
📁 prospects/{ville}-{date}/
🎯 Top 3 cibles toutes listes : {3 noms + scores}
👉 Prochaine action : lance `maquette-flash` sur ta cible n°1 avant d'aller la voir.
```

---

## 🛑 GATE D'ALERTE DÉVIATION (méta-règle — prioritaire sur tout le reste)

Dès que l'exécution s'écarte de la méthode documentée de ce skill — override d'un score, exclusion/inclusion d'un prospect hors des règles d'exclusion, choix d'une cible **au jugement** au lieu du tri/tier produit par la formule, saut d'une étape du pipeline — le skill **DOIT** :

1. **S'arrêter immédiatement.**
2. **Expliquer la déviation en une phrase** (« je m'écarte de la méthode parce que X »).
3. **Exiger un "OK Mike" explicite** avant de continuer.

**Interdiction absolue tant que le "OK Mike" n'est pas donné :** aucun commit de carnet, aucune création/modification de fichier `pilote/`, aucune avancée du tunnel, aucune décision stratégique posée en fait accompli (choix de cible, archivage, passage d'étape).

Une cible peut être excellente et le procédé fautif quand même : la justesse de la décision ne dispense JAMAIS de demander l'accord avant de la rendre effective. Le fait accompli sur une décision stratégique est la faute, pas l'erreur de jugement.

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
- Score 0-100, tiers A (≥75) / B (50-74) / C (<50)
- Exclusions auto : chaînes nationales + sites custom modernes (Lighthouse ≥85 et pas eatbu)
- 3 listes (eatbu / autre-site / pas-de-site), pas 2
- Pondération : 50 % valeur + 50 % probabilité
- Clé PageSpeed obligatoire en mode normal, mode dégradé documenté et accepté comme fallback
- (2026-05-16) Source de vérité = liste vivante `prospects/restaurants.yml`, vues régénérées ; `prospects/` versionné dans le repo privé (sauf cache) ; Google Places API officielle ajoutée comme source d'enrichissement optionnelle

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
