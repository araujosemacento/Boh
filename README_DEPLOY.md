# Configuração de Deploy no Vercel com GitHub Actions

## Passos para configurar o deploy:

### 1. Configurar o projeto no Vercel
1. Instale a CLI do Vercel: `npm install -g vercel`
2. Faça login: `vercel login`
3. No diretório do projeto, execute: `vercel link`
4. Isso criará uma pasta `.vercel` com o arquivo `project.json`

### 2. Obter informações necessárias
1. Obtenha seu **Vercel Access Token** em: https://vercel.com/account/tokens
2. Na pasta `.vercel/project.json`, encontre:
   - `projectId` (será usado como `VERCEL_PROJECT_ID`)
   - `orgId` (será usado como `VERCEL_ORG_ID`)

### 3. Configurar secrets no GitHub
No seu repositório GitHub, vá para Settings > Secrets and variables > Actions e adicione:

- `VERCEL_TOKEN`: Seu token de acesso do Vercel
- `VERCEL_ORG_ID`: O orgId do arquivo project.json
- `VERCEL_PROJECT_ID`: O projectId do arquivo project.json

### 4. Como funciona o workflow
- **Push para branch `ghpage`**: Cria um deploy de produção
- **Pull Request para branch `ghpage`**: Cria um deploy de preview

### 5. Estrutura do projeto
- A página estática é construída usando `build_static.py`
- Os arquivos estáticos ficam em `static_site/`
- As APIs Django ficam disponíveis em `/api/`
- O servidor Django roda através do WSGI no Vercel

### 6. URLs
- **Página estática**: `https://seu-projeto.vercel.app/`
- **API Django**: `https://seu-projeto.vercel.app/api/`

## Notas importantes
- Certifique-se de que o `build_static.py` gere corretamente os arquivos em `static_site/`
- O Django roda em modo serverless no Vercel
- As chamadas para as APIs Django devem ser feitas para `/api/` endpoints
