#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dialogue.boh_core import BOHCore


def test_colorize_arrows():
    """Testa a funcionalidade de colorização de setas"""
    boh = BOHCore()

    # Teste com setas simples
    test_text1 = "Teste ‹ esquerda › direita"
    result1 = boh.colorize_arrows(test_text1)
    print("Texto original:", test_text1)
    print("Texto colorizado:", result1)
    print()

    # Teste com setas duplas
    test_text2 = "Teste « esquerda dupla » direita dupla"
    result2 = boh.colorize_arrows(test_text2)
    print("Texto original:", test_text2)
    print("Texto colorizado:", result2)
    print()

    # Teste com mistura
    test_text3 = "‹Entrada› processamento «Saída»"
    result3 = boh.colorize_arrows(test_text3)
    print("Texto original:", test_text3)
    print("Texto colorizado:", result3)
    print()

    # Teste sem setas
    test_text4 = "Texto sem setas especiais"
    result4 = boh.colorize_arrows(test_text4)
    print("Texto original:", test_text4)
    print("Texto colorizado:", result4)


if __name__ == "__main__":
    test_colorize_arrows()
