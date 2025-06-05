#!/usr/bin/env python3
"""
Script para testar a estrutura Vercel Build Output API localmente
e validar se tudo está correto antes do deploy
"""

import json
import requests
from pathlib import Path
import subprocess
import time


def test_build_structure():
    """Verifica se a estrutura Build Output foi criada corretamente"""
    print("🔍 Verificando estrutura Build Output...")

    output_dir = Path(".vercel/output")

    # Verificar diretórios essenciais
    required_paths = [
        output_dir / "config.json",
        output_dir / "functions/api/index.py",
        output_dir / "functions/api/requirements.txt",
        output_dir / "functions/api/boh",
        output_dir / "functions/api/dialogue",
        output_dir / "static/index.html",
    ]

    missing = []
    for path in required_paths:
        if not path.exists():
            missing.append(str(path))

    if missing:
        print("❌ Arquivos/diretórios faltando:")
        for item in missing:
            print(f"   - {item}")
        return False

    print("✅ Estrutura Build Output válida")

    # Verificar configuração JSON
    try:
        with open(output_dir / "config.json", "r") as f:
            config = json.load(f)

        if config.get("version") != 3:
            print("❌ Versão da configuração inválida")
            return False

        if not config.get("routes"):
            print("❌ Rotas não configuradas")
            return False

        print("✅ Configuração JSON válida")
    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        return False

    return True


def test_local_server():
    """Testa se o servidor local está funcionando"""
    print("\n🔍 Testando servidor local...")

    try:
        # Testar endpoint de health
        response = requests.get("http://localhost:8000/api/dialogue/", timeout=5)

        if response.status_code == 200:
            data = response.json()
            print("✅ Servidor local funcionando")
            print(f"   Status: {response.status_code}")
            print(f"   Resposta: {data}")
            return True
        else:
            print(f"❌ Servidor retornou status {response.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        print("⚠️  Servidor local não está rodando")
        print("   Execute: python run_local.py")
        return False
    except Exception as e:
        print(f"❌ Erro ao testar servidor: {e}")
        return False


def test_vercel_deployment():
    """Testa se o deploy Vercel está funcionando"""
    print("\n🔍 Testando deploy Vercel...")

    # URLs de teste (ajuste conforme necessário)
    vercel_urls = [
        "https://boh-dialogue-api.vercel.app/api/dialogue/",
        "https://boh-dialogue-api.vercel.app/",
    ]

    for url in vercel_urls:
        try:
            print(f"   Testando: {url}")
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                print(f"   ✅ {url} - Status: {response.status_code}")

                # Tentar parsear JSON se possível
                try:
                    data = response.json()
                    print(f"      Resposta: {data}")
                except:
                    print(f"      Resposta HTML (length: {len(response.text)})")
            else:
                print(f"   ❌ {url} - Status: {response.status_code}")

        except Exception as e:
            print(f"   ❌ {url} - Erro: {e}")


def run_deployment_test():
    """Executa todos os testes de deployment"""
    print("🚀 TESTE DE DEPLOYMENT VERCEL BUILD OUTPUT API")
    print("=" * 50)

    # 1. Verificar estrutura build
    if not test_build_structure():
        print("\n❌ Falha na estrutura Build Output")
        print("Execute: python build_vercel.py")
        return False

    # 2. Testar servidor local
    local_ok = test_local_server()

    # 3. Testar deploy Vercel
    test_vercel_deployment()

    print("\n" + "=" * 50)
    print("📋 RESUMO DO TESTE:")
    print(f"   Build Structure: ✅")
    print(f"   Servidor Local: {'✅' if local_ok else '❌'}")
    print(f"   Deploy Vercel: Verifique logs acima")

    print("\n🔧 PRÓXIMOS PASSOS:")
    if not local_ok:
        print("1. Inicie o servidor local: python run_local.py")
    print("2. Commit e push das mudanças")
    print("3. Verifique GitHub Actions para deploy automático")
    print("4. Teste o endpoint final no Vercel")

    return True


if __name__ == "__main__":
    run_deployment_test()
