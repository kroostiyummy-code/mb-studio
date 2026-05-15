# Checklist patron-facing (étape 7 du pipeline)

Liste scriptable des vérifications "ce que le patron verra le 1er jour". Chaque check a : comment le tester, gravité si échec, et l'état attendu vs l'état réel du template `site-resto/` (au 2026-05-15).

> **Note d'adaptation au réel (2026-05-15)** : le template `site-resto/` de base ne contient PAS encore : page 404 personnalisée, favicon personnalisé, signature "Site édité par MB Studio" dans le footer. Ces éléments sont censés être ajoutés **par client** au moment de `site-from-brief` / du cadeau surprise. L'audit-livraison doit donc DÉTECTER leur absence et la remonter comme bloquant ou à améliorer — c'est précisément sa valeur. Ne jamais supposer qu'ils sont présents.

---

## Checks et gravité

| # | Check | Comment tester | Gravité si absent |
|---|---|---|---|
| 1 | **Decap CMS accessible** | `GET {url}/admin/` retourne 200 + le HTML charge `decap-cms` ; `public/admin/config.yml` existe et `backend.repo` = `kroostiyummy-code/{slug}-site` (pas `USER/REPO`) | 🔴 Bloquant (promesse centrale "édition autonome") |
| 2 | **Config Decap cohérente brief** | `public/admin/config.yml` expose bien les collections correspondant au brief (menu, settings, galerie si photos) | 🟡 À améliorer |
| 3 | **Favicon personnalisé** | `<link rel="icon">` présent dans le `<head>` ET pointe vers un asset du resto (logo), PAS le favicon Astro par défaut (`/favicon.svg` générique) | 🟡 À améliorer + candidat cadeau surprise |
| 4 | **README client personnalisé** | `clients/{slug}/README.md` contient le nom du resto + URL + coords patron, PAS le README générique du template (`# Site web — {NOM_RESTO}` rempli, pas le template brut) | 🔴 Bloquant (sinon repo non maintenable + signe de bâclage) |
| 5 | **incident-response.md personnalisé** | `clients/{slug}/incident-response.md` contient l'encart "Coordonnées spécifiques à ce client" rempli (nom resto, tel patron, domaine, repo, dates) — pas seulement le générique | 🔴 Bloquant (sinon support impossible le jour J) |
| 6 | **Page 404 personnalisée** | `clients/{slug}/src/pages/404.astro` existe ET son contenu reflète le ton du resto / signature MB Studio (pas la 404 Astro brute) | 🟡 À améliorer + candidat cadeau surprise (le template de base n'en a pas → quasi toujours à créer) |
| 7 | **Footer signé MB Studio** | Le HTML rendu du footer contient une mention discrète "Site édité par MB Studio" (lien) — cf principe non-négociable #5 (ambassadeur). Template de base ne l'a PAS encore → à ajouter | 🟡 À améliorer (systématique tant que pas dans le template ; remonter aussi comme amélioration template à faire un jour) |
| 8 | **Aucun placeholder résiduel** | `grep -ri "{{.*}}\|lorem ipsum\|TODO\|FIXME\|à compléter\|XXXXX" dist/ --include="*.html"` en **excluant `dist/admin/`** (config Decap, pas patron-facing) → 0 résultat. ⚠️ Vérifié au dry-run 2026-05-15 : sans l'exclusion `dist/admin/` + `--include=*.html`, faux positif sur `dist/admin/config.yml` (contient `USER/REPO` tant que `new-client` n'a pas tourné — normal, ce n'est pas une page visiteur). | 🔴 Bloquant (un `{{NOM}}` visible chez le patron = catastrophe de crédibilité) |
| 9 | **Aucune image cassée** | Pour chaque `<img src>` du HTML rendu : requête HEAD → statut 200, pas 404 | 🔴 Bloquant |
| 10 | **Pages de nav existent** | Chaque lien interne du `<nav>`/footer (href commençant par `/` ou `#`) pointe vers une page/ancre qui existe réellement | 🔴 Bloquant si lien mort vers une page ; 🟡 si ancre absente |
| 11 | **OpenGraph complet** | `<meta property="og:title">`, `og:description`, `og:image` présents et non vides ; `og:image` retourne 200 | 🟡 À améliorer (partage social cassé sinon) |
| 12 | **HTTPS / pas de mixed content** | Si URL prod : tout en `https://`, aucune ressource `http://` chargée | 🔴 Bloquant si mixed content |
| 13 | **Téléphone cliquable** | Au moins un `<a href="tel:+33...">` présent et le numéro = celui du brief | 🔴 Bloquant (CTA principal resto) |
| 14 | **Mentions légales présentes** | `/mentions-legales` retourne 200 et contient éditeur + hébergeur + le nom du resto (pas resté générique) | 🔴 Bloquant (obligation légale FR) |

---

## Notes d'implémentation

- Les checks 1, 9, 11, 12 nécessitent une URL servie (prod Cloudflare ou `npm run preview` local sur `dist/`).
- Les checks 4, 5, 6 se font sur les fichiers de `clients/{slug}/` directement (pas besoin du site servi).
- Le check 8 (placeholders) se fait sur le `dist/` buildé, pas sur les `.astro` source (un `{var}` Astro légitime dans le source devient une vraie valeur dans le `dist/` — on audite le rendu, pas le code).
- Check 10 : le template `site-resto/` réel a 2 pages (`/` et `/mentions-legales`) + des ancres (`#menu`, `#localisation`, etc.). Vérifier que les ancres du footer correspondent à des `id=` réellement présents dans le HTML rendu (dépend des sections activées dans `settings.yml` → l'auto-hide peut retirer une section dont le footer garde le lien : à détecter).

---

## Sortie attendue

Chaque check alimente l'Output A (`audit-interne.md`) dans la bonne section :
- 🔴 → section "BLOQUANTS"
- 🟡 → section "À AMÉLIORER" (avec tag `[quick win]` / `[pitch suivi]` / `[backlog]`)
- check OK + valorisable → section "POINTS FORTS"
- check 3/6 absent → alimente aussi "IDÉES BONUS" (favicon perso, 404 du resto = cadeaux surprise naturels)
