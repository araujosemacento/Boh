import os
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
