# Format des vues de prospects (décision Mike 2026-05-18)

> **Règle gravée.** Architecture normalisée (Rapport_classement). Le scan
> produit un **classement global unique** + des **filtres** par catégorie, en
> `.md` **et** `.txt` lisible. Chaque vue s'ouvre par un bloc
> « 📋 Critères de cette liste ».

## Vues produites dans `prospects/{ville}-{date}/`

| Fichier | Contenu | Tri |
|---|---|---|
| `classement-global` | TOUS les restos scorés, toutes catégories | `score_final ↓ puis confidence ↓` |
| `liste-eatbu` | Filtre eatbu — **cœur de cible, liste de travail 1er rang** | `score_final ↓` |
| `liste-autre-site` | Filtre site perso existant | `score_final ↓` |
| `liste-sans-site` | Filtre sans site à eux | `score_final ↓` |
| `quick-wins` | Bande **Priorité semaine** (top ~10 global, conf OK) | `score_final ↓` |
| `prospects-exclus.md` | Chaînes + sites modernes + raison | nom |
| `tableau-recap.csv` | Export campagne (compat) | `score_final ↓` |

`source_list` (eatbu/autre/sans) = **filtre & angle de pitch uniquement**, ce
n'est pas un classement séparé : le radar de priorisation est le classement
global.

## En-tête de CHAQUE vue

```
# {Titre}

**Chartres — rayon {km} km — {date}** · {N} restaurants

## 📋 Critères de cette liste

- **Ce qui définit cette liste :** {définition simple}
- **Angle stratégique (pourquoi / comment pitcher) :** {angle}
- **Tri de cette liste :** {tri annoncé}

---
```

`liste-eatbu` porte un bloc Critères spécifique : cœur de cible MB Studio,
liste de travail 1er rang à mener **en parallèle** du classement global ;
score objectif structurellement plus bas (un eatbu a moins de déficit brut
qu'un sans-site) — **ne pas juger au score seul sur cette liste**.

## Bloc fiche (un par resto, libellés français)

```
### {N}. {Nom} — {Cuisine} — ⭐ {note} / {nb} avis

**Adresse :** {rue, cp ville — "adresse inconnue" si rien} · **Téléphone :** {tél|inconnu}
**Présence web :** {Site eatbu loué — url | Site perso — url | Aucun site à lui — page {plateforme} | Aucune présence web}
**Lighthouse :** {perf/SEO/access. + LCP s | — (pas de site) | non mesuré}
**Ce qu'on peut apporter :** {V}/100  ·  **Probabilité qu'il accepte :** {P}/100
**Score final :** {final}/100 · **Confiance : {conf}/100** · **Tier {A|B|C|D}**{ _(override Mike)_ }
**Pourquoi lui :** {1 phrase — écart le plus fort mesuré}
**Action :** {Priorité semaine | Priorité mois | Réserve | À surveiller (confiance faible)}

> ℹ️ {mention données partielles si confiance < 60}
> ⚠️ {mention vitesse non mesurée si Lighthouse absent sur site}
> 🚩 {drapeau rouge si présent}

---
```

Détail des composantes, Confidence, tiers et bandes : voir
`references/scoring-formula.md` (source unique de vérité). Les notes manuelles
de Mike vivent dans `restaurants.yml` (`notes_mike` / `couche2`), jamais dans
ces vues régénérables.
