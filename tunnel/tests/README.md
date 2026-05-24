# Dossier tests/

Ce dossier contient les inputs et outputs pour tester les agents MB Studio isolément.

## Structure

```
tests/
├── inputs/                       # Inputs de test pour chaque client
│   └── [client-slug]/
│       ├── agent-1-input.md     # Données brutes pour Agent 1
│       ├── agent-2-input.md     # Inputs Agent 2 (optionnel)
│       └── agent-3-input.md     # Inputs Agent 3 (optionnel)
│
└── outputs/                      # Sorties générées par les agents
    └── [client-slug]/
        ├── agent-1.md           # Fiche restaurant + fiche d'âme
        ├── agent-2.md           # YAML copywriting
        └── agent-3.md           # Prompt Stitch
```

## Usage

### Lister les clients de test disponibles

```powershell
python scripts/run_agent.py list
```

### Lancer un agent

```powershell
# Agent 1 sur Al Badea
python scripts/run_agent.py 1 al-badea

# Agent 2 (utilise l'output Agent 1 précédent automatiquement)
python scripts/run_agent.py 2 al-badea

# Agent 3 (utilise les outputs précédents)
python scripts/run_agent.py 3 al-badea
```

### Avec un modèle différent

```powershell
python scripts/run_agent.py 1 al-badea --model claude-opus-4-7
python scripts/run_agent.py 1 al-badea --max-tokens 12000
```

## Créer un nouveau client de test

1. Crée le dossier : `mkdir tests\inputs\nom-client`
2. Crée `agent-1-input.md` avec le payload YAML structuré
3. Lance : `python scripts/run_agent.py 1 nom-client`

## Coûts indicatifs (Sonnet 4.6)

| Agent | Input tokens | Output tokens | Coût estimé |
|---|---|---|---|
| Agent 1 | ~25 000 | ~3 000 | ~0,12€ |
| Agent 2 | ~30 000 | ~4 000 | ~0,15€ |
| Agent 3 | ~35 000 | ~5 000 | ~0,18€ |
| **Total tunnel** | | | **~0,45€/site** |

Pour un test isolé d'un agent, c'est généralement entre 0,10€ et 0,20€.
