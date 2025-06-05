#!/usr/bin/env python3
"""
Script de deploy automático para BOH! Dialogue System
"""
import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Executa um comando e mostra o resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
        print(f"✅ {description} - OK")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Erro:")
        print(f"   {e.stderr}")
        return False


def check_git_status():
    """Verifica o status do git"""
    print("🔍 Verificando status do Git...")
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True
        )
        if result.stdout.strip():
            print("⚠️  Há arquivos modificados não commitados:")
            print(result.stdout)
            return False
        else:
            print("✅ Git status limpo")
            return True
    except Exception as e:
        print(f"❌ Erro ao verificar git: {e}")
        return False


def get_current_branch():
    """Obtém a branch atual"""
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"], capture_output=True, text=True
        )
        return result.stdout.strip()
    except:
        return "unknown"


def main():
    """Executa o processo de deploy"""
    print("🚀 BOH! Dialogue System - Deploy Script")
    print("=" * 50)

    # Verificar se estamos no diretório correto
    if not Path("manage.py").exists():
        print("❌ Execute este script no diretório raiz do projeto")
        sys.exit(1)

    # Verificar configuração
    print("1️⃣ Verificando configuração...")
    if not run_command("python check_config.py", "Verificação da configuração"):
        sys.exit(1)

    # Gerar site estático
    print("\n2️⃣ Gerando site estático...")
    if not run_command("python build_github_pages.py", "Build do GitHub Pages"):
        sys.exit(1)

    # Verificar Git
    print("\n3️⃣ Verificando Git...")
    current_branch = get_current_branch()
    print(f"   Branch atual: {current_branch}")

    if current_branch != "ghpage":
        print("⚠️  Você não está na branch 'ghpage'")
        response = input("   Deseja trocar para ghpage? (y/N): ")
        if response.lower() == "y":
            if not run_command("git checkout ghpage", "Mudança para branch ghpage"):
                sys.exit(1)
        else:
            print("   Continuando na branch atual...")

    # Verificar arquivos não commitados
    if not check_git_status():
        response = input("   Deseja commitar as mudanças? (y/N): ")
        if response.lower() == "y":
            commit_msg = (
                input("   Mensagem do commit: ") or "Deploy configuration update"
            )
            if run_command("git add .", "Adicionando arquivos"):
                run_command(f'git commit -m "{commit_msg}"', "Commitando mudanças")

    # Instruções finais
    print("\n" + "=" * 50)
    print("🎉 Preparação para deploy concluída!")
    print("\n📋 Próximos passos manuais:")
    print("1. Configure os secrets no GitHub:")
    print("   - VERCEL_TOKEN")
    print("   - VERCEL_ORG_ID")
    print("   - VERCEL_PROJECT_ID")
    print("\n2. Configure GitHub Pages:")
    print("   - Settings → Pages → GitHub Actions")
    print("\n3. Faça push para deploy:")
    print("   git push origin ghpage")
    print("\n4. Monitore os deploys:")
    print("   - GitHub Actions: https://github.com/suzuma/Boh/actions")
    print("   - Vercel: https://vercel.com/dashboard")
    print("\n🌐 URLs finais:")
    print("   - Frontend: https://suzuma.github.io/Boh")
    print("   - API: https://boh-dialogue-api.vercel.app/api/dialogue/")


if __name__ == "__main__":
    main()
