# Spec — Skill `scoring-prospects`

> Document de spécification destiné au Claude qui codera ce skill (en local terminal). Spec co-écrite avec Mike en session cloud le 2026-05-15. **Priorité 1 dans la roadmap** — à coder AVANT `audit-livraison` car débloque les 5 premières visites terrain.

---

## Pourquoi ce skill existe

Mike va démarcher en porte-à-porte les restos chartrains. Aujourd'hui, sans ce skill, il choisit au feeling. Conséquence probable : taux de conversion 1/5 sur ses premières visites, perte de moral, mauvais départ.

Avec `scoring-prospects`, il arrive à la porte du restaurant déjà armé de :
- Un **score d'opportunité 0-100** qui combine "valeur qu'on peut apporter" et "probabilité que le patron accepte"
- Les **3 arguments les plus forts** à pitcher (basés sur des métriques objectives sur LE site du patron, pas génériques)
- Une **liste triée** pour visiter les cibles faciles en premier (effet boule de neige : 3 signatures sur les 5 premières visites = témoignages, photos Insta, confiance)

Le skill tourne **une fois** pour générer les listes, puis ponctuellement quand Mike veut rafraîchir (tous les 3-6 mois).

---

## Triggers

**MANDATORY TRIGGERS :**
- "score les prospects"
- "scoring prospects"
- "génère la liste des prospects"
- "qui je démarche en premier"
- "prospects chartres"

**STRONG TRIGGERS (avec contexte) :**
- "fais-moi la liste des restos à visiter"
- "j'ai besoin de prioriser mes visites"
- "qui pitcher en premier à Chartres"

**Ne pas déclencher pour :**
- Audit d'un site spécifique (c'est `audit-eatbu`)
- Préparation d'une visite déjà décidée (c'est `maquette-flash`)

---

## Inputs requis au démarrage

Le skill demande à Mike, en une passe :

> "OK on lance le scoring. Donne-moi :
> 1. La ville (par défaut : Chartres). Tu peux mettre un rayon en km (par défaut : 5 km autour du centre).
> 2. Une clé API Google PageSpeed (procédure 1-fois plus bas si tu n'en as pas). Si absente, je tourne en mode dégradé (sans Lighthouse, score moins précis).
> 3. As-tu déjà fait tourner ce skill ? Si oui, je ré-utilise le cache."

Si la clé PageSpeed manque et que Mike dit "tant pis", continuer en mode dégradé en l'expliquant.

### Procédure 1-fois pour la clé Google PageSpeed (à documenter dans le skill)

1. Aller sur https://console.cloud.google.com/
2. Créer un projet "MB Studio Scoring"
3. Activer l'API "PageSpeed Insights API"
4. Créer une clé API (Identifiants → Créer → Clé API)
5. Restreindre la clé à l'API PageSpeed Insights (sécurité)
6. Stocker la clé dans `~/.mb-studio/secrets.env` sous `GOOGLE_PAGESPEED_API_KEY=...`

Gratuit jusqu'à 25 000 requêtes/jour. Largement assez pour 150 restos × 3 pages = 450 requêtes.

---

## Pipeline du skill (7 étapes)

### Étape 1 — Récupération des restos via Overpass API (OpenStreetMap)

Requête Overpass type :

```overpass
[out:json][timeout:25];
(
  node["amenity"~"restaurant|cafe|fast_food|bar|pub"]["name"](around:{rayon_m},{lat},{lon});
  way["amenity"~"restaurant|cafe|fast_food|bar|pub"]["name"](around:{rayon_m},{lat},{lon});
);
out center tags;
```

Centre de Chartres : `48.4439, 1.4892`. Rayon par défaut 5000 m.

Pour chaque POI récupéré, extraire :
- `name`
- `addr:street`, `addr:housenumber`, `addr:postcode`, `addr:city`
- `cuisine` (italien, français, asiatique, etc.)
- `website` si présent (souvent absent dans OSM)
- `phone` si présent
- `opening_hours` si présent
- Coordonnées lat/lon

**Volume attendu pour Chartres dans un rayon de 5 km : 80-150 POI.**

**Limite OSM connue :** ~70-80% des restos réels sont dans OSM. Certains petits restos manquent. C'est acceptable, on n'a pas besoin d'exhaustivité pour démarrer.

Cache : sauvegarder dans `prospects/cache/overpass-{ville}-{rayon}.json` avec un TTL de 30 jours.

### Étape 2 — Enrichissement web (détection du site)

Pour chaque resto, déterminer s'il a un site web et lequel :

1. **Si `website` est dans les tags OSM** → on a déjà l'URL
2. **Sinon, chercher sur Nominatim** (API OSM, gratuit) avec le nom du resto pour récupérer plus de tags
3. **Sinon, chercher la fiche GMB** : utiliser l'**Overpass Places API** d'OSM ou un proxy ; si pas dispo, marquer "site inconnu" et **demander à Mike** une URL en mode interactif batch (mais limiter à max 20 restos à vérifier à la main)

**Classification en 3 buckets** :
- **`eatbu`** : URL contient `eatbu.com`
- **`autre-site`** : URL existe et n'est pas eatbu
- **`pas-de-site`** : pas d'URL trouvée

### Étape 3 — Lighthouse sur les sites trouvés (mode batch parallèle)

Pour chaque resto avec un site (buckets `eatbu` et `autre-site`), lancer PageSpeed Insights API :

```
GET https://www.googleapis.com/pagespeedonline/v5/runPagespeed
  ?url={site_url}
  &strategy=mobile
  &category=PERFORMANCE
  &category=ACCESSIBILITY
  &category=SEO
  &category=BEST_PRACTICES
  &key={GOOGLE_PAGESPEED_API_KEY}
```

Récupérer pour chaque site :
- Performance, Accessibilité, SEO, Bonnes pratiques (4 scores 0-100)
- LCP, CLS, INP/FID, FCP (Core Web Vitals)
- Poids total transféré

**Parallélisation** : 4 requêtes en parallèle max (politesse + éviter rate-limiting).

**Cache** : `prospects/cache/lighthouse/{slug}.json`, TTL 30 jours.

**Mode dégradé (sans clé API)** : skip cette étape, marquer les scores Lighthouse à `null`, ajuster la formule (voir étape 6).

### Étape 4 — Ancienneté du site (Wayback Machine)

Pour les sites trouvés, interroger l'API CDX de Wayback :

```
GET https://web.archive.org/cdx/search/cdx?url={url}&output=json&limit=1&from=2010
```

Récupérer la **date de la première capture**. Convertir en "âge en années".

Pour les sites où Wayback ne retourne rien :
- **Fallback** : chercher la date du **premier avis Google** sur la fiche GMB. Comme c'est fragile à scraper sans API officielle, fallback à `âge = null` (proxy : "âge inconnu, considéré médian = 2 ans").

**Cache** : `prospects/cache/wayback/{slug}.json`, TTL 90 jours (Wayback bouge lentement).

### Étape 5 — Filtres d'exclusion (avant scoring)

Avant de scorer, exclure les restos qui matchent :

1. **Chaînes nationales** : nom dans la liste statique `skills/scoring-prospects/references/chaines-nationales.md` (Mc Donald's, Subway, KFC, Buffalo Grill, La Mie Câline, Burger King, Five Guys, Pizza Hut, Domino's, Sushi Shop, Brioche Dorée, Paul, Class'Croute, Pomme de Pain, Quick, Léon de Bruxelles, Hippopotamus, Courtepaille, Flunch, Crocodile, Léon, Memphis Coffee, O'Tacos, Tacos Avenue, etc. — liste à compléter à la main).

2. **Sites custom modernes** : `bucket=autre-site` ET Lighthouse perf mobile ≥ 85 ET SEO ≥ 85. Le patron a déjà investi, pas de valeur à apporter.

Les restos exclus sortent dans un 4e fichier `prospects-exclus.md` avec la **raison** (transparent : Mike peut overrider si besoin).

### Étape 6 — Calcul du score

Pour chaque resto restant, calculer **2 sous-scores** + **1 score combiné**.

#### Sous-score "Valeur apportée" (0-100)

Mesure : "à quel point le site/présence numérique du resto est en-dessous de ce que MB Studio peut livrer".

Pondération pour bucket `eatbu` :
- `100 - lighthouse_perf` × 0.30 → site lent = grosse valeur à apporter
- `100 - lighthouse_seo` × 0.25 → mauvais SEO = grosse valeur
- `100 - lighthouse_a11y` × 0.10 → mauvaise accessibilité = valeur modérée
- `min(âge_site × 10, 50)` × 0.15 → site vieux = valeur de modernisation
- `100 - score_GMB_completude` × 0.20 → fiche GMB pauvre = valeur globale

Pondération pour bucket `autre-site` : identique mais avec une **pénalité de 15 points** (le patron a déjà payé un site, plus dur à remplacer).

Pondération pour bucket `pas-de-site` : score fixe **valeur = 90** (énorme valeur à apporter par définition).

#### Sous-score "Probabilité d'acceptation" (0-100)

Mesure : signaux faibles de "patron ouvert au numérique et capable de payer 490€".

- **Note Google ≥ 4.0** : +25 pts ; entre 3.5 et 4.0 : +10 ; <3.5 : 0
- **Nombre d'avis Google** : ≥100 : +20 ; 50-99 : +15 ; 20-49 : +10 ; <20 : +5
- **Patron répond aux avis** : oui (mesure : ≥30% des avis ont une réponse du propriétaire) : +20 ; partiel : +10 ; jamais : 0
- **Fiche GMB complète** (photos ≥10, horaires, description, catégories) : +15
- **Présence Instagram active** (dernier post <30 jours, si détectable) : +10
- **Âge du site eatbu ≥3 ans** : +10 (patron lassé, prêt à changer)
- **Âge du site eatbu <6 mois** : -20 (patron vient d'investir, refusera)

Score plafonné à 100, plancher à 0.

#### Score combiné

```
score_total = 0.5 × valeur_apportée + 0.5 × probabilité_acceptation
```

Tier dérivé :
- **A** : score ≥ 75 (cibles prioritaires, à visiter en premier)
- **B** : 50-74 (cibles moyennes, à visiter après le rodage)
- **C** : <50 (à laisser de côté pour l'instant, ou pitcher quand Mike sera à l'aise)

### Étape 7 — Synchronisation dans la liste vivante + génération des vues

**Source de vérité unique : `prospects/restaurants.yml`** (voir `prospects/README.md`).
Ce fichier persiste et s'enrichit run après run — il N'est PAS écrasé. Pour chaque resto
scanné : créer l'entrée si elle n'existe pas, sinon mettre à jour le bloc `scan` + `scoring`
**sans toucher** aux blocs `tunnel` et `notes_mike` (écrits par `pilote-client` / Mike), et
**sans écraser** un `scoring.mike_override` existant.

Vues régénérées (jamais éditées à la main, toutes dérivées de `restaurants.yml`) :

1. `prospects/restaurants.csv` — **vue plate vivante**, 1 ligne / resto, colonnes
   resserrées et claires, prête à déposer dans un outil d'infographie ou Google Sheets.
2. Dans `prospects/{ville}-{YYYY-MM-DD}/` (snapshot daté d'une campagne) :
   - `prospects-avec-site-eatbu.md` — triée par score décroissant
   - `prospects-avec-site-autre.md` — triée par score décroissant
   - `prospects-sans-site.md` — triée par score décroissant
   - `prospects-exclus.md` — chaînes nationales + sites custom modernes (avec raison)
   - `tableau-recap.csv` — export **brut riche** de la campagne (toutes les sous-métriques
     Lighthouse, drapeaux, etc.), squelette dans `templates/tableau-recap.csv`

---

## Format de chaque fiche de prospect (dans les .md)

```markdown
### {N°}. {Nom du resto} — Tier {A/B/C}, score {XX}/100

**Adresse :** {rue, ville}
**Téléphone :** {numéro si connu}
**Site actuel :** {URL ou "pas de site"}
**Note Google :** {x.x} ({n} avis)
**Cuisine :** {italienne / française / etc.}

**Sous-scores :**
- Valeur apportée : {XX}/100
- Probabilité d'acceptation : {XX}/100

**Top 3 arguments à pitcher :**
1. {argument basé sur la pire métrique mesurée — ex : "Son site charge en 5.2s sur mobile, c'est 4× trop lent. 30% de ses visiteurs partent avant d'avoir vu le menu."}
2. {2e argument — ex : "Son SEO score 42/100, il n'apparaît pas sur 'restaurant italien chartres'. Vérifié à l'instant : il est en page 3 alors que son concurrent direct est en page 1."}
3. {3e argument — ex : "Sa fiche Google n'a que 4 photos, dont une floue. Un patron qui investit dans des belles photos voit ses clics doubler."}

**Drapeau rouge éventuel :** {ex : "Patron ne répond jamais aux avis = à éviter pour ta 1ère visite, prends quelqu'un de plus 'numérique-friendly'."}

**Notes Mike :** _(à remplir à la main après visite)_

---
```

---

## Garde-fous critiques

1. **Aucun email/téléphone scrappé en masse pour cold outreach automatisé.** Ce skill produit des fiches que Mike utilise pour des visites en personne. Pas de spam, pas d'envoi auto.

2. **Pas de comparaison nominative entre prospects** dans les listes. Chaque fiche est autonome (le n°3 ne mentionne jamais le n°1).

3. **Le skill ne juge pas la valeur humaine d'un patron.** Un score bas = "pas le bon timing" ou "pas la bonne cible aujourd'hui", jamais "mauvais resto".

4. **Wayback Machine et OSM sont des sources publiques librement utilisables.** Pas de scraping de Google Maps (ToS), pas de scraping de la fiche GMB en masse. Si on a besoin d'enrichir une fiche GMB, Mike le fait à la main pour 5-10 cibles prioritaires.

5. **La liste n'est pas figée.** Mike peut overrider tout score à la main, le skill garde son override entre runs (champ `mike_override` dans le CSV).

6. **Le score n'est pas une vérité absolue.** C'est un outil d'aide à la priorisation, pas un oracle. Mike a le dernier mot.

7. **Confidentialité :** ne JAMAIS publier ces listes hors du repo MB Studio. Les fiches contiennent des données déjà publiques mais agrégées de façon qui pourrait être perçue comme intrusive par un patron qui découvrirait son fichier.

---

## Resources à créer pendant l'implémentation

- `skills/scoring-prospects/SKILL.md` — le skill lui-même (à écrire en suivant cette spec)
- `skills/scoring-prospects/references/chaines-nationales.md` — liste statique des chaînes à exclure
- `skills/scoring-prospects/references/scoring-formula.md` — formule de score détaillée et justifiée
- `skills/scoring-prospects/references/argument-library.md` — bibliothèque de phrases d'arguments à utiliser par le skill quand il génère le "Top 3 arguments à pitcher"
- `skills/scoring-prospects/templates/fiche-prospect.md` — squelette de fiche
- `skills/scoring-prospects/templates/tableau-recap.csv` — squelette du CSV récap

---

## Mode dégradé (sans clé Google PageSpeed)

Si la clé API n'est pas configurée :
- Skip l'étape 3 (Lighthouse), tous les scores Lighthouse = `null`
- Recalculer le sous-score "Valeur apportée" en redistribuant les pondérations sur les critères restants (âge + GMB)
- Marquer chaque fiche avec un encart "⚠️ Score approximatif (Lighthouse non mesuré)"
- Inviter Mike à configurer la clé pour le prochain run

---

## Décisions Mike validées en session du 2026-05-15

- Source : Overpass OSM auto + complément GMB
- Score 0-100 + tiers A (≥75) / B (50-74) / C (<50)
- Exclusions auto : chaînes nationales + sites custom modernes (Lighthouse ≥85 et pas eatbu)
- **Priorité 1**, avant `audit-livraison`
- Décisions tranchées sans re-questionner Mike :
  - 3 listes au lieu de 2 (eatbu / autre-site / pas-de-site)
  - Score = 50% valeur + 50% probabilité
  - Clé PageSpeed obligatoire en mode normal, mode dégradé documenté

---

## Hors-scope (ne PAS implémenter dans ce skill)

- Cold emailing / cold calling automatisé (Mike fait du porte-à-porte uniquement)
- Détection automatique du patron sur LinkedIn (intrusif, pas le ton MB Studio)
- Score d'évolution dans le temps (un seul snapshot suffit pour démarrer ; revisiter dans 6 mois)
- Intégration CRM (Mike n'a pas de CRM, le CSV suffit pour les 20 premiers clients)
- Géocodage avancé / clustering géographique pour optimiser les tournées (overkill, Mike connaît Chartres par cœur)
- Scoring "ennemi" : marquer les restos déjà clients d'une autre agence (impossible à détecter de façon fiable et hors-scope)
