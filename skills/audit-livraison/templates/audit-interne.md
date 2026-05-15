# Audit interne — {NOM_CLIENT}

Date : {YYYY-MM-DD}
Slug : {slug}
URL auditée : {URL_OU_"build local dist/"}
Mode : {client | projet}
Score Lighthouse global : {MOYENNE_4_SCORES}/100

---

## 🔴 BLOQUANTS — à régler AVANT de prévenir le patron

{Si vide : "Rien à régler. Tu peux livrer."}

1. **{Titre court du problème}**
   - Où : {chemin fichier ou URL}
   - Pourquoi c'est bloquant : {1 phrase}
   - Comment réparer : {action concrète, max 3 lignes}

---

## 🟡 À AMÉLIORER — décision Mike

{liste numérotée, items non bloquants. Tag chacun : `[quick win]` (<15min) / `[pitch suivi]` (Pack Suivi) / `[backlog]` (prochain client / amélioration template)}

1. **{Titre}** `[tag]`
   - {description + action}

---

## 🟢 POINTS FORTS — à pointer au patron pendant la livraison

{3-5 forces objectives factuelles, formulées comme des phrases prononçables par Mike. Alimentent l'Output B.}

- {ex : "Lighthouse perf mobile : 96/100, top 5% mondial."}
- {ex : "Site complet en 0,8 s vs 4,2 s pour l'ancien eatbu."}

---

## 💡 IDÉES BONUS — cadeau surprise à découvrir pendant la livraison

{1-3 propositions créatives matchant le ton du resto. Mike choisit 0, 1 ou plusieurs.}

- {ex : "Page 404 : illustration du chef qui rate une omelette + bouton retour menu."}

---

## Métriques brutes (pour mémoire)

| Métrique | Nouveau site | Ancien eatbu | Moyenne secteur |
|---|---|---|---|
| Performance mobile | {x}/100 | {x ou n/a} | {x}/100 |
| Accessibilité | {x}/100 | {x ou n/a} | {x}/100 |
| SEO | {x}/100 | {x ou n/a} | {x}/100 |
| Bonnes pratiques | {x}/100 | {x ou n/a} | {x}/100 |
| LCP (mobile) | {x}s | {x ou n/a} | {x}s |
| Poids transféré | {x}KB | {x ou n/a} | {x}KB |

{Si snapshot eatbu absent : "🟡 Snapshot eatbu absent — comparaison avant/après impossible. Documenter au brief pour les prochains clients."}
{Si mode dégradé Lighthouse : "⚠️ Lighthouse non mesuré (clé PageSpeed absente)."}

---

## Cohérence brief vs site (étape 6)

| Élément brief | Présent sur le site ? | Identique ? | Gravité si écart |
|---|---|---|---|
| Téléphone | {✅/❌} | {✅/❌} | 🔴 |
| Adresse | {✅/❌} | {✅/❌} | 🔴 |
| Horaires (mode {fixe/foodtruck}) | {✅/❌} | {✅/❌} | 🔴 |
| Tous les plats du brief | {✅/❌} | {✅/❌} | 🟡 |
| Allergènes | {✅/❌} | {✅/❌} | 🔴 (légal) |
| Slogan exact | {✅/❌} | {✅/❌} | 🟡 |
| google_maps_embed_url | {✅/❌} | {✅/❌} | 🟡 |

---

## Checklist patron-facing (étape 7)

{Reprendre les 14 checks de references/checklist-patron-facing.md avec leur résultat ✅/❌ et la gravité. Les ❌ sont déjà reportés dans les sections BLOQUANTS / À AMÉLIORER ci-dessus — ce tableau est le récap exhaustif.}

| # | Check | Résultat | Gravité |
|---|---|---|---|
| 1 | Decap CMS accessible | {✅/❌} | 🔴 |
| ... | ... | ... | ... |

---

_Ce fichier ne sort JAMAIS du dossier client. Il n'est pas pour le patron._
