#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MB Studio Tunnel - Test d'un agent isolé (v2)

Nouveauté v2 : pour Agent 2 et Agent 3, le script charge automatiquement
les outputs des agents précédents (s'ils existent) en plus du fichier
agent-N-input.md, et les passe à l'agent comme contexte.

Usage:
    cd C:\\Users\\PC\\mb-studio\\tunnel

    # Test Agent 1 sur Al Badea
    python scripts/run_agent.py 1 al-badea

    # Test Agent 2 (charge auto l'output Agent 1)
    python scripts/run_agent.py 2 al-badea

    # Test Agent 3 (charge auto les outputs Agent 1 et 2)
    python scripts/run_agent.py 3 al-badea

    # Liste des inputs de test disponibles
    python scripts/run_agent.py list
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Couleurs ANSI
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    END = '\033[0m'

def header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}\n")

def success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def error(text):
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def info(text):
    print(f"{Colors.BLUE}→ {text}{Colors.END}")

def dim(text):
    print(f"{Colors.DIM}{text}{Colors.END}")

def warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")


# Détection des chemins du projet
SCRIPT_DIR = Path(__file__).parent
TUNNEL_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = TUNNEL_DIR.parent

DOCTRINE_DIR = TUNNEL_DIR / 'doctrine'
AGENTS_DIR = TUNNEL_DIR / 'agents'
TESTS_DIR = TUNNEL_DIR / 'tests'
TESTS_INPUTS_DIR = TESTS_DIR / 'inputs'
TESTS_OUTPUTS_DIR = TESTS_DIR / 'outputs'


def load_doctrine():
    """Charge tous les fichiers de doctrine pour les injecter dans le system prompt."""
    doctrine_files = sorted(DOCTRINE_DIR.glob('*.md'))
    if not doctrine_files:
        error(f"Aucun fichier doctrine trouvé dans {DOCTRINE_DIR}")
        sys.exit(1)

    doctrine_content = []
    for f in doctrine_files:
        doctrine_content.append(f"\n\n### Document : {f.name}\n\n")
        doctrine_content.append(f.read_text(encoding='utf-8'))

    return ''.join(doctrine_content)


def load_agent_prompt(agent_number):
    """Charge le system prompt d'un agent (1, 2 ou 3)."""
    agent_files = {
        1: AGENTS_DIR / 'agent-1-fiche-restaurant.md',
        2: AGENTS_DIR / 'agent-2-copywriting.md',
        3: AGENTS_DIR / 'agent-3-prompt-stitch.md',
    }

    agent_file = agent_files.get(agent_number)
    if not agent_file:
        error(f"Numéro d'agent invalide : {agent_number} (attendu : 1, 2 ou 3)")
        sys.exit(1)

    if not agent_file.exists():
        error(f"Fichier agent introuvable : {agent_file}")
        info(f"Vérifie que {agent_file.name} est bien dans tunnel/agents/")
        sys.exit(1)

    return agent_file.read_text(encoding='utf-8')


def load_previous_outputs(client_slug, current_agent):
    """
    Charge automatiquement les outputs des agents précédents.

    Pour Agent 2 : charge l'output d'Agent 1
    Pour Agent 3 : charge les outputs d'Agent 1 et Agent 2
    Pour Agent 1 : retourne une chaîne vide
    """
    if current_agent == 1:
        return ""

    outputs_content = []
    client_outputs_dir = TESTS_OUTPUTS_DIR / client_slug

    for prev_agent in range(1, current_agent):
        prev_output_file = client_outputs_dir / f'agent-{prev_agent}.md'

        if not prev_output_file.exists():
            error(f"Output Agent {prev_agent} introuvable : {prev_output_file}")
            error(f"Tu dois d'abord lancer Agent {prev_agent} avant Agent {current_agent}.")
            info(f"Commande : python scripts/run_agent.py {prev_agent} {client_slug}")
            sys.exit(1)

        content = prev_output_file.read_text(encoding='utf-8')
        outputs_content.append(
            f"\n\n========== OUTPUT AGENT {prev_agent} (déjà validé) ==========\n\n"
            f"{content}\n"
        )
        size_kb = len(content) / 1024
        success(f"Output Agent {prev_agent} chargé ({size_kb:.1f} Ko)")

    return ''.join(outputs_content)


def load_test_input(client_slug, agent_number):
    """Charge l'input de test pour un client donné."""
    input_file = TESTS_INPUTS_DIR / client_slug / f'agent-{agent_number}-input.md'

    if not input_file.exists():
        error(f"Input de test introuvable : {input_file}")
        info(f"Crée le fichier avec les données nécessaires (voir tests/README.md)")
        sys.exit(1)

    return input_file.read_text(encoding='utf-8')


def call_anthropic_api(system_prompt, user_message, model, max_tokens):
    """Effectue l'appel API Anthropic."""
    from anthropic import Anthropic

    client = Anthropic()  # utilise ANTHROPIC_API_KEY de .env automatiquement

    info(f"Modèle : {model}")
    info(f"Max tokens output : {max_tokens}")
    info("Appel API en cours... (peut prendre 30-90s)")

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": user_message
        }]
    )

    return response


def save_output(client_slug, agent_number, content):
    """Sauvegarde l'output dans tests/outputs/[client]/agent-N.md"""
    client_dir = TESTS_OUTPUTS_DIR / client_slug
    client_dir.mkdir(parents=True, exist_ok=True)

    output_file = client_dir / f'agent-{agent_number}.md'
    output_file.write_text(content, encoding='utf-8')

    return output_file


def list_test_inputs():
    """Liste les clients de test disponibles."""
    header("INPUTS DE TEST DISPONIBLES")

    if not TESTS_INPUTS_DIR.exists():
        info(f"Dossier {TESTS_INPUTS_DIR} n'existe pas encore.")
        return

    clients = sorted([d for d in TESTS_INPUTS_DIR.iterdir() if d.is_dir()])

    if not clients:
        info("Aucun client de test disponible.")
        return

    for client_dir in clients:
        print(f"\n{Colors.BOLD}{client_dir.name}{Colors.END}")
        inputs = sorted(client_dir.glob('agent-*-input.md'))
        if inputs:
            for inp in inputs:
                size_kb = inp.stat().st_size / 1024
                print(f"  {Colors.GREEN}✓{Colors.END} {inp.name} ({size_kb:.1f} Ko)")
        else:
            print(f"  {Colors.RED}✗{Colors.END} Aucun input")

        output_dir = TESTS_OUTPUTS_DIR / client_dir.name
        if output_dir.exists():
            outputs = sorted(output_dir.glob('agent-*.md'))
            if outputs:
                print(f"  {Colors.DIM}Outputs existants :{Colors.END}")
                for out in outputs:
                    size_kb = out.stat().st_size / 1024
                    print(f"    {Colors.CYAN}→{Colors.END} {out.name} ({size_kb:.1f} Ko)")


def run_agent(agent_number, client_slug, model='claude-sonnet-4-6', max_tokens=8000):
    """Lance un agent sur un client de test."""
    header(f"AGENT {agent_number} — Client : {client_slug}")

    # 1. Charger la doctrine
    info("Chargement de la doctrine MB Studio...")
    doctrine = load_doctrine()
    success(f"Doctrine chargée ({len(doctrine)} caractères)")

    # 2. Charger le prompt de l'agent
    info(f"Chargement du system prompt Agent {agent_number}...")
    agent_prompt = load_agent_prompt(agent_number)
    success(f"Agent {agent_number} chargé ({len(agent_prompt)} caractères)")

    # 3. Charger les outputs précédents (Agent 2 et 3 uniquement)
    previous_outputs = ""
    if agent_number > 1:
        info(f"Chargement des outputs des agents précédents...")
        previous_outputs = load_previous_outputs(client_slug, agent_number)

    # 4. Charger l'input de test
    info(f"Chargement de l'input pour {client_slug}...")
    user_input = load_test_input(client_slug, agent_number)
    success(f"Input chargé ({len(user_input)} caractères)")

    # 5. Construire le user_message complet (outputs précédents + input)
    if previous_outputs:
        user_message = (
            f"{previous_outputs}\n\n"
            f"========== INPUT POUR TON TRAVAIL (Agent {agent_number}) ==========\n\n"
            f"{user_input}"
        )
    else:
        user_message = user_input

    info(f"User message total : {len(user_message)} caractères")

    # 6. Construire le system prompt complet (doctrine + agent)
    system_prompt = f"""Tu es un agent spécialisé du tunnel MB Studio.

# DOCTRINE MB STUDIO (référence absolue)

{doctrine}

---

# TES INSTRUCTIONS SPÉCIFIQUES (Agent {agent_number})

{agent_prompt}

---

Applique strictement ta doctrine et tes instructions pour le client suivant."""

    info(f"System prompt total : {len(system_prompt)} caractères (~{len(system_prompt)//4} tokens estimés)")

    # 7. Appel API
    response = call_anthropic_api(system_prompt, user_message, model, max_tokens)

    # 8. Extraction du contenu
    output_text = response.content[0].text

    success(f"Réponse reçue ({len(output_text)} caractères)")
    info(f"Tokens utilisés : {response.usage.input_tokens} input + {response.usage.output_tokens} output")

    # Coût
    if 'sonnet' in model.lower():
        cost_usd = (response.usage.input_tokens * 3 + response.usage.output_tokens * 15) / 1_000_000
    elif 'opus' in model.lower():
        cost_usd = (response.usage.input_tokens * 15 + response.usage.output_tokens * 75) / 1_000_000
    else:
        cost_usd = 0

    info(f"Coût de cet appel : ${cost_usd:.4f} (~{cost_usd * 0.92:.4f}€)")

    # 9. Sauvegarde
    output_file = save_output(client_slug, agent_number, output_text)
    success(f"Output sauvegardé : {output_file}")

    # 10. Aperçu de l'output
    header("APERÇU DE L'OUTPUT (200 premières lignes)")
    lines = output_text.split('\n')
    preview = '\n'.join(lines[:200])
    print(preview)

    if len(lines) > 200:
        print(f"\n{Colors.DIM}... ({len(lines) - 200} lignes supplémentaires){Colors.END}")
        info(f"Output complet dans : {output_file}")

    header("TERMINÉ")

    # 11. Suggestion pour l'agent suivant
    if agent_number < 3:
        next_agent = agent_number + 1
        next_input = TESTS_INPUTS_DIR / client_slug / f'agent-{next_agent}-input.md'

        print(f"\n{Colors.CYAN}→ Pour valider l'output ci-dessus, ouvre :")
        print(f"  {output_file}{Colors.END}")

        if next_input.exists():
            print(f"\n{Colors.CYAN}→ Si l'output est OK, lance l'agent suivant :")
            print(f"  python scripts/run_agent.py {next_agent} {client_slug}{Colors.END}\n")
        else:
            warning(f"Avant de lancer Agent {next_agent}, crée l'input :")
            print(f"  {next_input}")


def main():
    # Charger les variables d'environnement
    from dotenv import load_dotenv
    env_path = TUNNEL_DIR / '.env'
    load_dotenv(env_path)

    parser = argparse.ArgumentParser(
        description='Lance un agent MB Studio isolément pour test',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('command', help='Numéro agent (1, 2, 3) ou "list"')
    parser.add_argument('client', nargs='?', help='Slug du client de test (ex: al-badea)')
    parser.add_argument('--model', default=None, help='Override modèle (défaut depuis .env)')
    parser.add_argument('--max-tokens', type=int, default=8000, help='Tokens max output (défaut 8000)')

    args = parser.parse_args()

    if args.command == 'list':
        list_test_inputs()
        return

    try:
        agent_number = int(args.command)
    except ValueError:
        error(f"Première argument invalide : '{args.command}'. Attendu : 1, 2, 3 ou 'list'")
        parser.print_help()
        sys.exit(1)

    if agent_number not in [1, 2, 3]:
        error(f"Numéro agent doit être 1, 2 ou 3. Reçu : {agent_number}")
        sys.exit(1)

    if not args.client:
        error("Slug du client manquant.")
        info("Usage : python scripts/run_agent.py <agent-number> <client-slug>")
        sys.exit(1)

    model = args.model or os.getenv('ANTHROPIC_MODEL', 'claude-sonnet-4-6')

    try:
        run_agent(agent_number, args.client, model, args.max_tokens)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Interrompu par l'utilisateur{Colors.END}")
        sys.exit(130)
    except Exception as e:
        error(f"Erreur : {type(e).__name__}")
        error(f"Message : {str(e)}")
        if 'authentication' in str(e).lower() or '401' in str(e):
            info("→ Vérifie ta clé API dans .env")
        elif 'rate_limit' in str(e).lower():
            info("→ Limite de requêtes atteinte, attends 1 min")
        elif 'credit' in str(e).lower() or 'quota' in str(e).lower():
            info("→ Crédit API épuisé, recharge sur console.anthropic.com")
        sys.exit(1)


if __name__ == "__main__":
    main()
