#!/usr/bin/env python3
"""
Script de verificação da configuração do projeto BOH!
"""
import os
import json
from pathlib import Path


def check_project_structure():
    """Verifica se a estrutura do projeto está correta"""
    print("Verificando estrutura do projeto...")

    required_files = [
        ".github/workflows/deploy.yaml",
        "vercel.json",
        "api/wsgi.py",
        "build_github_pages.py",
        "dialogue/boh_core.py",
        "dialogue/views.py",
        "dialogue/static/dialogue/js/boh_dialogue.js",
        "requirements.txt",
    ]

    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)

    if missing_files:
        print("Arquivos faltando:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("Estrutura do projeto OK")
        return True


def check_vercel_config():
    """Verifica configuração do Vercel"""
    print("\nVerificando vercel.json...")

    try:
        with open("vercel.json", "r") as f:
            config = json.load(f)

        # Verificar estrutura básica
        if "functions" not in config:
            print("Propriedade 'functions' não encontrada")
            return False

        if "api/wsgi.py" not in config["functions"]:
            print("Função 'api/wsgi.py' não configurada")
            return False

        if "routes" not in config:
            print("Propriedade 'routes' não encontrada")
            return False

        # Verificar CORS
        if "headers" not in config:
            print("Headers CORS não configurados")

        print("vercel.json OK")
        return True

    except Exception as e:
        print(f"Erro ao verificar vercel.json: {e}")
        return False


def check_github_workflow():
    """Verifica workflow do GitHub Actions"""
    print("\nVerificando workflow do GitHub Actions...")

    workflow_path = Path(".github/workflows/deploy.yaml")
    if not workflow_path.exists():
        print("Workflow não encontrado")
        return False

    try:
        with open(workflow_path, "r") as f:
            content = f.read()

        required_elements = [
            "deploy-github-pages",
            "deploy-vercel-api",
            "build_github_pages.py",
            "vercel build",
            "vercel deploy",
        ]

        missing_elements = []
        for element in required_elements:
            if element not in content:
                missing_elements.append(element)

        if missing_elements:
            print("Elementos faltando no workflow:")
            for element in missing_elements:
                print(f"   - {element}")
            return False

        print("Workflow do GitHub Actions OK")
        return True

    except Exception as e:
        print(f"Erro ao verificar workflow: {e}")
        return False


def check_javascript_config():
    """Verifica configuração do JavaScript"""
    print("\nVerificando configuração do JavaScript...")

    js_path = Path("dialogue/static/dialogue/js/boh_dialogue.js")
    if not js_path.exists():
        print("boh_dialogue.js não encontrado")
        return False

    try:
        with open(js_path, "r", encoding="utf-8") as f:
            content = f.read()

        if "getApiUrl()" not in content:
            print("Método getApiUrl() não encontrado")
            return False

        if "github.io" not in content:
            print("Detecção do GitHub Pages não configurada")
            return False

        print("JavaScript configurado OK")
        return True

    except Exception as e:
        print(f"Erro ao verificar JavaScript: {e}")
        return False


def main():
    """Executa todas as verificações"""
    print("BOH! Project Configuration Checker")
    print("=" * 50)

    checks = [
        check_project_structure,
        check_vercel_config,
        check_github_workflow,
        check_javascript_config,
    ]

    all_passed = True
    for check in checks:
        if not check():
            all_passed = False

    print("\n" + "=" * 50)
    if all_passed:
        print("Todas as verificações passaram!")
        print("\nPróximos passos:")
        print("1. Configure os secrets no GitHub")
        print("2. Faça push para a branch 'ghpage'")
        print("3. Verifique os deploys no GitHub Actions e Vercel")
    else:
        print("Algumas verificações falharam")
        print("Corrija os problemas antes de fazer deploy")


if __name__ == "__main__":
    main()
