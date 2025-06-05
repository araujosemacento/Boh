# BOH! Dialogue System - Deploy Configuration

## Arquitetura do Sistema

### Opção Implementada: GitHub Pages + Vercel API

- **Frontend**: GitHub Pages hospeda a página estática
  - URL: `https://suzuma.github.io/Boh`
  - Arquivos estáticos (HTML, CSS, JS)
  - Gerados automaticamente via GitHub Actions

- **Backend**: Vercel hospeda apenas a API Django
  - URL: `https://boh-api.vercel.app/api/`
  - Endpoints da API para comunicação com frontend
  - Processamento da lógica de diálogo

## Configuração de Deploy

### 1. Secrets do GitHub

Configure os seguintes secrets no repositório:

- `VERCEL_TOKEN`: Token de acesso do Vercel
- `VERCEL_ORG_ID`: ID da organização Vercel
- `VERCEL_PROJECT_ID`: ID do projeto Vercel

### 2. Configuração do GitHub Pages

1. Vá em Settings → Pages
2. Selecione "GitHub Actions" como source
3. O workflow automaticamente publicará em `/docs`

### 3. Como funciona

#### Push para branch `ghpage`:

1. **GitHub Actions** executa simultaneamente:
   - Build da página estática (`build_github_pages.py`)
   - Deploy no GitHub Pages
   - Deploy da API no Vercel

2. **Resultado**:
   - Frontend disponível: `https://suzuma.github.io/Boh`
   - API disponível: `https://boh-api.vercel.app/api/`

### 4. Desenvolvimento Local

```bash
# Executar servidor Django localmente
python manage.py runserver

# Gerar build para GitHub Pages
python build_github_pages.py
```

### 5. URLs e Endpoints

- **Página Principal**: https://suzuma.github.io/Boh
- **API Django**: https://boh-api.vercel.app/api/dialogue/
- **CORS**: Configurado para permitir comunicação entre domínios

### 6. Arquivos Importantes

- `.github/workflows/deploy.yaml`: Configuração CI/CD
- `vercel.json`: Configuração apenas da API
- `api/wsgi.py`: WSGI otimizado para Vercel
- `build_github_pages.py`: Gerador de site estático
- `.vercelignore`: Ignora arquivos desnecessários no Vercel

### 7. Vantagens desta Arquitetura

- **Performance**: CDN do GitHub Pages para estáticos
- **Custo**: GitHub Pages gratuito, Vercel cobra só pela API
- **SEO**: URL limpa com nome do repositório
- **Separação**: Frontend e backend independentes
- **Escalabilidade**: Cada parte pode escalar separadamente

## Notas Importantes

- O JavaScript detecta automaticamente o ambiente (local/GitHub Pages/Vercel)
- CORS está configurado para permitir `https://suzuma.github.io`
- A API do Vercel roda em modo serverless (Django optimizado)
- Logs de erro disponíveis no painel do Vercel
