import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Configuração Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boh.settings")

try:
    import django

    django.setup()
    from django.core.wsgi import get_wsgi_application

    application = get_wsgi_application()
except Exception as e:
    import json

    print(f"Erro ao configurar Django: {e}")

    # Fallback simples se Django falhar
    def fallback_application(environ, start_response):
        status = "500 Internal Server Error"
        headers = [("Content-type", "application/json")]
        start_response(status, headers)
        return [json.dumps({"error": f"Configuração falhou: {str(e)}"}).encode()]

    application = fallback_application
