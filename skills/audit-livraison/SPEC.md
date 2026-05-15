# Spec — Skill `audit-livraison`

> Document de spécification destiné au Claude qui codera ce skill (en local terminal, avec contexte frais sur `templates/site-resto/` et les autres skills MB Studio). Cette spec a été co-écrite avec Mike en session cloud le 2026-05-15. Toute décision d'implémentation doit respecter ces choix sauf clarification explicite de Mike.

---

## Pourquoi ce skill existe

Mike construit chaque site avec `site-from-brief`. À la fin, il a un site qui marche, mais il n'a aucune vue d'ensemble sur **ce qui pourrait coincer à la livraison** ni sur **ce qui est suffisamment fort pour être valorisé devant le patron**. Aujourd'hui c'est implicite, dans sa tête, et donc oubliable.

`audit-livraison` produit deux choses, à chaque fin de construction :

1. **Un audit interne brut** pour Mike — brutalement honnête, pour corriger avant de livrer.
2. **Un rapport de mise en service** pour le patron — valorisant, factuel, traduit en bénéfices business, présenté à la visite de livraison.

Ce skill tourne **après** `site-from-brief` et **avant** la visite de livraison (étape 4 du process).

---

## Triggers

**MANDATORY TRIGGERS :**
- "audit livraison"
- "lance l'audit du site"
- "audite le site avant livraison"
- "rapport de mise en service"

**STRONG TRIGGERS (avec contexte client) :**
- "le site de {slug} est prêt, on l'audite"
- "vérifie {slug} avant que j'aille chez le patron"

**Mode projet (cas spécial) :**
- "audite la vitrine MB Studio"
- "audit-livraison sur le projet" → mode projet (voir section "Modes" plus bas)

**Ne pas déclencher pour :**
- Audit froid d'un site eatbu avant signature (c'est `audit-eatbu`)
- Review de code (c'est `/review` ou `/security-review`)

---

## Inputs requis au démarrage

Le skill demande à Mike, en une passe :

> "OK on audite. Donne-moi :
> 1. Le slug du client (ex : `le-saint-hilaire`) — je vais lire `clients/{slug}/` et `briefs/{slug}/`
> 2. L'URL de prod du nouveau site (Cloudflare Pages) si déjà déployée, ou je build en local
> 3. Mode : `client` (défaut) ou `projet` (pour auditer MB Studio lui-même)"

Si le slug est absent → bloquer. Si l'URL de prod est absente → faire un build local et auditer le `dist/`. Si le mode n'est pas précisé → assumer `client`.

---

## Modes

### Mode `client` (cas standard)

Produit **deux outputs** dans `clients/{slug}/audit-livraison/` :

- `audit-interne.md` — pour Mike uniquement, brutal, exhaustif
- `rapport-mise-en-service.md` — pour le patron, valorisant, présentable
- `rapport-mise-en-service.pdf` (optionnel si Mike a `pandoc` + LaTeX, sinon on s'en passe : le .md suffit, Mike imprime depuis VSCode)

### Mode `projet`

Le projet MB Studio lui-même = vitrine, repo, skills. Pas de patron à qui montrer.

Produit **un seul output** : `audit-interne.md` à la racine du repo MB Studio (pas de dossier client). Mike le lance une fois maintenant + tous les 6 mois.

---

## Pipeline du skill (8 étapes)

### Étape 1 — Discovery (lire le contexte client)

Le skill lit, dans cet ordre :

1. `briefs/{slug}/brief.md` — pour connaître les promesses faites au patron pendant le brief
2. `briefs/{slug}/settings.yml` — pour comparer avec le settings final du site
3. `briefs/{slug}/eatbu-snapshot/` — pour la comparaison "avant" (si présent ; sinon noter "snapshot eatbu absent, pas de comparaison possible" dans l'audit interne)
4. `clients/{slug}/src/content/settings/site.yml` — état actuel du site
5. `clients/{slug}/src/content/menu/` — menus actuels
6. `clients/{slug}/README.md` — pour vérifier qu'il a été personnalisé (pas resté générique)
7. `clients/{slug}/incident-response.md` — pour vérifier qu'il a été personnalisé (numéros, URLs)

À la fin de cette étape, le skill connaît : ce qui a été promis, ce qui a été livré, ce qui était l'ancien état.

### Étape 2 — Build & déploiement de test

Si l'URL de prod n'est pas fournie :
- `cd clients/{slug}/ && npm install && npm run build`
- Si le build échoue → 🔴 BLOQUANT immédiat, on s'arrête, on dit à Mike "build cassé, je ne peux pas auditer un site qui ne build pas"
- Servir `dist/` via `npm run preview` (port 4321) pour les checks suivants

Si l'URL de prod est fournie : utiliser cette URL pour les checks suivants.

### Étape 3 — Lighthouse mobile (sur le nouveau site)

Lancer Lighthouse en mode mobile sur :
- `/` (homepage)
- `/menu` (page menu)
- `/contact` (page contact, si elle existe)

Récupérer les 4 scores (Performance, Accessibilité, SEO, Bonnes pratiques) + métriques Core Web Vitals (LCP, CLS, INP/FID, FCP, TBT) + poids total transféré.

Sauvegarder le rapport Lighthouse brut dans `clients/{slug}/audit-livraison/lighthouse-new.json`.

### Étape 4 — Comparaison avec l'ancien site eatbu

Si `briefs/{slug}/eatbu-snapshot/lighthouse.json` existe :
- Calculer les écarts (Δ Performance, Δ LCP, Δ poids, etc.)
- Préparer les phrases bénéfice patron (voir section "Output B" plus bas)

Si absent :
- Noter dans l'audit interne : "🟡 Snapshot eatbu absent, comparaison avant/après impossible. À documenter pour les prochains clients."
- Le rapport patron n'aura pas la section "Votre ancien site vs votre nouveau site"

### Étape 5 — Comparaison avec une moyenne sectorielle

Le skill maintient un fichier de référence `skills/audit-livraison/references/eatbu-benchmarks.md` (à créer par le futur Claude codeur) contenant les Lighthouse moyens d'un échantillon de sites eatbu (5-10 sites chartrains/français, à mesurer une fois et à ré-évaluer tous les 6 mois).

Le rapport patron utilisera cette moyenne pour une phrase type : "Un autre restaurant local dans votre catégorie : performance 3.1s, score Google 65/100. Votre site : 0.8s, 95/100."

**Pas de comparaison nominative** (jamais "Le Pichet a un site moins rapide"). Anonyme uniquement.

### Étape 6 — Checks fonctionnels (cohérence brief vs site)

Le skill compare le `brief.md` au site livré et liste tout ce qui diverge :

- Téléphone identique entre brief et site ? Adresse ? Horaires ?
- Tous les plats du brief sont-ils dans le menu du site ?
- Les allergènes sont-ils tous présents ?
- Le mode (fixe / foodtruck) du brief est-il bien reflété dans `site.yml` ?
- Le `google_maps_embed_url` du brief est-il celui injecté ?
- Le slogan exact du brief est-il sur la home ?

Chaque divergence = 🔴 BLOQUANT ou 🟡 À AMÉLIORER selon gravité (téléphone faux = bloquant ; ordre des plats différent = à améliorer).

### Étape 7 — Checks "patron-facing" (ce que le patron verra le 1er jour)

Vérifications spécifiques aux engagements MB Studio :

- **Decap CMS accessible** : tester que `/admin/` charge et que la config Decap référence bien les champs du brief
- **Favicon présent et personnalisé** (pas le favicon Astro par défaut)
- **README.md client personnalisé** (pas le générique du template)
- **`incident-response.md` personnalisé** (numéros utiles, URL Cloudflare du client, etc.)
- **Page 404 personnalisée** (signature MB Studio + ton du resto, pas la 404 par défaut Astro)
- **Footer signé "Site édité par MB Studio"** présent
- **Aucune mention "{{placeholder}}", "lorem ipsum", "TODO" dans le HTML rendu** → check critique
- **Aucune image cassée** (toutes les `<img>` retournent 200, pas 404)
- **Toutes les pages déclarées dans le menu de nav existent réellement**
- **Métadonnées OpenGraph** : titre, description, og:image présents et corrects

### Étape 8 — Sortie : génération des deux rapports

Voir sections "Output A" et "Output B" ci-dessous pour le format exact attendu.

---

## Output A — `audit-interne.md` (pour Mike)

**Audience :** Mike uniquement. Brutalement honnête. Pas destiné au patron.

**Ton :** direct, pair-à-pair, tutoiement. "Tu as oublié X." Pas de fioritures.

**Structure imposée :**

```markdown
# Audit interne — {Nom du client}

Date : {YYYY-MM-DD}
Slug : {slug}
URL auditée : {url ou "build local"}
Score Lighthouse global : {moyenne perf/access/seo/best-practices}

---

## 🔴 BLOQUANTS — à régler AVANT de prévenir le patron

{liste numérotée. Si vide : "Rien à régler. Tu peux livrer."}

Chaque item suit ce format :
1. **{Titre court du problème}**
   - Où : {chemin fichier ou URL spécifique}
   - Pourquoi c'est bloquant : {1 phrase}
   - Comment réparer : {action concrète, max 3 lignes}

---

## 🟡 À AMÉLIORER — décision Mike

{liste numérotée. Items non bloquants mais dignes d'attention.}

Pour chaque item, noter si c'est :
- Réparable en <15min → tag `[quick win]`
- Pertinent à proposer dans le Pack Suivi → tag `[pitch suivi]`
- Reportable au prochain client → tag `[backlog]`

---

## 🟢 POINTS FORTS — à pointer au patron pendant la livraison

{liste de 3-5 forces objectives, factuelles. Ce sont les phrases que Mike peut prononcer pendant la visite de livraison, ou qui alimenteront le rapport patron (output B).}

Exemple :
- "Lighthouse perf mobile : 96/100. C'est dans le top 5% mondial."
- "Site complet en 0.8s vs 4.2s pour l'ancien eatbu."
- "Tous les plats du brief sont sur le site, avec allergènes."

---

## 💡 IDÉES BONUS — cadeau surprise à découvrir pendant la livraison

{1 à 3 propositions créatives qui matchent le ton du resto. Pas obligatoires.}

Mike choisit 0, 1 ou plusieurs à implémenter avant la livraison. Si rien ne lui inspire, il reporte au prochain client.

Exemple :
- "Page 404 avec dessin du chef qui rate une omelette + bouton 'retour au menu'"
- "Favicon animé : la cocotte qui fume légèrement au scroll"
- "Easter egg : taper le code du jour de fermeture affiche un message du patron"

---

## Métriques brutes (pour mémoire)

| Métrique | Nouveau site | Ancien site eatbu | Moyenne sectorielle |
|---|---|---|---|
| Performance mobile | {x}/100 | {x ou n/a}/100 | {x}/100 |
| Accessibilité | ... | ... | ... |
| SEO | ... | ... | ... |
| Bonnes pratiques | ... | ... | ... |
| LCP (mobile) | {x}s | {x ou n/a}s | {x}s |
| Poids transféré | {x}KB | {x ou n/a}KB | {x}KB |

---

## Cohérence brief vs site

| Élément brief | Présent sur le site ? | Identique ? |
|---|---|---|
| Téléphone | ✅ | ✅ |
| Adresse | ✅ | ✅ |
| {tous les items vérifiés à l'étape 6} | | |
```

---

## Output B — `rapport-mise-en-service.md` (pour le patron)

**Audience :** le patron du resto. Présenté à la livraison sur tablette ou imprimé.

**Ton :** vouvoiement, valorisant **mais factuel**. Pas de superlatifs ronflants. Pas de jargon tech (sauf 1-2 termes expliqués).

**Règle d'or :** si une métrique n'apporte rien de positif (ex : Lighthouse perf 72), elle **n'apparaît pas** dans ce rapport. Mike ne ment pas, mais il ne valorise que ce qui mérite d'être valorisé.

**Structure imposée :**

```markdown
# Votre nouveau site est en ligne — {Nom du resto}

Livré le {DD/MM/YYYY} par Mike (MB Studio).

---

## Ce que vous avez gagné, en chiffres

{3 à 5 métriques traduites en français patron. Chaque métrique suit ce format :}

### Vitesse de chargement

Votre nouveau site charge en **{X} seconde{s}**.
{Si snapshot eatbu existant :} Votre ancien site eatbu prenait **{Y} secondes** — votre site est **{Z}× plus rapide**.

**Pourquoi c'est important :** {phrase de bénéfice business, ex : "30% des visiteurs partent quand un site dépasse 3 secondes. Vous gardez ces 30%."}

### Référencement Google

Score Google de votre site : **{X}/100**.
{Si snapshot eatbu :} Votre ancien site : {Y}/100.

**Pourquoi c'est important :** "Google comprend parfaitement votre menu, vos horaires et vos prix. Vous apparaîtrez plus facilement sur des recherches comme '{exemple basé sur la spécialité}'."

### {Etc. pour les autres métriques sélectionnées}

---

## Vs un autre restaurant local (anonyme)

Pour vous donner une référence : nous avons mesuré {N} sites de restaurants chartrains comparables.

| | Leur site (moyenne) | Votre site |
|---|---|---|
| Vitesse | {X}s | **{Y}s** |
| Score Google | {X}/100 | **{Y}/100** |
| Score Accessibilité | {X}/100 | **{Y}/100** |

{NB : section omise si le nouveau site n'est PAS au-dessus de la moyenne sur au moins 2 métriques sur 3.}

---

## Ce que ça change concrètement pour vous

{3 à 4 puces en bénéfices clients très concrets, jamais en termes techniques.}

- Un client qui cherche "{spécialité du resto} {ville}" sur Google verra votre menu directement dans les résultats (pas besoin de cliquer).
- Une personne âgée ou malvoyante peut lire votre menu sans loupe ni zoom (taille de texte respectée, contrastes vérifiés).
- Votre site fonctionne en 4G sur un téléphone bas de gamme, en moins d'une seconde.
- Vous éditez votre menu, vos horaires et vos photos en autonomie depuis l'adresse {URL}/admin/ — sans nous appeler.

---

## Un petit cadeau, en plus

{Texte court qui décrit le "cadeau surprise" implémenté pour ce site, voir Output A → "Idées bonus". Décrit en termes patron, pas tech. Si aucun cadeau implémenté, omettre cette section.}

Exemple : "Quand un visiteur tape une URL qui n'existe pas sur votre site, il tombe sur une petite illustration du chef en train de rater une omelette, avec un bouton pour revenir au menu. Petit clin d'œil, sans prétention."

---

## Et après ?

Votre site est à vous. L'adresse, le code, les contenus : tout est sur votre nom.

Vous pouvez l'éditer seul. Si vous voulez un suivi mensuel (rapport visiteurs, optimisation Google Business, mises à jour techniques), on en parle à tête reposée.
```

---

## Garde-fous critiques

1. **Le skill ne ment jamais au patron.** Si une métrique est mauvaise, elle n'apparaît pas dans Output B. Mais dans Output A, elle apparaît clairement.

2. **Pas de comparaison nominative dans Output B.** Jamais "Le restaurant X a un site moins bien". Toujours "moyenne sectorielle" ou "un autre restaurant local".

3. **Output B doit pouvoir être imprimé sur 1-2 pages A4.** Si ça déborde, le skill doit raccourcir, pas allonger.

4. **Output A ne sort jamais du dossier client.** `audit-interne.md` n'est pas pour le patron. Ne JAMAIS le mélanger avec Output B.

5. **Si le snapshot eatbu est absent**, le rapport patron est plus court mais reste utile. Ne pas inventer de chiffres.

6. **Cadeau surprise** : Output A propose 1-3 idées. C'est Mike qui décide et qui implémente. Si rien n'est implémenté à l'heure de la livraison, la section "Un petit cadeau, en plus" de Output B est **omise** — pas inventée.

7. **Le mode `projet`** ne produit jamais d'Output B. Le projet MB Studio n'a pas de patron.

---

## Resources à créer pendant l'implémentation

- `skills/audit-livraison/SKILL.md` — le skill lui-même (à écrire en suivant cette spec)
- `skills/audit-livraison/references/eatbu-benchmarks.md` — Lighthouse moyens de 5-10 sites eatbu chartrains, mesurés à la main une fois, ré-évalués tous les 6 mois
- `skills/audit-livraison/references/benefit-translations.md` — table de correspondance "métrique technique → phrase bénéfice patron" (Performance → vitesse de chargement → "30% partent au-delà de 3s", SEO → référencement Google, Accessibilité → "personnes âgées et malvoyantes", etc.) — à utiliser comme bibliothèque par le skill
- `skills/audit-livraison/templates/audit-interne.md` — squelette de Output A
- `skills/audit-livraison/templates/rapport-mise-en-service.md` — squelette de Output B
- `skills/audit-livraison/references/checklist-patron-facing.md` — la liste complète de l'étape 7 (favicon, README, incident-response, 404, footer, etc.) à transformer en checks scriptables

---

## Décisions Mike validées en session du 2026-05-15

- 4 niveaux de gravité : 🔴 Bloquant / 🟡 À améliorer / 🟢 Point fort / 💡 Idée bonus
- Deux outputs séparés (interne brut + patron valorisant), produits dans la même passe
- Comparaison "ancien eatbu vs nouveau" basée sur snapshot fait au moment du brief
- Comparaison "moyenne sectorielle" en plus, anonyme uniquement
- Pas de garantie Lighthouse ≥ 90, mais si atteint, c'est valorisé. Si raté, c'est bloquant en interne (à corriger ou justifier).
- Lighthouse rapproché à des bénéfices business en langage patron, pas en chiffres bruts.
- Mode `projet` parallèle pour auditer MB Studio lui-même (sans Output B).

---

## Hors-scope (ne PAS implémenter dans ce skill)

- Diagnostic d'incident en prod (c'est le futur skill `incident` qui s'en chargera)
- Audit SEO sémantique (mots-clés, positionnement) — c'est le rôle de `monthly-report`
- Test sur navigateurs anciens (IE11, etc.) — pas le public cible
- Tests d'écriture pour Decap (ouvrir l'admin, créer un post test) — trop fragile pour de l'automatisation, Mike le fait à la main
- Génération de PDF du rapport patron — `pandoc` optionnel si dispo, sinon Mike imprime le .md depuis son éditeur
