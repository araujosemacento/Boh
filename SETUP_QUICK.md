# BOH! Dialogue System - Quick Setup

## ✅ Estrutura Implementada

### Frontend: GitHub Pages
- URL: `https://araujosemacento.github.io/Boh`
- Arquivos estáticos gerados automaticamente

### Backend: Vercel API
- URL: `https://boh-dialogue-api.vercel.app/api/`
- Django API serverless

## 🚀 Deploy Automático

### Branch: `ghpage`
Todo push para `ghpage` executa:
1. Build do site estático → GitHub Pages
2. Deploy da API → Vercel

## 📋 Configuração Necessária

### GitHub Secrets:
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID` 
- `VERCEL_PROJECT_ID`

### GitHub Pages:
- Settings → Pages → GitHub Actions

## 🎯 URLs Finais

- **Página**: https://araujosemacento.github.io/Boh
- **API**: https://boh-dialogue-api.vercel.app/api/dialogue/

## 🔧 Desenvolvimento Local

```bash
python manage.py runserver
```

O JavaScript detecta automaticamente o ambiente e usa a API correta!
