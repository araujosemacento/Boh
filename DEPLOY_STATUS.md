# BOH! Dialogue System - Final Configuration

## ✅ Status da Configuração

### Estrutura Implementada - GitHub Pages + Vercel API

#### Frontend (GitHub Pages)
- **URL**: `https://suzuma.github.io/Boh`
- **Fonte**: Arquivos estáticos gerados por `build_github_pages.py`
- **Deploy**: Automático via GitHub Actions

#### Backend (Vercel API)
- **URL**: `https://boh-dialogue-api.vercel.app`
- **Endpoints**: `/api/dialogue/`
- **Deploy**: Automático via GitHub Actions

### Arquivos Principais Configurados

✅ `.github/workflows/deploy.yaml` - CI/CD pipeline
✅ `vercel.json` - Configuração da API Vercel
✅ `api/wsgi.py` - WSGI otimizado para Vercel
✅ `build_github_pages.py` - Gerador de site estático
✅ `dialogue/static/dialogue/js/boh_dialogue.js` - Cliente JavaScript
✅ `.vercelignore` - Otimização do deploy Vercel

### Configuração de URLs

- **Frontend**: `https://suzuma.github.io/Boh`
- **API**: `https://boh-dialogue-api.vercel.app/api/dialogue/`
- **CORS**: Configurado para permitir comunicação entre domínios

## 🚀 Deploy

### Secrets Necessários no GitHub

```
VERCEL_TOKEN=<seu_token_vercel>
VERCEL_ORG_ID=<id_da_organizacao>
VERCEL_PROJECT_ID=<id_do_projeto>
```

### Como fazer deploy

1. **Configure os secrets** no GitHub repository
2. **Push para branch `ghpage`**:
   ```bash
   git checkout ghpage
   git add .
   git commit -m "Deploy configuration"
   git push origin ghpage
   ```

3. **Monitore os deploys**:
   - GitHub Actions: Deploy do frontend
   - Vercel Dashboard: Deploy da API

## 🔧 Desenvolvimento

### Local
```bash
python manage.py runserver
# Acesse: http://localhost:8000/dialogue/
```

### Build para GitHub Pages
```bash
python build_github_pages.py
# Gera arquivos em ./docs/
```

### Verificação
```bash
python check_config.py
# Verifica se tudo está configurado corretamente
```

## 📊 Monitoramento

### Logs de Deploy
- **GitHub Actions**: Aba "Actions" do repositório
- **Vercel**: Dashboard do projeto no Vercel

### URLs de Teste
- **Frontend**: https://suzuma.github.io/Boh
- **API Health**: https://boh-dialogue-api.vercel.app/api/dialogue/

## 🔄 Fluxo Completo

1. **Desenvolvimento** → `main` branch
2. **Deploy** → Push para `ghpage` branch
3. **GitHub Actions** executa:
   - Build do site estático
   - Deploy no GitHub Pages
   - Deploy da API no Vercel
4. **Resultado**: Site funcionando com comunicação frontend ↔ API

---

**Status**: ✅ Pronto para deploy
