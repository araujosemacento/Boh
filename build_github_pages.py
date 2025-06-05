#!/usr/bin/env python3
"""
Script para gerar arquivos estáticos para deploy no GitHub Pages
"""
import os
import shutil
from pathlib import Path


def create_github_pages_site():
    """Cria o site estático para GitHub Pages"""

    # Diretório de saída
    output_dir = Path("docs")  # GitHub Pages pode usar /docs
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir()

    # Copiar arquivos estáticos
    static_src = Path("dialogue/static/dialogue")
    if static_src.exists():
        static_dest = output_dir / "static"
        shutil.copytree(static_src, static_dest)
        print(
            f"Copiados arquivos estáticos para {static_dest}"
        )  # Criar index.html principal baseado na estrutura original do Django template
    index_content = """<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BOH! - Diálogo Interativo</title>
    <link rel="stylesheet" href="static/css/style.css">
</head>
<body>
    <div class="container">
        <div class="terminal-window">
            <div class="terminal-header">
                <div class="terminal-buttons">
                    <span class="btn red"></span>
                    <span class="btn yellow"></span>
                    <span class="btn green"></span>
                </div>
                <div class="terminal-title">BOH! - Terminal Interativo</div>
                <div></div>
            </div>
            <div class="terminal-content">
                <!-- Área principal do BOH -->
                <div class="boh-display">
                    <div class="expression" id="boh-expression">[ ▀ ¸ ▀]</div>
                    <div class="dialogue-container">
                        <span class="dialogue-prefix">──┤</span>
                        <span class="dialogue-text" id="dialogue-text"></span>
                        <span class="dialogue-suffix">│</span>
                    </div>
                </div>

                <!-- Área para texto estático -->
                <div class="static-text" id="static-display"></div>

                <!-- Área para diagramas ASCII das listas -->
                <div class="list-model" id="ascii-display"></div>                <!-- Área para arte ASCII do AUX -->
                <div class="ascii-art" id="aux-display"></div>

                <!-- Controles de resposta - usando estrutura existente -->
                <div class="input-area" id="response-controls" style="display: none;">
                    <button class="control-btn" onclick="sendResponse('positive')">
                        <span class="text-green">S</span>im
                    </button>
                    <button class="control-btn" onclick="sendResponse('negative')">
                        <span class="text-red">N</span>ão
                    </button>
                </div>                <!-- Input para nome - usando classe existente -->
                <div class="name-input" id="name-input-area" style="display: none;">
                    <label for="name-input-field">Digite seu nome aqui:</label>
                    <input type="text" id="name-input-field" maxlength="20" placeholder="Nome" />
                    <button onclick="submitName()">Enviar</button>
                </div>                <!-- Loading screen - usando estrutura simples sem classe específica -->
                <div id="loading-screen" style="display: none; text-align: center; padding: 20px;">
                    <div class="expression">[ ▀ ¸ ▀]</div>
                    <div style="color: #c9d1d9; margin-top: 10px;">Carregando diálogo do BOH...</div>
                </div>

                <!-- Status de conectividade -->
                <div id="connection-status" style="position: fixed; top: 20px; left: 20px; padding: 10px; background: rgba(0,0,0,0.8); border-radius: 4px; font-size: 12px; color: #c9d1d9; z-index: 1000;">
                    <div>🔗 Status: <span id="connection-indicator">Testando...</span></div>
                    <div>📍 API: <span id="api-url-display">-</span></div>
                </div>
            </div>
        </div>
    </div>

    <!-- Controles de áudio -->
    <div class="controls" id="audio-controls">
        <button class="control-btn" id="toggle-sound">🔊</button>
        <div class="sound-indicator" id="sound-indicator"></div>
    </div>

    <script>
        // Configuração da API do Vercel
        window.VERCEL_API_URL = 'https://boh-dialogue-api.vercel.app';
    </script>
    <script src="static/js/boh_dialogue.js"></script>
</body>
</html>"""

    with open(output_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(index_content)

    print(f"Criado index.html em {output_dir}")

    # Criar configuração do GitHub Pages
    github_config = """---
title: BOH! Dialogue System
description: Sistema interativo de diálogo com BOH!
theme: jekyll-theme-minimal
baseurl: /Boh
url: https://suzuma.github.io
"""

    with open(output_dir / "_config.yml", "w", encoding="utf-8") as f:
        f.write(github_config)

    print(f"Criado _config.yml")

    # Criar README para GitHub Pages
    readme_content = """# BOH! Dialogue System

Sistema interativo de diálogo com BOH!

## Acesso

- **Página Principal**: [https://suzuma.github.io/Boh](https://suzuma.github.io/Boh)
- **API Backend**: Hospedada no Vercel

## Arquitetura

- **Frontend**: GitHub Pages (arquivos estáticos)
- **Backend**: Vercel (API Django)
- **Comunicação**: CORS habilitado para domínios cruzados

## Desenvolvimento

Para executar localmente:

```bash
python manage.py runserver
```

Para gerar build para GitHub Pages:

```bash
python build_github_pages.py
```
"""
    with open(output_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"Criado README.md")

    # Criar arquivo .nojekyll para GitHub Pages
    with open(output_dir / ".nojekyll", "w") as f:
        f.write("")

    print(f"Criado .nojekyll")
    print(f"\nSite estático gerado em {output_dir}")
    print("Lembre-se de:")
    print("   1. Atualizar a URL da API no index.html")
    print("   2. Configurar o repositório para usar GitHub Pages")
    print("   3. Definir os secrets no GitHub Actions")


if __name__ == "__main__":
    create_github_pages_site()
