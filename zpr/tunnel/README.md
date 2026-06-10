# Tunnel de prospection — pilotage de l'objectif

Le moteur ZPR (`../run_zpr.py`) dit **où** prospecter. Ce tunnel dit **où tu en es**
et **combien de contacts il te reste à produire** pour tenir l'objectif :
**100 000 € de CA et 10 mandats exclusifs en 6 mois** (Étapes 4 & 5 de la méthode).

Ratio de performance de référence : **30 contacts → 5 qualifiés → 2 estimations → 1 mandat**.

## Utilisation

```bash
$EDITOR zpr/tunnel/pipeline.yml      # ta liste de prospects + ton objectif
python zpr/tunnel/run_tunnel.py      # génère le tableau de bord
```

`pipeline.yml` est la **source de vérité** (saisie manuelle). Le script en dérive :

| Sortie | Contenu |
|---|---|
| `{date}/tableau-de-bord.md` `.txt` | Objectif, entonnoir réel vs cible, CA signé + pondéré, **projection à l'échéance**, **volume de contacts à produire** + cadence hebdo, sources & signaux 3D, contrôle conformité |
| `{date}/pipeline.csv` | Vue plate 1 ligne/prospect (Google Sheets) |

## Ce que le tableau de bord calcule

- **Entonnoir cumulatif** par étape et **taux de conversion réels vs cibles**.
- **CA signé** (mandats fermes) et **CA pondéré du pipeline** (chaque prospect ×
  sa probabilité cible d'aller au mandat × honoraires moyens).
- **Projection** : run-rate de mandats/mois → mandats projetés à l'échéance, écart,
  sur/sous trajectoire.
- **Volume à produire** : pour les mandats restants, combien de contacts / qualifiés /
  estimations, et la **cadence hebdomadaire** nécessaire. Tant qu'il y a moins d'un
  cycle complet (30 contacts), on s'appuie sur les **taux cibles** de la méthode
  plutôt que d'extrapoler un échantillon trop maigre.
- **Conformité Bloctel/RGPD** : à partir du **11 août 2026**, signale les prospects
  qu'on ne peut plus appeler à froid (ni consentement, ni contrat en cours).

## Statuts d'un prospect

`contact → qualifie → estimation → mandat` (ou `perdu`). Pour un `perdu`, renseigne
`stade_atteint` pour qu'il compte dans l'entonnoir jusqu'où il était monté.

Discipline (comme tout le repo) : **aucun chiffre inventé**. Sans honoraires saisis,
on retombe sur les honoraires moyens (`ca_cible / mandats_cibles`), signalé comme hypothèse.
Dépendance unique : PyYAML (cf `../requirements.txt`). Tests : `python zpr/tunnel/tests/run_tests.py`.
