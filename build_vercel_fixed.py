#!/usr/bin/env python3
"""
Script para construir o projeto usando Vercel Build Output API
Cria a estrutura .vercel/output/ com serverless functions e static files
"""

import os
import json
import shutil
from pathlib import Path


def create_vercel_output():
    """Cria a estrutura .vercel/output/ conforme Build Output API"""

    # Diretórios base
    output_dir = Path(".vercel/output")
    functions_dir = output_dir / "functions"
    static_dir = output_dir / "static"

    # Limpar diretório anterior se existir
    if output_dir.exists():
        shutil.rmtree(output_dir)

    # Criar estrutura de diretórios
    functions_dir.mkdir(parents=True, exist_ok=True)
    static_dir.mkdir(parents=True, exist_ok=True)

    print("🏗️  Criando Build Output Structure...")

    # 1. Criar serverless function para Django API
    api_func_dir = functions_dir / "api"
    api_func_dir.mkdir(exist_ok=True)

    # Criar arquivo index.py otimizado para Vercel
    index_py_content = """import os
import sys
from pathlib import Path
import json

# Configurar paths para Vercel
current_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(current_dir))

# Configuração de ambiente
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boh.settings")
os.environ.setdefault("DEBUG", "False")

def handler(request):
    try:
        import django
        from django.conf import settings
        
        # Configurar Django se não estiver configurado
        if not settings.configured:
            django.setup()
        
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
        
        # Converter request do Vercel para WSGI
        environ = {
            'REQUEST_METHOD': request.method,
            'PATH_INFO': request.url.path,
            'QUERY_STRING': request.url.query or '',
            'CONTENT_TYPE': request.headers.get('content-type', ''),
            'CONTENT_LENGTH': str(len(request.body or '')),
            'SERVER_NAME': request.url.hostname,
            'SERVER_PORT': str(request.url.port or 443),
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': request.url.scheme,
            'wsgi.input': request.body,
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': True,
            'wsgi.run_once': False,
        }
        
        # Adicionar headers HTTP
        for key, value in request.headers.items():
            key = key.upper().replace('-', '_')
            if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                environ[f'HTTP_{key}'] = value
        
        # Executar aplicação WSGI
        response_data = []
        
        def start_response(status, headers, exc_info=None):
            response_data.extend([status, headers])
        
        result = application(environ, start_response)
        
        # Preparar resposta
        status_code = int(response_data[0].split()[0])
        response_headers = dict(response_data[1])
        
        # Garantir CORS
        response_headers.update({
            'Access-Control-Allow-Origin': 'https://suzuma.github.io',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Allow-Credentials': 'true'
        })
        
        body = b''.join(result).decode('utf-8')
        
        return {
            'statusCode': status_code,
            'headers': response_headers,
            'body': body
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': 'https://suzuma.github.io',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            },
            'body': json.dumps({
                'error': 'Internal Server Error',
                'message': str(e),
                'debug': 'Django setup failed'
            })
        }
"""

    with open(api_func_dir / "index.py", "w", encoding="utf-8") as f:
        f.write(index_py_content)

    # Copiar requirements.txt para a função
    shutil.copy2("requirements.txt", api_func_dir / "requirements.txt")

    # Copiar código Django
    django_dirs = ["boh", "dialogue", "protocols"]
    for dir_name in django_dirs:
        if Path(dir_name).exists():
            shutil.copytree(
                dir_name,
                api_func_dir / dir_name,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.sqlite3"),
            )

    print("✅ Função serverless Django criada")

    # 2. Criar arquivo de configuração global
    config = {
        "version": 3,
        "routes": [{"handle": "filesystem"}, {"src": "/api/(.*)", "dest": "/api/$1"}],
        "functions": {"api/**": {"runtime": "python3.9"}},
    }

    with open(output_dir / "config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    print("✅ Configuração global criada")

    # 3. Criar health check estático
    health_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Boh API Health Check</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .success { background-color: #d4edda; color: #155724; }
        .error { background-color: #f8d7da; color: #721c24; }
        .loading { background-color: #fff3cd; color: #856404; }
    </style>
</head>
<body>
    <h1>Boh API Health Check</h1>
    <div id="status" class="status loading">Testando conexão com a API...</div>
    
    <h2>Endpoints Disponíveis:</h2>
    <ul>
        <li><a href="/api/dialogue/" target="_blank">GET /api/dialogue/</a> - Status da API</li>
        <li><code>POST /api/dialogue/</code> - Processar ações do diálogo</li>
    </ul>
    
    <h2>GitHub Pages:</h2>
    <p><a href="https://suzuma.github.io/Boh/" target="_blank">https://suzuma.github.io/Boh/</a></p>
    
    <script>
        async function testAPI() {
            try {
                const response = await fetch('/api/dialogue/');
                const data = await response.json();
                
                if (response.ok) {
                    document.getElementById('status').innerHTML = 
                        'API funcionando! Resposta: ' + JSON.stringify(data, null, 2);
                    document.getElementById('status').className = 'status success';
                } else {
                    throw new Error('Status: ' + response.status);
                }
            } catch (error) {
                document.getElementById('status').innerHTML = 
                    'Erro na API: ' + error.message;
                document.getElementById('status').className = 'status error';
            }
        }
        
        testAPI();
    </script>
</body>
</html>"""

    with open(static_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(health_content)

    print("✅ Health check estático criado")

    # 4. Criar arquivo .vercelignore atualizado
    vercelignore_content = """# Database
*.sqlite3
db.sqlite3

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd

# Virtual environments
.venv/
venv/
env/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Development
.env
.env.local
test_*.py
run_local.py

# GitHub Pages
docs/
.nojekyll

# Git
.git/
.gitignore
"""

    with open(".vercelignore", "w", encoding="utf-8") as f:
        f.write(vercelignore_content)

    print("✅ .vercelignore atualizado")

    print("\n🎉 Build Output Structure criada com sucesso!")
    print(f"📁 Estrutura criada em: {output_dir.resolve()}")
    print("\n📋 Arquivos criados:")
    print("├── .vercel/output/")
    print("│   ├── config.json")
    print("│   ├── functions/api/index.py")
    print("│   └── static/index.html")
    print("└── .vercelignore")

    print("\n🚀 Próximos passos:")
    print("1. Commit e push das mudanças")
    print("2. Deploy automático via GitHub Actions")
    print("3. Testar endpoints:")
    print("   - Health check: https://[projeto].vercel.app/")
    print("   - API: https://[projeto].vercel.app/api/dialogue/")


if __name__ == "__main__":
    create_vercel_output()
