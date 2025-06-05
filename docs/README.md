# BOH! Dialogue System

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
