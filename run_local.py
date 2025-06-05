#!/usr/bin/env python
"""
Script para executar o servidor de desenvolvimento local com configurações adequadas.
Este script garante que o ambiente local funcione independentemente do Vercel.
"""
import os
import sys
import django
from django.core.management import execute_from_command_line


def setup_local_environment():
    """Configura o ambiente local para desenvolvimento"""
    # Define variáveis de ambiente para desenvolvimento local
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boh.settings")
    os.environ.setdefault("DEBUG", "True")

    # Configura CORS para desenvolvimento local
    os.environ.setdefault("CORS_ALLOW_ALL_ORIGINS", "True")

    print("🚀 Configurando ambiente de desenvolvimento local...")
    print(f"📍 DEBUG: {os.environ.get('DEBUG', 'False')}")
    print(
        f"🌐 CORS_ALLOW_ALL_ORIGINS: {os.environ.get('CORS_ALLOW_ALL_ORIGINS', 'False')}"
    )
    print(f"🔧 DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}")


def main():
    """Executa comandos Django com configuração local"""
    setup_local_environment()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Se nenhum comando foi fornecido, executa runserver
    if len(sys.argv) == 1:
        print("🔄 Nenhum comando especificado, executando runserver...")
        sys.argv.append("runserver")
        sys.argv.append("127.0.0.1:8000")

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
