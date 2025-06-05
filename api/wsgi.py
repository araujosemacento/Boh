import os
import sys
import json
from pathlib import Path

# Adiciona o diretório raiz ao Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Configuração Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boh.settings")
os.environ.setdefault("DEBUG", "False")


def handler(request):
    """Handler principal para Vercel serverless function"""
    try:
        import django
        from django.conf import settings

        # Configurar Django se não estiver configurado
        if not settings.configured:
            django.setup()

        from django.core.wsgi import get_wsgi_application

        wsgi_app = get_wsgi_application()

        # Converter request do Vercel para WSGI environ
        environ = {
            "REQUEST_METHOD": request.method,
            "PATH_INFO": request.url.path,
            "QUERY_STRING": request.url.query or "",
            "CONTENT_TYPE": request.headers.get("content-type", ""),
            "CONTENT_LENGTH": str(len(request.body or b"")),
            "SERVER_NAME": request.url.hostname,
            "SERVER_PORT": str(request.url.port or 443),
            "wsgi.version": (1, 0),
            "wsgi.url_scheme": request.url.scheme,
            "wsgi.input": request.body or b"",
            "wsgi.errors": sys.stderr,
            "wsgi.multithread": False,
            "wsgi.multiprocess": True,
            "wsgi.run_once": False,
        }

        # Adicionar headers HTTP
        for key, value in request.headers.items():
            key = key.upper().replace("-", "_")
            if key not in ("CONTENT_TYPE", "CONTENT_LENGTH"):
                environ[f"HTTP_{key}"] = value

        # Executar aplicação WSGI
        response_data = []

        def start_response(status, headers, exc_info=None):
            response_data.extend([status, headers])

        result = wsgi_app(environ, start_response)

        # Preparar resposta
        status_code = int(response_data[0].split()[0]) if response_data else 500
        response_headers = dict(response_data[1]) if len(response_data) > 1 else {}        # Garantir CORS
        response_headers.update(
            {
                "Access-Control-Allow-Origin": "https://araujosemacento.github.io",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With",
                "Access-Control-Allow-Credentials": "true",
            }
        )

        # Se OPTIONS request, retornar apenas headers CORS
        if request.method == "OPTIONS":
            return {"statusCode": 200, "headers": response_headers, "body": ""}

        body = b"".join(result).decode("utf-8") if result else ""

        return {"statusCode": status_code, "headers": response_headers, "body": body}

    except Exception as e:
        return {
            "statusCode": 500,            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "https://araujosemacento.github.io",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization",
            },
            "body": json.dumps(
                {
                    "error": "Internal Server Error",
                    "message": str(e),
                    "debug_info": "Django handler failed",
                    "path_info": getattr(request, "url", {}).get("path", "unknown"),
                }
            ),
        }


# Manter compatibilidade com WSGI tradicional
try:
    import django

    django.setup()
    from django.core.wsgi import get_wsgi_application

    application = get_wsgi_application()

    # Alias para Vercel
    app = application

except Exception as e:
    print(f"Erro ao configurar Django: {e}")

    # Fallback simples se Django falhar
    def fallback_application(environ, start_response):
        status = "500 Internal Server Error"
        headers = [("Content-type", "application/json")]
        start_response(status, headers)
        return [json.dumps({"error": f"Configuração falhou: {str(e)}"}).encode()]

    application = fallback_application
    app = application
