# MB Studio Tunnel

Système de production de sites web pour restaurants TPE.

## Vue d'ensemble

Le tunnel orchestre 3 agents IA spécialisés (fiche restaurant → copywriting → prompt Stitch) pour produire des sites web sur-mesure, mobile-first, à des restaurants locaux.

Chaque site produit est **unique** : pas de template visuel partagé, direction artistique pensée pour chaque lieu.

## Architecture

```
tunnel/
├── doctrine/              # Le savoir codifié MB Studio (vision, méthode, anti-jumeau)
├── agents/                # Les 3 system prompts des agents IA
├── scripts/               # Le code Python du CLI
├── prospects-outputs/     # Outputs des sites en cours de production
│   └── _template/         # Squelette à dupliquer pour chaque nouveau client
├── exemples/              # Sites de référence (Al Badea, Anamour, Casa Tropical)
├── registre/              # Registre anti-jumeau (combinaisons utilisées)
├── .env                   # Configuration locale (clé API, etc.) — JAMAIS commité
├── .env.example           # Template de configuration
├── .gitignore             # Exclusions Git
├── requirements.txt       # Dépendances Python
├── CLAUDE.md              # Instructions pour Claude Code
└── README.md              # Ce fichier
```

## Installation

### Prérequis

- Python 3.13+
- pip (livré avec Python)
- Clé API Anthropic ([console.anthropic.com](https://console.anthropic.com))
- Compte Stitch ([stitch.withgoogle.com](https://stitch.withgoogle.com))

### Étapes

1. **Cloner le repo** (déjà fait)

2. **Installer les dépendances Python** :

```powershell
cd C:\Users\PC\mb-studio\tunnel
pip install -r requirements.txt
```

3. **Configurer les clés API** :

```powershell
copy .env.example .env
```

Puis ouvre `.env` et remplace `sk-ant-api03-REMPLACE_PAR_TA_VRAIE_CLE` par ta vraie clé API Anthropic.

4. **Tester la connexion API** :

```powershell
python scripts/test_api.py
```

Si tout marche, tu verras un message de validation. Sinon, vérifie ta clé API.

## Usage (à venir en Session 3)

Le CLI principal sera utilisable ainsi :

```powershell
# Nouveau client
python scripts/mb_studio.py new-client "Al Badea" "Chartres"

# Vérifier l'unicité d'une combinaison (anti-jumeau)
python scripts/mb_studio.py check-unicite

# Lister les clients en cours
python scripts/mb_studio.py list-clients
```

Pour l'instant (Session 1), seul `test_api.py` est disponible.

## Doctrine

Avant toute utilisation, lire impérativement :

- `doctrine/00-vision-mb-studio.md` (5 min)
- `doctrine/01-methode-emotionnelle.md` (10 min)
- `doctrine/04-workflow-orchestration.md` (10 min)

Ces 3 documents = 25 minutes pour comprendre le projet.

## Coûts estimés

| Élément | Coût |
|---|---|
| Clé API Anthropic | Selon usage (~0,22€ / site avec Sonnet 4.6) |
| Stitch | Gratuit (forfait gratuit suffisant pour démarrer) |
| Cloudflare Pages | Gratuit (illimité) |
| GitHub privé | Gratuit |

**Budget mensuel API estimé** : 5-15€ pour 10-30 sites/mois.

## Sécurité

- **Ne jamais commit le fichier `.env`** (protégé par `.gitignore`)
- **Ne jamais partager la clé API** dans une conversation publique
- **Renouveler la clé** si elle est exposée par erreur

## Évolutions prévues

- [x] Session 1 — Fondations du repo (CE QUE TU LIS ACTUELLEMENT)
- [ ] Session 2 — Les 3 agents IA formalisés
- [ ] Session 3 — Script CLI Python d'orchestration
- [ ] Session 4 — Registre anti-jumeau + exemples concrets

## Support

Maintenu par Mike (Mouaad).
Pour toute question : voir `CLAUDE.md` pour les instructions à Claude Code.
