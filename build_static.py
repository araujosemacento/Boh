#!/usr/bin/env python3
"""
Script para gerar uma versão estática da aplicação BOH para deploy no GitHub Pages
"""

import os
import sys
import shutil
import django
from pathlib import Path


def setup_django():
    """Configura o Django para uso standalone"""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boh.settings")
    try:
        django.setup()
    except Exception as e:
        print(f"Erro ao configurar Django: {e}")
        return False
    return True


def create_static_site():
    """Cria o diretório e arquivos para o site estático"""

    # Criar diretório de saída
    output_dir = Path("static_site")
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir()

    # Copiar arquivos estáticos
    static_dir = Path("dialogue/static")
    if static_dir.exists():
        shutil.copytree(static_dir, output_dir, dirs_exist_ok=True)
        print("Arquivos estáticos copiados")

    # Criar index.html principal
    index_content = """<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BOH - Diálogo Interativo</title>
    <link rel="stylesheet" href="dialogue/css/style.css">
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: 'Courier New', monospace;
            background: #000;
            color: #00ff00;
            overflow: hidden;
        }
        
        .container {
            display: flex;
            flex-direction: column;
            height: 100vh;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
        
        .boh-display {
            margin: 20px;
        }
        
        .expression {
            font-size: 2em;
            margin-bottom: 10px;
        }
        
        .dialogue-container {
            font-size: 1.2em;
            margin: 10px 0;
        }
        
        .response-controls, .name-input-area {
            margin: 20px 0;
        }
        
        .control-btn, .name-input-area button {
            background: #333;
            color: #00ff00;
            border: 1px solid #00ff00;
            padding: 10px 20px;
            margin: 5px;
            cursor: pointer;
            font-family: inherit;
        }
        
        .control-btn:hover, .name-input-area button:hover {
            background: #00ff00;
            color: #000;
        }
        
        #name-input {
            background: #333;
            color: #00ff00;
            border: 1px solid #00ff00;
            padding: 10px;
            font-family: inherit;
        }
        
        .text-red { color: #ff0000; }
        .text-green { color: #00ff00; }
        .text-blue { color: #0088ff; }
        .text-yellow { color: #ffff00; }
        .text-purple { color: #ff00ff; }
        .text-cyan { color: #00ffff; }
        .text-bold { font-weight: bold; }
        
        .static-text, .list-model, .aux-display {
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            margin: 10px 0;
            max-width: 90vw;
            overflow-x: auto;
        }
        
        .loading-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #000;
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        
        .sound-indicator {
            position: fixed;
            top: 10px;
            right: 10px;
            font-size: 1.5em;
            cursor: pointer;
        }
        
        .sound-indicator.active {
            animation: pulse 0.1s ease-in-out;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.2); }
            100% { transform: scale(1); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="boh-display">
            <div class="expression" id="boh-expression">[ ▀ ¸ ▀]</div>
            <div class="dialogue-container">
                <span class="dialogue-prefix">──┤</span>
                <span class="dialogue-text" id="dialogue-text">Clique em qualquer lugar para começar...</span>
                <span class="dialogue-suffix">│</span>
            </div>
        </div>
        
        <div class="static-text" id="static-display" style="display: none;"></div>
        <div class="list-model" id="ascii-display" style="display: none;"></div>
        <div class="aux-display" id="aux-display" style="display: none;"></div>
        
        <div class="response-controls" id="response-controls" style="display: none;">
            <button class="control-btn yes-btn" onclick="sendResponse('s')">
                <span class="text-green">S</span>im
            </button>
            <button class="control-btn no-btn" onclick="sendResponse('n')">
                <span class="text-red">N</span>ão
            </button>
        </div>
        
        <div class="name-input-area" id="name-input-area" style="display: none;">
            <label for="name-input">Digite seu nome aqui:</label>
            <input type="text" id="name-input" maxlength="20" placeholder="Nome" />
            <button onclick="submitName()">Enviar</button>
        </div>
        
        <div class="sound-indicator" id="sound-indicator">🔊</div>
        
        <div class="loading-screen" id="loading-screen">
            <div class="loading-content">
                <div class="loading-expression">[ ▀ ¸ ▀]</div>
                <div class="loading-text">Carregando diálogo do BOH...</div>
            </div>
        </div>
    </div>
    
    <script src="dialogue/js/boh_dialogue.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Aguardar um clique para ativar áudio (requisito dos navegadores)
            document.addEventListener('click', function initAudio() {
                document.removeEventListener('click', initAudio);
            });

            // Inicializar diálogo após clique
            document.addEventListener('click', function startDialogue() {
                document.removeEventListener('click', startDialogue);
                if (typeof BOHDialogue !== 'undefined') {
                    window.bohDialogue = new BOHDialogue();
                    window.bohDialogue.start();
                }
            });
        });
        
        // Permitir teclas S/N para respostas
        document.addEventListener('keydown', function(event) {
            const responseControls = document.getElementById('response-controls');
            if (responseControls && responseControls.style.display !== 'none') {
                if (event.key.toLowerCase() === 's') {
                    sendResponse('s');
                } else if (event.key.toLowerCase() === 'n') {
                    sendResponse('n');
                }
            }
        });
    </script>
</body>
</html>"""

    with open(output_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(index_content)

    print("Site estático criado em 'static_site/'")
    print("Arquivos incluídos:")
    for file_path in output_dir.rglob("*"):
        if file_path.is_file():
            print(f"  - {file_path.relative_to(output_dir)}")


def main():
    """Função principal"""
    print("Gerando site estático para BOH...")

    if not setup_django():
        print("Falha ao configurar Django. Continuando sem Django...")

    create_static_site()
    print("\nConcluído! O site estático está pronto para deploy.")
    print(
        "Para testar localmente, execute: python -m http.server 8000 --directory static_site"
    )


if __name__ == "__main__":
    main()
