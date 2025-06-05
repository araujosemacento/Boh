# 🤖 BOH! Dialogue System - Guia de Desenvolvimento Local

## ✅ Status do Sistema

- **🏠 Ambiente Local**: ✅ **FUNCIONAL**
- **🌐 Endpoint Vercel**: ⚠️  Com problemas (em manutenção)
- **📱 GitHub Pages**: 🔗 Conecta com Vercel quando disponível

## 🚀 Início Rápido

### 1. Instalar Dependências
```powershell
cd "c:\Users\Suzuma\Documents\scripts\python\Boh"
pip install -r requirements.txt
```

### 2. Iniciar Servidor Local
```powershell
# Opção 1: Usando o script personalizado (recomendado)
python run_local.py

# Opção 2: Usando manage.py tradicional
python manage.py runserver 127.0.0.1:8000
```

### 3. Testar Conectividade
```powershell
python test_connectivity.py
```

### 4. Acessar o Sistema
- **Interface Web**: http://127.0.0.1:8000/
- **API Direta**: http://127.0.0.1:8000/api/dialogue/

## 🔧 Scripts Disponíveis

### `run_local.py`
Script otimizado para desenvolvimento local:
- ✅ Configura automaticamente variáveis de ambiente
- ✅ Ativa CORS para todos os origins em modo DEBUG
- ✅ Inicia servidor automaticamente se nenhum comando for especificado
- ✅ Mostra informações de debug úteis

```powershell
# Iniciar servidor (padrão)
python run_local.py

# Executar outros comandos Django
python run_local.py makemigrations
python run_local.py migrate
python run_local.py shell
```

### `test_connectivity.py`
Script de diagnóstico completo:
- 🔍 Testa servidor local
- 🌐 Testa endpoint Vercel
- 💬 Verifica carregamento de dados de diálogo
- 🎨 Testa API de colorização
- 📊 Relatório detalhado

## 🌐 Comunicação com GitHub Pages

O sistema é projetado para funcionar em múltiplos ambientes:

### Desenvolvimento Local
- **Frontend**: Servido pelo Django (templates)
- **Backend**: Django local (127.0.0.1:8000)
- **CORS**: Permissivo para desenvolvimento

### GitHub Pages + Vercel
- **Frontend**: GitHub Pages (arquivos estáticos)
- **Backend**: Vercel (API Django)
- **CORS**: Configurado para suzuma.github.io

### Estrutura de URLs
```
Local:
- Frontend: http://127.0.0.1:8000/
- API: http://127.0.0.1:8000/api/dialogue/

Produção:
- Frontend: https://suzuma.github.io/Boh/
- API: https://boh-dialogue-api.vercel.app/api/dialogue/
```

## 📁 Estrutura do Projeto

```
Boh/
├── 📄 manage.py                    # Django management
├── 🔧 run_local.py                # Script de desenvolvimento
├── 🧪 test_connectivity.py        # Testes de conectividade
├── 📦 requirements.txt            # Dependências Python
├── ⚙️  vercel.json                # Configuração Vercel
│
├── boh/                           # Configurações Django
│   ├── settings.py               # ✅ CORS configurado
│   └── urls.py
│
├── dialogue/                      # App principal
│   ├── 🧠 boh_core.py            # Lógica do BOH
│   ├── 🌐 views.py               # API endpoints
│   ├── 📝 templates/             # Templates Django
│   └── 📦 static/                # Assets estáticos
│
└── docs/                          # GitHub Pages
    ├── 🌐 index.html             # Frontend estático
    └── 📦 static/                # Assets copiados
```

## 🔧 Configurações Importantes

### CORS (Cross-Origin Resource Sharing)
```python
# Em development (DEBUG=True)
CORS_ALLOW_ALL_ORIGINS = True

# Em production
CORS_ALLOWED_ORIGINS = [
    "https://suzuma.github.io",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
```

### Detecção de Ambiente (JavaScript)
```javascript
getApiUrl() {
  const hostname = window.location.hostname;
  
  // GitHub Pages → Vercel
  if (hostname.includes('github.io')) {
    return 'https://boh-dialogue-api.vercel.app';
  }
  
  // Desenvolvimento local → Django local
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return 'http://localhost:8000';
  }
  
  return window.location.origin;
}
```

## 🐛 Solução de Problemas

### Erro: "No module named 'corsheaders'"
```powershell
pip install django-cors-headers
```

### Erro: "CORS header 'Access-Control-Allow-Origin' missing"
- ✅ Verifique se `corsheaders` está em `INSTALLED_APPS`
- ✅ Verifique se `CorsMiddleware` está primeiro em `MIDDLEWARE`
- ✅ Use `run_local.py` que configura CORS automaticamente

### Erro: "Method not allowed"
- ✅ API GET: Apenas para teste de saúde
- ✅ API POST: Para todas as ações funcionais
- ✅ Use `test_connectivity.py` para diagnóstico

### Servidor local não inicia
```powershell
# Verificar se a porta está livre
netstat -an | findstr :8000

# Migrar banco de dados
python run_local.py migrate

# Verificar logs detalhados
python run_local.py runserver --verbosity=2
```

## 📊 API Endpoints

### GET /api/dialogue/
Teste de saúde - retorna status do sistema
```json
{
  "status": "healthy",
  "message": "BOH Dialogue API está funcionando",
  "dialogue_steps": 50,
  "expressions": 6,
  "list_models": 12,
  "aux_art": 8
}
```

### POST /api/dialogue/
Ações funcionais:
- `get_all_data`: Carrega todos os dados do diálogo
- `get_dialogue_item`: Obtém item específico
- `colorize_arrows`: Coloriza texto com setas
- `advance_step`: Avança para próximo passo
- E outras...

## 🎯 Próximos Passos

1. **✅ Ambiente local funcionando** - ✅ Concluído
2. **🔧 Fix Vercel deployment** - 🔄 Em progresso
3. **🎨 Melhorar frontend** - 📅 Planejado
4. **🔊 Otimizar áudio** - 📅 Planejado

---

## 💡 Dicas de Desenvolvimento

- Use `run_local.py` para desenvolvimento mais fluido
- Execute `test_connectivity.py` após mudanças importantes
- O sistema funciona offline (modo local)
- CORS está configurado para desenvolvimento fácil
- Logs detalhados estão disponíveis no console do navegador

**🎉 Sistema totalmente funcional em ambiente local!**
