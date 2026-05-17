# Liste prospects — la mémoire centrale de MB Studio

C'est **ta plus grande ressource commerciale**. Pas une liste figée : une base qui
grossit et s'enrichit toute seule au fil des scans, des visites et des outils.

## La règle (non négociable)

**Une seule source de vérité : `restaurants.yml`.** Tout le reste est régénéré à partir
de lui — on ne maintient jamais deux listes à la main qui finissent par diverger.

| Fichier | C'est quoi | Qui écrit dedans |
|---|---|---|
| `restaurants.yml` | La base vivante, complète, enrichie dans le temps | `scoring-prospects` (scan), `pilote-client` (déroulé commercial), toi (notes) |
| `restaurants.csv` | **Vue plate, claire, 1 ligne par resto** — à déposer dans un outil d'infographie ou Google Sheets | Régénéré automatiquement. **Ne pas éditer à la main.** |
| `{ville}-{date}/` | Photo d'une campagne de prospection à un instant T (listes triées + fiches à pitcher) | Régénéré par `scoring-prospects`. Dérivé, jamais la source. |
| `cache/` | Caches techniques des API (Overpass, Lighthouse, Wayback) | Outils. À ignorer. |

## Comment ça s'enrichit (les 2 leviers)

1. **Le scan** (`scoring-prospects`) remplit/met à jour les blocs `scan` et `scoring`.
2. **Le tunnel** (`pilote-client`) réécrit le bloc `tunnel` à chaque étape vécue
   (maquette vue, objection entendue, délai réel, ce qui a fait signer ou perdre).
   → Plus on fait de clients, plus les scores, les arguments et les délais s'affinent
   tout seuls. Le tunnel n'est jamais "fini", il se bonifie.

Tes notes manuelles (`notes_mike`) et tes corrections de score (`scoring.mike_override`)
sont **toujours préservées** : aucun outil ne les écrase.

## Confidentialité

Ces données agrègent du public d'une façon qui pourrait être mal perçue par un patron
qui découvrirait son propre fichier. **Ne jamais publier hors du repo MB Studio.**
Aucun email/téléphone collecté en masse : ces fiches servent à des visites en personne.
