#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MB Studio Tunnel - Test de connexion API Anthropic

Ce script vérifie que :
1. Le fichier .env est correctement configuré
2. La clé API Anthropic est valide
3. Le modèle Claude Sonnet 4.6 répond correctement
4. Les dépendances Python sont installées

Usage :
    cd C:\\Users\\PC\\mb-studio\\tunnel
    python scripts/test_api.py

Coût du test : ~0,01€ (un seul appel API léger)
"""

import os
import sys
from pathlib import Path

# Couleurs ANSI pour l'affichage terminal (compatible Windows 10+)
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}→ {text}{Colors.END}")


def test_imports():
    """Étape 1 : Vérifie que les dépendances Python sont installées."""
    print_header("ÉTAPE 1/4 : Vérification des dépendances Python")

    required_modules = {
        'anthropic': 'anthropic',
        'dotenv': 'python-dotenv',
        'yaml': 'pyyaml',
    }

    missing = []
    for module, package in required_modules.items():
        try:
            __import__(module)
            print_success(f"Module '{module}' installé")
        except ImportError:
            print_error(f"Module '{module}' manquant (package: {package})")
            missing.append(package)

    if missing:
        print()
        print_error(f"Dépendances manquantes : {', '.join(missing)}")
        print_info(f"Lance cette commande pour les installer :")
        print(f"\n  pip install {' '.join(missing)}\n")
        sys.exit(1)

    print_success("Toutes les dépendances sont OK")


def test_env_file():
    """Étape 2 : Vérifie que .env existe et contient la clé API."""
    print_header("ÉTAPE 2/4 : Vérification du fichier .env")

    # Détecter le chemin du .env (dans tunnel/, pas dans scripts/)
    script_dir = Path(__file__).parent
    tunnel_dir = script_dir.parent
    env_path = tunnel_dir / '.env'

    if not env_path.exists():
        print_error(f"Fichier .env introuvable à {env_path}")
        print_info("Étapes pour le créer :")
        print(f"  1. cd {tunnel_dir}")
        print(f"  2. copy .env.example .env")
        print(f"  3. Ouvre .env et remplace la clé par ta vraie clé API")
        sys.exit(1)

    print_success(f"Fichier .env trouvé : {env_path}")

    # Charger les variables d'environnement
    from dotenv import load_dotenv
    load_dotenv(env_path)

    # Vérifier la clé API
    api_key = os.getenv('ANTHROPIC_API_KEY', '')

    if not api_key:
        print_error("Variable ANTHROPIC_API_KEY non définie dans .env")
        sys.exit(1)

    if api_key == 'sk-ant-api03-REMPLACE_PAR_TA_VRAIE_CLE':
        print_error("La clé API n'a pas été remplacée par ta vraie clé")
        print_info("Ouvre le fichier .env et remplace la valeur par ta clé API")
        sys.exit(1)

    if not api_key.startswith('sk-ant-api03-'):
        print_warning(f"La clé ne commence pas par 'sk-ant-api03-' (format inattendu)")
        print_info(f"Premiers caractères : {api_key[:15]}...")

    # Afficher partiellement la clé (sécurité)
    key_preview = api_key[:15] + '...' + api_key[-4:]
    print_success(f"Clé API détectée : {key_preview}")

    # Vérifier le modèle
    model = os.getenv('ANTHROPIC_MODEL', 'claude-sonnet-4-6')
    print_success(f"Modèle configuré : {model}")

    return api_key, model


def test_api_call(api_key, model):
    """Étape 3 : Effectue un appel API minimal pour valider la connexion."""
    print_header("ÉTAPE 3/4 : Test d'appel API Anthropic")

    print_info("Envoi d'un message test à Claude...")
    print_info(f"Modèle : {model}")

    try:
        from anthropic import Anthropic

        client = Anthropic(api_key=api_key)

        response = client.messages.create(
            model=model,
            max_tokens=100,
            messages=[{
                "role": "user",
                "content": "Réponds uniquement par ces 3 mots exacts : 'MB Studio opérationnel'"
            }]
        )

        # Extraire le texte de la réponse
        reply_text = response.content[0].text.strip()

        print_success(f"Réponse reçue : '{reply_text}'")

        # Afficher les tokens utilisés
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        print_info(f"Tokens utilisés : {input_tokens} input + {output_tokens} output")

        # Estimer le coût
        if 'sonnet' in model.lower():
            cost_usd = (input_tokens * 3 + output_tokens * 15) / 1_000_000
        elif 'opus' in model.lower():
            cost_usd = (input_tokens * 15 + output_tokens * 75) / 1_000_000
        else:
            cost_usd = 0

        cost_eur = cost_usd * 0.92  # Approximation USD → EUR
        print_info(f"Coût estimé de ce test : ${cost_usd:.6f} (~{cost_eur:.6f}€)")

        return True

    except Exception as e:
        print_error(f"Erreur lors de l'appel API : {type(e).__name__}")
        print_error(f"Message : {str(e)}")

        # Messages d'aide selon l'erreur
        error_str = str(e).lower()
        if 'authentication' in error_str or 'invalid' in error_str or '401' in error_str:
            print_warning("\nProblème probable : clé API invalide ou révoquée")
            print_info("Solutions :")
            print("  1. Vérifie que la clé API dans .env est exacte (pas d'espaces)")
            print("  2. Vérifie sur console.anthropic.com que la clé est active")
            print("  3. Vérifie que tu as bien des crédits (Plans & Billing)")
        elif 'rate_limit' in error_str or '429' in error_str:
            print_warning("\nProblème probable : limite de requêtes atteinte")
            print_info("Solution : attends 1 minute et relance")
        elif 'quota' in error_str or 'credit' in error_str:
            print_warning("\nProblème probable : crédit API épuisé")
            print_info("Solution : recharge sur console.anthropic.com → Plans & Billing")
        elif 'model' in error_str:
            print_warning(f"\nProblème probable : modèle '{model}' indisponible")
            print_info("Solutions :")
            print("  1. Vérifie l'orthographe du modèle dans .env")
            print("  2. Essaie avec 'claude-sonnet-4-5' temporairement")

        return False


def test_doctrine_files():
    """Étape 4 : Vérifie que la doctrine est bien en place."""
    print_header("ÉTAPE 4/4 : Vérification de la doctrine")

    script_dir = Path(__file__).parent
    tunnel_dir = script_dir.parent
    doctrine_dir = tunnel_dir / 'doctrine'

    expected_files = [
        '00-vision-mb-studio.md',
        '01-methode-emotionnelle.md',
        '02-anti-jumeau-da.md',
        '03-references-cinematique.md',
        '04-workflow-orchestration.md',
    ]

    if not doctrine_dir.exists():
        print_error(f"Dossier doctrine/ introuvable : {doctrine_dir}")
        print_info("Copie les 5 fichiers MD de doctrine dans ce dossier")
        return False

    missing = []
    for filename in expected_files:
        filepath = doctrine_dir / filename
        if filepath.exists():
            size_kb = filepath.stat().st_size / 1024
            print_success(f"{filename} ({size_kb:.1f} Ko)")
        else:
            print_error(f"{filename} MANQUANT")
            missing.append(filename)

    if missing:
        print()
        print_warning(f"Fichiers manquants : {len(missing)}/{len(expected_files)}")
        print_info("Copie les fichiers manquants dans tunnel/doctrine/")
        return False

    print_success(f"Tous les fichiers doctrine ({len(expected_files)}) sont en place")
    return True


def main():
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║       MB STUDIO TUNNEL - Test de configuration API        ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")

    # Exécuter les 4 étapes
    test_imports()
    api_key, model = test_env_file()
    api_ok = test_api_call(api_key, model)
    doctrine_ok = test_doctrine_files()

    # Bilan final
    print_header("BILAN FINAL")

    if api_ok and doctrine_ok:
        print_success("Configuration complète et opérationnelle !")
        print()
        print_info("Tu peux maintenant :")
        print("  1. Continuer avec Session 2 (création des 3 agents IA)")
        print("  2. Tester un premier appel des agents (à venir)")
        print()
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 MB Studio Tunnel est prêt.{Colors.END}\n")
        sys.exit(0)
    else:
        print_warning("Configuration partiellement OK — voir les erreurs ci-dessus")
        if not api_ok:
            print_error("API : NON FONCTIONNELLE")
        if not doctrine_ok:
            print_error("Doctrine : INCOMPLÈTE")
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()
