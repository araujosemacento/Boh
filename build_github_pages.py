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
        print(f"Copiados arquivos estáticos para {static_dest}")

    # Criar index.html principal
    index_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BOH! Dialogue System</title>
    <link rel="stylesheet" href="static/css/style.css">
</head>
<body>
    <div class="container">
        <div class="dialogue-container">
            <div id="ascii-art"></div>
            <div id="dialogue-box">
                <div id="dialogue-text"></div>
                <div id="response-controls" style="display: none;">
                    <button onclick="sendResponse('yes')">Sim</button>
                    <button onclick="sendResponse('no')">Não</button>
                </div>
                <div id="name-input" style="display: none;">
                    <input type="text" id="name-field" placeholder="Digite seu nome">
                    <button onclick="submitName()">Confirmar</button>
                </div>
            </div>
            <div id="static-display"></div>
            <div id="aux-display"></div>
        </div>
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
