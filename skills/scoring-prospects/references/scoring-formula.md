# Formule de scoring détaillée

Référence de calcul pour l'étape 6 du pipeline. Toute modification de pondération se fait ICI, jamais en dur dans le SKILL.md.

---

## Vue d'ensemble

```
score_total = 0.5 × valeur_apportée + 0.5 × probabilité_acceptation
```

- `valeur_apportée` ∈ [0, 100]
- `probabilité_acceptation` ∈ [0, 100]
- `score_total` ∈ [0, 100]

Tiers :
- **A** : score ≥ 75 → cibles prioritaires (visiter en premier)
- **B** : 50 ≤ score < 75 → cibles moyennes (après rodage)
- **C** : score < 50 → à laisser pour plus tard

---

## Sous-score 1 — Valeur apportée (0-100)

« À quel point la présence numérique du resto est en-dessous de ce que MB Studio peut livrer. »

### Bucket `eatbu`

| Composante | Calcul | Poids |
|---|---|---|
| Lenteur site | `(100 − lighthouse_perf)` | 0.30 |
| Mauvais SEO | `(100 − lighthouse_seo)` | 0.25 |
| Mauvaise accessibilité | `(100 − lighthouse_a11y)` | 0.10 |
| Vieillesse du site | `min(âge_site_années × 10, 50)` | 0.15 |
| Fiche GMB pauvre | `(100 − score_gmb_completude)` | 0.20 |

```
valeur = 0.30·(100−perf) + 0.25·(100−seo) + 0.10·(100−a11y)
       + 0.15·min(âge×10,50) + 0.20·(100−gmb)
```

### Bucket `autre-site`

Identique à `eatbu`, puis **pénalité −15 points** (le patron a déjà payé un site, plus dur à déloger) :

```
valeur = [même formule] − 15   (plancher 0)
```

### Bucket `pas-de-site`

Score fixe :

```
valeur = 90
```

(Énorme valeur à apporter par définition : on part de zéro, tout est gain.)

### Score GMB complétude (sous-composante)

Calculé sur la fiche GMB quand accessible (sinon proxy = 50, médian) :

| Critère | Points |
|---|---|
| ≥ 10 photos | +30 |
| 5-9 photos | +15 |
| < 5 photos | +0 |
| Horaires renseignés | +20 |
| Description présente (> 100 car.) | +20 |
| ≥ 2 catégories | +15 |
| Au moins 1 post < 90 jours | +15 |

Total plafonné à 100. `score_gmb_completude` = ce total.

---

## Sous-score 2 — Probabilité d'acceptation (0-100)

« Signaux faibles d'un patron ouvert au numérique et capable de payer 490€. »

Score additif, plancher 0, plafond 100 :

| Signal | Condition | Points |
|---|---|---|
| Note Google | ≥ 4.0 | +25 |
| | 3.5 – 3.99 | +10 |
| | < 3.5 | 0 |
| Nb d'avis | ≥ 100 | +20 |
| | 50 – 99 | +15 |
| | 20 – 49 | +10 |
| | < 20 | +5 |
| Patron répond aux avis | ≥ 30 % des avis ont une réponse propriétaire | +20 |
| | quelques réponses (< 30 %) | +10 |
| | jamais | 0 |
| Fiche GMB complète | photos ≥ 10 ET horaires ET description | +15 |
| Instagram actif | dernier post < 30 jours (si détectable) | +10 |
| Âge site eatbu | ≥ 3 ans (patron lassé, prêt à changer) | +10 |
| Âge site eatbu | < 6 mois (vient d'investir, refusera) | −20 |

```
proba = somme des points applicables
proba = max(0, min(100, proba))
```

---

## Mode dégradé (sans clé Google PageSpeed)

Lighthouse indisponible → `lighthouse_perf`, `lighthouse_seo`, `lighthouse_a11y` = `null`.

**Recalcul de la valeur apportée** en redistribuant les poids des 3 composantes Lighthouse (0.30 + 0.25 + 0.10 = 0.65) sur les 2 composantes restantes, au prorata :

- Vieillesse : poids passe de 0.15 → 0.15 / 0.35 ≈ **0.43**
- GMB pauvre : poids passe de 0.20 → 0.20 / 0.35 ≈ **0.57**

```
valeur_dégradée = 0.43·min(âge×10,50) + 0.57·(100−gmb)
```

(Bucket `pas-de-site` reste à 90, non affecté. Bucket `autre-site` garde la pénalité −15.)

Chaque fiche générée en mode dégradé porte l'encart :
> ⚠️ Score approximatif — vitesse du site non mesurée (clé PageSpeed absente). Configure la clé pour un score précis au prochain run.

---

## Données manquantes — valeurs par défaut

| Donnée absente | Valeur de remplacement | Justification |
|---|---|---|
| `âge_site` (Wayback vide) | 2 ans | Médian observé |
| `score_gmb_completude` (fiche non accessible) | 50 | Médian neutre |
| `note_google` | traiter comme < 3.5 → 0 pt | Conservateur (pas de bonus indu) |
| `nb_avis` | traiter comme < 20 → +5 pt | Conservateur |
| Instagram | non détecté → 0 pt | On ne suppose pas |

Une fiche avec beaucoup de valeurs par défaut porte une mention « données partielles » pour que Mike sache que le score est moins fiable.

---

## Exemple de calcul (bucket eatbu, mode normal)

Resto fictif : eatbu, perf=35, seo=48, a11y=70, âge=4 ans, gmb_completude=40, note=4.3, avis=82, répond rarement aux avis, GMB incomplète, Insta inconnu.

**Valeur apportée :**
```
= 0.30·(100−35) + 0.25·(100−48) + 0.10·(100−70) + 0.15·min(40,50) + 0.20·(100−40)
= 0.30·65 + 0.25·52 + 0.10·30 + 0.15·40 + 0.20·60
= 19.5 + 13 + 3 + 6 + 12
= 53.5
```

**Probabilité acceptation :**
```
note 4.3 ≥ 4.0          → +25
avis 82 (50-99)         → +15
répond rarement         → +10
GMB incomplète          → +0
Insta inconnu           → +0
âge eatbu 4 ans ≥ 3     → +10
= 60
```

**Score total :**
```
0.5·53.5 + 0.5·60 = 26.75 + 30 = 56.75 → arrondi 57 → Tier B
```
