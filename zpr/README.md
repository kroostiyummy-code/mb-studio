# ZPR — Moteur de Zone de Prospection Rentable

Outil de **prospection immobilière ciblée** (Étapes 1 & 2 de la Stratégie ZPR) :
il décide, chiffres à l'appui, **où prospecter** et **où ne jamais aller**.

> *« La performance immobilière n'est pas une affaire de talent, mais de discipline
> mathématique appliquée à un territoire. »*

Même philosophie que `prospects/` (la prospection commerçants de MB Studio) :
une **seule source de vérité** (`zones.yml`), des vues régénérées, et la règle d'or
**jamais de chiffre inventé** — une donnée manquante reste manquante.

## Ce que l'outil calcule

Pour chaque commune candidate, en croisant des données **open data** :

| Indicateur | Source | À quoi ça sert |
|---|---|---|
| **Taux de rotation** `τ_R = (mutations an. moy. / nb logements) × 100` | DVF (mutations) + INSEE (logements) | **Le verdict.** ≥ 4,0 % = GO, sinon NO-GO. |
| **Segment dominant** (« Maison < 90 m² », « Appartement T1-T2 »…) | DVF | Sur quoi se spécialiser. |
| **Gisement passoires F/G** | DPE / ADEME | Bailleurs découragés = transactions opportunistes. |
| **DPE récents (< 90 j)** | DPE / ADEME | Signal **pré-marché** : un DPE précède l'annonce. |
| **% propriétaires occupants, revenu médian, % 60 ans+** | INSEE / Filosofi | Leviers des **« 3D »** (Divorce, Décès, Déménagement). |
| **Score d'opportunité** (0-100) | composite | Classe les communes **GO** entre elles. |

Le **verdict reste binaire sur la rotation** (seuil critique 4,0 %, moyenne nationale ≈ 2,5 %).
Le score d'opportunité ne sert qu'à **ordonner** les communes déjà au-dessus du seuil.

Exclusions de la méthode déjà appliquées : **garages / box** sont hors du numérateur
(honoraires trop faibles). Les **copropriétés dégradées** ne sont pas détectables en DVF —
à écarter à la main (champ `notes`).

## Utilisation

```bash
# 1. Éditer la liste des communes à comparer
$EDITOR zpr/zones.yml          # une entrée par commune, code_insee obligatoire

# 2. Lancer l'analyse (nécessite curl + un réseau ouvert sur les API ci-dessous)
python zpr/run_zpr.py

# Options (variables d'environnement)
ZPR_CAMPAGNE=2026-06-10 \      # date de campagne (défaut : aujourd'hui)
ZPR_ANNEES=5 \                 # fenêtre DVF en années pleines (défaut : 5)
python zpr/run_zpr.py
```

### Sorties générées

| Fichier | Contenu | Édition |
|---|---|---|
| `zones.yml` | **Source de vérité** : communes + saisie INSEE + résultats | À la main (entrées + `insee_filosofi` + `notes`) |
| `{date}/comparatif-villes.md` `.txt` | Tableau de décision + fiches par commune | Régénéré, ne pas éditer |
| `{date}/zones.csv` | Vue plate 1 ligne/commune (Google Sheets) | Régénéré, ne pas éditer |
| `cache/` | Caches API (gitignored) | Ignorer |

## Et après ? Le tunnel de conversion

Le moteur ZPR dit **où** prospecter. Pour piloter ensuite l'activité vers l'objectif
(100 000 € / 10 mandats en 6 mois) avec le ratio 30 → 5 → 2 → 1, voir
[`tunnel/`](tunnel/README.md) : entonnoir réel vs cible, projection à l'échéance,
volume de contacts à produire, et contrôle de conformité Bloctel/RGPD.

## Le dénominateur (à renseigner à la main)

`τ_R` a besoin du **nombre total de logements** de la commune. Ce chiffre officiel
ne s'expose pas en API sans clé ; renseigne-le dans `zones.yml` :

> INSEE → [Dossier complet](https://www.insee.fr/fr/statistiques) → ta commune →
> *Logement* → **« Nombre total de logements »** → `insee_filosofi.nb_logements`.

Mêmes onglets pour `part_proprietaires_occ`, `revenu_median`, `part_60_ans_plus`.

À défaut de chiffre saisi, l'outil dérive une **estimation** `population / 2,2`
**explicitement taggée `[ESTIMÉ]`** : utile pour dégrossir, à remplacer par le vrai
chiffre INSEE avant toute décision d'implantation. Aucune estimation n'est jamais
présentée comme une donnée réelle.

## Sources open data (aucune clé requise)

- **DVF** (mutations) — `files.data.gouv.fr/geo-dvf/latest/csv/{année}/communes/{dep}/{insee}.csv`
- **DPE** (ADEME) — `data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines`
- **Communes** (population, centre) — `geo.api.gouv.fr/communes/{insee}`
- **Logements + sociodémo** — INSEE *Dossier complet* / Filosofi (saisie manuelle)

> **Réseau (Claude Code on the web).** L'environnement d'exécution distant filtre le
> réseau sortant. Ces hôtes doivent être **autorisés par la politique réseau** de
> l'environnement, sinon les appels échouent et tout reste `INDÉTERMINÉ`. À lancer
> de préférence en **local**, ou avec une politique réseau ouverte sur ces domaines.
> Cf. https://code.claude.com/docs/en/claude-code-on-the-web

## Tests

```bash
python zpr/tests/run_tests.py     # valide la logique de calcul hors-ligne (fixtures)
```

Couvre : dédup des mutations, exclusion garages/box, segment dominant, formule `τ_R`,
verdict au seuil, score borné/neutre, codes département (Corse 2A/2B, DOM 97x).

## Conformité (rappel)

Dès le **11 août 2026**, démarchage téléphonique non sollicité interdit sans
consentement explicite ou contrat en cours. Privilégier l'**inbound** et la
recommandation ; emailing sur consentement RGPD ; SMS ultra-local sur opt-in.
Comme `prospects/`, ces données agrègent du public : **ne pas publier hors du repo.**
