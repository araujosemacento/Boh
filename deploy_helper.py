#!/usr/bin/env python3
"""
Script helper para deploy no GitHub Pages via branch ghpage
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, cwd=None):
    """Executa um comando e retorna o resultado"""
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, cwd=cwd
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def get_current_branch():
    """Retorna a branch atual"""
    success, stdout, stderr = run_command("git branch --show-current")
    if success:
        return stdout.strip()
    return None


def branch_exists(branch_name):
    """Verifica se uma branch existe"""
    success, stdout, stderr = run_command(f"git branch --list {branch_name}")
    return branch_name in stdout


def check_git_status():
    """Verifica se há alterações não commitadas"""
    success, stdout, stderr = run_command("git status --porcelain")
    return success, stdout.strip()


def deploy_to_ghpage():
    """Executa o processo de deploy para a branch ghpage"""

    print("🚀 Iniciando deploy para GitHub Pages...")
    print("=" * 50)

    # Verificar se estamos em um repositório git
    if not os.path.exists(".git"):
        print("❌ Erro: Este não é um repositório Git!")
        return False

    # Verificar status do git
    success, status = check_git_status()
    if not success:
        print("❌ Erro ao verificar status do Git!")
        return False

    if status:
        print("⚠️  Há alterações não commitadas:")
        print(status)
        response = input("\nDeseja continuar mesmo assim? (y/N): ")
        if response.lower() not in ["y", "yes"]:
            print("Deploy cancelado.")
            return False

    # Obter branch atual
    current_branch = get_current_branch()
    if not current_branch:
        print("❌ Erro ao obter branch atual!")
        return False

    print(f"📍 Branch atual: {current_branch}")

    # Verificar se a branch ghpage existe
    if not branch_exists("ghpage"):
        print("🔧 Branch 'ghpage' não existe. Criando...")
        success, stdout, stderr = run_command("git checkout -b ghpage")
        if not success:
            print(f"❌ Erro ao criar branch ghpage: {stderr}")
            return False
        print("✅ Branch 'ghpage' criada com sucesso!")
    else:
        # Mudar para branch ghpage
        print("🔄 Mudando para branch ghpage...")
        success, stdout, stderr = run_command("git checkout ghpage")
        if not success:
            print(f"❌ Erro ao mudar para branch ghpage: {stderr}")
            return False

    # Se não estávamos na main, fazer merge da branch atual
    if current_branch != "ghpage":
        print(f"🔀 Fazendo merge de '{current_branch}' para 'ghpage'...")
        success, stdout, stderr = run_command(f"git merge {current_branch}")
        if not success:
            print(f"❌ Erro no merge: {stderr}")
            print("💡 Resolva os conflitos manualmente e tente novamente.")
            return False
        print("✅ Merge realizado com sucesso!")

    # Fazer push para ghpage
    print("📤 Fazendo push para branch ghpage...")
    success, stdout, stderr = run_command("git push origin ghpage")
    if not success:
        print(f"❌ Erro no push: {stderr}")
        return False

    print("✅ Push realizado com sucesso!")
    print("\n🎉 Deploy iniciado!")
    print("📋 Próximos passos:")
    print(
        "   1. Verifique o progresso em: https://github.com/[seu-usuario]/[seu-repo]/actions"
    )
    print("   2. Após conclusão, acesse: https://[seu-usuario].github.io/[seu-repo]")

    # Voltar para a branch original
    if current_branch != "ghpage":
        print(f"\n🔙 Voltando para branch '{current_branch}'...")
        success, stdout, stderr = run_command(f"git checkout {current_branch}")
        if success:
            print("✅ Retornado à branch original!")
        else:
            print(f"⚠️  Não foi possível retornar à branch original: {stderr}")

    return True


def show_help():
    """Mostra a ajuda do script"""
    print(
        """
🚀 Deploy Helper para GitHub Pages

Este script automatiza o processo de deploy para a branch 'ghpage'.

Uso:
    python deploy_helper.py [comando]

Comandos:
    deploy    - Executa o processo de deploy (padrão)
    status    - Mostra o status atual do repositório
    help      - Mostra esta ajuda

O que o script faz:
1. Verifica se há alterações não commitadas
2. Muda para a branch 'ghpage' (cria se não existir)
3. Faz merge da branch atual para 'ghpage'
4. Faz push para 'ghpage' (aciona o GitHub Actions)
5. Retorna à branch original

Pré-requisitos:
- Repositório Git configurado
- Branch 'ghpage' configurada para GitHub Pages
- Workflow do GitHub Actions configurado
"""
    )


def show_status():
    """Mostra o status atual do repositório"""
    print("📊 Status do Repositório Git")
    print("=" * 30)

    # Branch atual
    current_branch = get_current_branch()
    print(f"📍 Branch atual: {current_branch or 'Desconhecida'}")

    # Status do git
    success, status = check_git_status()
    if success:
        if status:
            print("📝 Alterações pendentes:")
            print(status)
        else:
            print("✅ Nenhuma alteração pendente")
    else:
        print("❌ Erro ao verificar status")

    # Verificar se branch ghpage existe
    if branch_exists("ghpage"):
        print("✅ Branch 'ghpage' existe")
    else:
        print("⚠️  Branch 'ghpage' não existe")


def main():
    """Função principal"""
    command = sys.argv[1] if len(sys.argv) > 1 else "deploy"

    if command == "help":
        show_help()
    elif command == "status":
        show_status()
    elif command == "deploy":
        success = deploy_to_ghpage()
        if not success:
            sys.exit(1)
    else:
        print(f"❌ Comando desconhecido: {command}")
        print("Use 'python deploy_helper.py help' para ver os comandos disponíveis.")
        sys.exit(1)


if __name__ == "__main__":
    main()
