#!/usr/bin/env python
"""
Script de teste para validar conectividade e funcionamento
do sistema BOH em diferentes ambientes.
"""
import os
import sys
import requests
import json
from urllib.parse import urljoin


def test_local_server():
    """Testa o servidor Django local"""
    print("🔍 Testando servidor local...")

    try:
        # Testa endpoint de saúde
        response = requests.get("http://127.0.0.1:8000/api/dialogue/", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor local respondendo corretamente")
            return True
        else:
            print(f"⚠️  Servidor local com status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Servidor local não está rodando")
        return False
    except Exception as e:
        print(f"❌ Erro ao testar servidor local: {e}")
        return False


def test_dialogue_data(base_url):
    """Testa carregamento de dados de diálogo"""
    print(f"💬 Testando dados de diálogo em {base_url}...")

    try:
        response = requests.post(
            f"{base_url}/api/dialogue/",
            json={"action": "get_all_data"},
            headers={"Content-Type": "application/json"},
            timeout=10,
        )

        if response.status_code == 200:
            data = response.json()
            print("✅ Dados de diálogo carregados com sucesso")
            print(f"   - Passos de diálogo: {len(data.get('dialogue_sequence', []))}")
            print(f"   - Expressões: {len(data.get('expressions', {}))}")
            print(f"   - Modelos: {len(data.get('list_models', {}))}")
            return True
        else:
            print(f"❌ Erro ao carregar dados: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar dados de diálogo: {e}")
        return False


def test_colorize_api(base_url):
    """Testa API de colorização"""
    print(f"🎨 Testando API de colorização em {base_url}...")

    try:
        test_text = "→ Teste de colorização ←"
        response = requests.post(
            f"{base_url}/api/dialogue/",
            json={"action": "colorize_arrows", "text": test_text},
            headers={"Content-Type": "application/json"},
            timeout=10,
        )

        if response.status_code == 200:
            data = response.json()
            print("✅ API de colorização funcionando")
            print(f"   Original: {test_text}")
            print(f"   Colorizado: {data.get('colorized_text', '')}")
            return True
        else:
            print(f"❌ Erro na colorização: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar colorização: {e}")
        return False


def test_vercel_endpoint():
    """Testa endpoint Vercel"""
    vercel_url = "https://boh-dialogue-api.vercel.app"
    print(f"🌐 Testando endpoint Vercel: {vercel_url}...")

    try:
        response = requests.get(f"{vercel_url}/api/dialogue/", timeout=15)
        if response.status_code == 200:
            print("✅ Endpoint Vercel respondendo")
            return True
        else:
            print(f"⚠️  Endpoint Vercel com status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao conectar com Vercel: {e}")
        return False


def main():
    """Executa todos os testes"""
    print("🧪 INICIANDO TESTES DE CONECTIVIDADE BOH")
    print("=" * 50)

    results = {}

    # Teste 1: Servidor local
    results["local_server"] = test_local_server()

    if results["local_server"]:
        # Teste 2: Dados de diálogo (local)
        results["local_dialogue"] = test_dialogue_data("http://127.0.0.1:8000")

        # Teste 3: Colorização (local)
        results["local_colorize"] = test_colorize_api("http://127.0.0.1:8000")
    else:
        print("⚠️  Servidor local não disponível, pulando testes locais")
        results["local_dialogue"] = False
        results["local_colorize"] = False

    print("\n" + "=" * 50)

    # Teste 4: Endpoint Vercel
    results["vercel_server"] = test_vercel_endpoint()

    if results["vercel_server"]:
        # Teste 5: Dados de diálogo (Vercel)
        results["vercel_dialogue"] = test_dialogue_data(
            "https://boh-dialogue-api.vercel.app"
        )

        # Teste 6: Colorização (Vercel)
        results["vercel_colorize"] = test_colorize_api(
            "https://boh-dialogue-api.vercel.app"
        )
    else:
        print("⚠️  Endpoint Vercel não disponível, pulando testes remotos")
        results["vercel_dialogue"] = False
        results["vercel_colorize"] = False

    # Relatório final
    print("\n" + "=" * 50)
    print("📊 RELATÓRIO FINAL")
    print("=" * 50)

    print("🏠 AMBIENTE LOCAL:")
    print(f"   ✓ Servidor: {'✅ OK' if results['local_server'] else '❌ FALHOU'}")
    print(f"   ✓ Diálogo: {'✅ OK' if results['local_dialogue'] else '❌ FALHOU'}")
    print(f"   ✓ Colorização: {'✅ OK' if results['local_colorize'] else '❌ FALHOU'}")

    print("\n🌐 AMBIENTE VERCEL:")
    print(f"   ✓ Servidor: {'✅ OK' if results['vercel_server'] else '❌ FALHOU'}")
    print(f"   ✓ Diálogo: {'✅ OK' if results['vercel_dialogue'] else '❌ FALHOU'}")
    print(f"   ✓ Colorização: {'✅ OK' if results['vercel_colorize'] else '❌ FALHOU'}")

    # Determinar status geral
    local_ok = all(
        [results["local_server"], results["local_dialogue"], results["local_colorize"]]
    )
    vercel_ok = all(
        [
            results["vercel_server"],
            results["vercel_dialogue"],
            results["vercel_colorize"],
        ]
    )

    print(f"\n🎯 STATUS GERAL:")
    print(f"   🏠 Local: {'✅ FUNCIONAL' if local_ok else '❌ COM PROBLEMAS'}")
    print(f"   🌐 Vercel: {'✅ FUNCIONAL' if vercel_ok else '❌ COM PROBLEMAS'}")

    if local_ok and vercel_ok:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("   O sistema está funcionando tanto localmente quanto no Vercel.")
    elif local_ok:
        print("\n⚠️  APENAS O AMBIENTE LOCAL ESTÁ FUNCIONANDO")
        print("   Verifique o deploy no Vercel.")
    elif vercel_ok:
        print("\n⚠️  APENAS O AMBIENTE VERCEL ESTÁ FUNCIONANDO")
        print("   Inicie o servidor local com: python run_local.py")
    else:
        print("\n❌ FALHA GERAL NO SISTEMA")
        print("   Verifique as configurações e dependências.")

    return local_ok or vercel_ok


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
