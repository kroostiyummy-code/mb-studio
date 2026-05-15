---
name: audit-livraison
description: "Audite un site client juste avant la visite de livraison (étape 4 du process MB Studio, après site-from-brief). Produit DEUX rapports en une passe : un audit interne brutalement honnête pour Mike (4 niveaux 🔴🟡🟢💡) + un rapport de mise en service valorisant et factuel pour le patron (zéro jargon, vouvoiement, métriques traduites en bénéfices business). Compare le nouveau site au snapshot eatbu archivé au brief et à une moyenne sectorielle anonyme. Mode projet pour auditer la vitrine MB Studio elle-même. MANDATORY TRIGGERS: 'audit livraison', 'lance l'audit du site', 'audite le site avant livraison', 'rapport de mise en service'. STRONG TRIGGERS (avec contexte client): 'le site de {slug} est prêt, on l'audite', 'vérifie {slug} avant que j'aille chez le patron'. MODE PROJET: 'audite la vitrine MB Studio', 'audit-livraison sur le projet'. Ne pas déclencher pour : audit froid d'un eatbu avant signature (c'est audit-eatbu), review de code (c'est /review)."
---

# Audit Livraison

Skill MB Studio qui sécurise la livraison. Tourne **après `site-from-brief`** et **avant la visite de livraison** (étape 4). Produit deux rapports dans la même passe :

1. **`audit-interne.md`** — pour Mike. Brutalement honnête, exhaustif, tutoiement. Sert à corriger avant de livrer.
2. **`rapport-mise-en-service.md`** — pour le patron. Valorisant mais factuel, vouvoiement, zéro jargon. Présenté à la livraison.

Le skill ne ment jamais au patron : une métrique mauvaise n'apparaît pas dans le rapport patron (mais elle est dans l'audit interne).

---

## Quand déclencher

**Bons cas :** "audit livraison", "le site de le-saint-hilaire est prêt on l'audite", "audite la vitrine MB Studio" (mode projet).

**Mauvais cas (ne pas déclencher) :**
- Audit froid d'un eatbu avant signature → `audit-eatbu`
- Review de code → `/review` ou `/security-review`

---

## Inputs requis au démarrage

> "OK on audite. Donne-moi :
> 1. Le slug du client (ex : `le-saint-hilaire`) — je lis `clients/{slug}/` et `briefs/{slug}/`
> 2. L'URL de prod (Cloudflare Pages) si déjà déployée, sinon je build en local
> 3. Mode : `client` (défaut) ou `projet` (auditer MB Studio lui-même)"

- Slug absent en mode client → **bloquer** (rien à auditer).
- URL prod absente → build local + `npm run preview`, auditer le `dist/`.
- Mode non précisé → `client`.

---

## Modes

### Mode `client` (standard)
Produit dans `clients/{slug}/audit-livraison/` :
- `audit-interne.md` (Mike only, brutal)
- `rapport-mise-en-service.md` (patron, valorisant)
- `rapport-mise-en-service.pdf` *(optionnel, seulement si `pandoc` dispo ; sinon le .md suffit, Mike imprime depuis son éditeur)*

### Mode `projet`
Audite MB Studio lui-même (repo, skills, futur site vitrine). **Un seul output** : `audit-interne.md` à la racine du repo. Pas de rapport patron (pas de patron). À lancer maintenant + tous les 6 mois.

---

## Pipeline en 8 étapes

### Étape 1 — Discovery (lire le contexte)

Lire dans l'ordre (mode client) :
1. `briefs/{slug}/brief.md` — ce qui a été promis
2. `briefs/{slug}/settings.yml` — settings issu du brief
3. `briefs/{slug}/eatbu-snapshot/` — l'état "avant" (si absent : noter "🟡 snapshot eatbu absent" et continuer sans la comparaison avant/après)
4. `clients/{slug}/src/content/settings/site.yml` — état livré
5. `clients/{slug}/src/content/menu/` — menus livrés
6. `clients/{slug}/README.md` — vérifier personnalisation
7. `clients/{slug}/incident-response.md` — vérifier personnalisation

Mode projet : lire `CLAUDE.md`, `process.md`, `skills/*/SKILL.md`, `templates/site-resto/`. L'audit porte sur la cohérence du repo et la santé du template, pas sur un client.

### Étape 2 — Build & service

Si URL prod fournie → l'utiliser pour les checks réseau.
Sinon :
```bash
cd clients/{slug} && npm install && npm run build
```
- Build échoue → **🔴 BLOQUANT immédiat**, stop. "Build cassé, je n'audite pas un site qui ne build pas. Relance site-from-brief après correction."
- Build OK → `npm run preview` (port 4321) pour les checks réseau.

### Étape 3 — Lighthouse mobile

**⚠️ Adaptation réelle (2026-05-15) :** le template `site-resto/` réel n'a que **2 pages** : `/` (index) et `/mentions-legales`. PAS de `/menu` ni `/contact` (le menu est une section ancre `#menu` de la home, le contact est un `tel:`). Donc Lighthouse mobile sur :
- `/` (homepage — la page critique)
- `/mentions-legales` (page légale)

Via PageSpeed API si clé dispo (`~/.mb-studio/secrets.env` → `GOOGLE_PAGESPEED_API_KEY`), sinon Lighthouse CLI local sur le `preview`, sinon **mode dégradé** (scores `null`, noté dans l'audit interne, rapport patron sans section chiffres vitesse).

```bash
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={URL}/&strategy=mobile&category=PERFORMANCE&category=ACCESSIBILITY&category=SEO&category=BEST_PRACTICES&key={KEY}"
```

Sauvegarder le brut dans `clients/{slug}/audit-livraison/lighthouse-new.json`. Extraire 4 scores + LCP/CLS/INP/FCP/TBT + poids transféré (`audits['total-byte-weight']`).

### Étape 4 — Comparaison ancien eatbu

Si `briefs/{slug}/eatbu-snapshot/lighthouse.json` existe → calculer Δ (perf, LCP, poids, SEO…) pour les phrases "avant/après" du rapport patron.
Sinon → audit interne : "🟡 Snapshot eatbu absent, comparaison avant/après impossible. À documenter pour les prochains clients." Rapport patron sans section comparative.

### Étape 5 — Comparaison moyenne sectorielle

Lire `references/eatbu-benchmarks.md`. Comparaison **anonyme uniquement** ("un autre restaurant local comparable" / "moyenne du secteur" — jamais de nom). Tant que le benchmark est en statut estimation : écrire "moyenne estimée". Section incluse dans le rapport patron seulement si le nouveau site bat la moyenne sur **≥ 2 métriques sur 3**.

### Étape 6 — Cohérence brief vs site

Comparer `brief.md` au site livré. Pour chaque écart, classer 🔴 ou 🟡 :
- Téléphone identique brief↔site ? Adresse ? Horaires ? → écart = 🔴
- Tous les plats du brief dans le menu ? → manquant = 🟡, prix faux = 🔴
- Allergènes tous présents ? → manquant = 🔴 (obligation légale FR)
- Mode (fixe/foodtruck) du brief reflété dans `site.yml` ? → 🔴
- `google_maps_embed_url` du brief injecté ? → 🟡
- Slogan exact du brief sur la home ? → 🟡

### Étape 7 — Checks patron-facing

Dérouler **les 14 checks de `references/checklist-patron-facing.md`** avec leur méthode de test et gravité. Rappel des adaptations réelles : le template de base n'a PAS de 404 perso, PAS de favicon perso, PAS de signature footer "MB Studio" → ces checks **détectent l'absence** et la remontent (🟡 + candidats cadeau surprise / amélioration template). Ne jamais supposer leur présence.

Check 8 (placeholders `{{...}}` / lorem / TODO) et check 9 (images cassées) se font sur le `dist/` rendu, pas sur le source `.astro`. Check 10 : vérifier que les ancres du footer correspondent à des `id=` réellement rendus (l'auto-hide d'une section peut laisser un lien footer orphelin → à détecter).

### Étape 8 — Génération des 2 rapports

- `audit-interne.md` depuis `templates/audit-interne.md` — TOUTES les sections, brutal, tutoiement. Chaque écart des étapes 6-7 rangé dans 🔴 / 🟡 (taggé `[quick win]` / `[pitch suivi]` / `[backlog]`). Forces → 🟢. Manques 404/favicon → aussi 💡 idées bonus.
- `rapport-mise-en-service.md` depuis `templates/rapport-mise-en-service.md` — UNIQUEMENT les métriques bonnes (garde-fou #1), phrases piochées dans `references/benefit-translations.md`, vouvoiement, ≤ 2 pages A4. Section "cadeau" seulement si un cadeau a réellement été implémenté (sinon omise, jamais inventée). Mode projet : ne PAS produire ce fichier.

Récap final à Mike :
```
✅ Audit terminé — {slug} (mode {client|projet})
   🔴 {n} bloquants {— À RÉGLER avant de prévenir le patron | — aucun, tu peux livrer}
   🟡 {n} à améliorer ({q} quick wins)
   🟢 {n} points forts valorisables
   💡 {n} idées cadeau surprise
   Lighthouse global : {x}/100 {| ⚠️ mode dégradé}
📁 clients/{slug}/audit-livraison/
👉 Prochaine action : {si bloquants : "règle les 🔴 puis relance l'audit" | "aucun bloquant — tu peux caler la visite de livraison"}
```

---

## Garde-fous critiques

1. **Ne jamais mentir au patron.** Métrique mauvaise → absente de l'Output B, présente dans l'Output A.
2. **Aucune comparaison nominative dans Output B.** "Moyenne du secteur" / "un autre resto local" uniquement.
3. **Output B ≤ 2 pages A4.** Si ça déborde : raccourcir, jamais allonger.
4. **Output A ne sort JAMAIS du dossier client.** Ne jamais le mélanger ni l'envoyer au patron.
5. **Snapshot eatbu absent** → rapport patron plus court mais honnête. Ne pas inventer de chiffres "avant".
6. **Cadeau surprise** : Output A propose 1-3 idées, Mike décide et implémente. Section cadeau de Output B omise si rien d'implémenté — jamais inventée.
7. **Mode `projet`** ne produit jamais d'Output B.
8. **Build cassé = stop immédiat.** On n'audite pas un site qui ne build pas.

---

## Décisions Mike validées (NE PAS reposer)

- 4 niveaux : 🔴 Bloquant / 🟡 À améliorer / 🟢 Point fort / 💡 Idée bonus
- 2 outputs séparés produits en une passe
- Comparaison ancien eatbu via snapshot fait au brief
- Comparaison moyenne sectorielle anonyme en plus
- Pas de garantie Lighthouse ≥ 90, mais si atteint = valorisé, si raté = bloquant interne (corriger ou justifier)
- Lighthouse traduit en bénéfices patron, pas en chiffres bruts
- Mode `projet` parallèle sans Output B

---

## Hors-scope (NE PAS implémenter)

- Diagnostic d'incident en prod (futur skill `incident`)
- Audit SEO sémantique mots-clés/positionnement (rôle de `monthly-report`)
- Test navigateurs anciens (IE11…)
- Tests d'écriture Decap (ouvrir l'admin, créer un post test — trop fragile, Mike le fait à la main)
- Génération PDF du rapport (pandoc optionnel si dispo, sinon Mike imprime le .md)

---

## Resources

- `references/eatbu-benchmarks.md` — moyennes sectorielles anonymes (statut calibration)
- `references/benefit-translations.md` — table métrique tech → bénéfice patron
- `references/checklist-patron-facing.md` — les 14 checks étape 7, scriptables
- `templates/audit-interne.md` — squelette Output A
- `templates/rapport-mise-en-service.md` — squelette Output B

---

## Exemple d'invocation

```
Mike : Le site de le-saint-hilaire est prêt, audite-le avant que j'aille chez le patron jeudi.
```

Le skill : lit brief + clients/le-saint-hilaire/ → build local OK → Lighthouse `/` et `/mentions-legales` → compare au snapshot eatbu (perf 38→96, LCP 4,2s→0,9s) → benchmark secteur → cohérence brief/site (tel ✅, 1 plat oublié 🟡, allergènes ✅) → 14 checks patron-facing (404 absente 🟡+💡, footer non signé 🟡, README perso ✅) → génère audit-interne.md (2 🟡, 0 🔴, 4 🟢, 2 💡) + rapport-mise-en-service.md → "Aucun bloquant, tu peux caler la visite".
