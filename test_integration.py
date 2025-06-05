#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json


def test_dialogue_integration():
    """Testa a integração completa do sistema de diálogo"""
    base_url = "http://127.0.0.1:8000"
    api_url = f"{base_url}/api/dialogue/"

    print("=== TESTE DE INTEGRAÇÃO BOH! ===\n")

    # 1. Testa página principal
    try:
        response = requests.get(base_url, timeout=5)
        print(
            f"✅ Página principal: {response.status_code} ({len(response.content)} bytes)"
        )
    except Exception as e:
        print(f"❌ Erro na página principal: {e}")
        return

    # 2. Testa carregamento de dados completo
    try:
        response = requests.post(api_url, json={"action": "get_all_data"}, timeout=5)
        data = response.json()
        print(f"✅ Dados carregados: {len(data)} seções")

        # Verifica se tem as seções esperadas
        expected_sections = [
            "expressions",
            "dialogue_sequence",
            "list_models",
            "aux_art",
            "messages",
        ]
        for section in expected_sections:
            if section in data:
                print(f"   ✅ {section}: {len(data[section])} items")
            else:
                print(f"   ❌ {section}: não encontrado")

    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")
        return

    # 3. Testa sequência de diálogo
    try:
        for step in [0, 1, 2]:
            response = requests.post(
                api_url, json={"action": "get_dialogue_item", "step": step}, timeout=5
            )

            if response.status_code == 200:
                item = response.json()
                print(
                    f"✅ Step {step}: {item['item']['type']} - '{item['item']['text'][:30]}...'"
                )
            else:
                print(f"❌ Step {step}: HTTP {response.status_code}")

    except Exception as e:
        print(f"❌ Erro na sequência de diálogo: {e}")

    # 4. Testa colorização de setas
    try:
        response = requests.post(
            api_url,
            json={
                "action": "colorize_arrows",
                "text": "Teste ‹ esquerda › direita « dupla » fim",
            },
            timeout=5,
        )

        if response.status_code == 200:
            result = response.json()
            original_len = len("Teste ‹ esquerda › direita « dupla » fim")
            colorized_len = len(result["colorized_text"])
            print(
                f"✅ Colorização: {original_len}→{colorized_len} chars (spans adicionados)"
            )
        else:
            print(f"❌ Colorização: HTTP {response.status_code}")

    except Exception as e:
        print(f"❌ Erro na colorização: {e}")

    print("\n=== TESTE CONCLUÍDO ===")


if __name__ == "__main__":
    test_dialogue_integration()
