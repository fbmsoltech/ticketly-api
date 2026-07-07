# Deploy no Render

## Objetivo

Este guia prepara o Ticketly API para execucao no Render usando um Web Service
FastAPI, um banco PostgreSQL gerenciado, variaveis de ambiente e migrations
Alembic executadas no start da aplicacao.

## Pre-requisitos

- Conta no Render.
- Repositorio do projeto conectado ao Render.
- Projeto com dependencias Python instalaveis via `pip install -e .`.
- Nenhum secret real salvo no repositorio.

## Banco PostgreSQL no Render

Crie um banco PostgreSQL gerenciado no Render com o nome `ticketly-db`, ou use o
nome desejado e ajuste o `render.yaml`.

O `DATABASE_URL` da aplicacao deve vir da connection string gerada pelo Render
Postgres. Nao copie uma URL real para arquivos versionados.

## Web Service

Crie um Web Service apontando para o repositorio do Ticketly API.

Use os comandos:

```bash
pip install -e .
```

```bash
bash scripts/start.sh
```

O start script executa:

```bash
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
```

O Render fornece a variavel `PORT`; localmente, o script usa `8000` como
fallback.

## Variaveis de ambiente

Configure no Render:

```env
APP_NAME
APP_VERSION
APP_ENV
DATABASE_URL
JWT_SECRET_KEY
JWT_ALGORITHM
JWT_ACCESS_TOKEN_EXPIRE_MINUTES
LOG_LEVEL
ENABLE_REQUEST_LOGGING
ENABLE_METRICS
```

Valores esperados:

```env
APP_NAME=Ticketly API
APP_VERSION=0.1.0
APP_ENV=production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
LOG_LEVEL=INFO
ENABLE_REQUEST_LOGGING=true
ENABLE_METRICS=true
```

`DATABASE_URL` deve vir do Render Postgres. `JWT_SECRET_KEY` deve ser um segredo
forte criado no Render e nunca deve usar o valor `change-me-in-production`.

Arquivos `.env`, `.env.production` e `.env.render` nao devem ser enviados ao
Git.

## Uso do render.yaml

O arquivo `render.yaml` documenta o Blueprint com:

- Web Service `ticketly-api`;
- plano `free`;
- build command `pip install -e .`;
- start command `bash scripts/start.sh`;
- health check path `/api/v1/health/live`;
- banco `ticketly-db`;
- `DATABASE_URL` vindo do banco gerenciado;
- `JWT_SECRET_KEY` com `sync: false`.

O plano gratuito e adequado para portfolio e validacao, mas nao para producao
permanente. Ele pode ter cold starts, limites de recurso e politicas de
expiracao ou indisponibilidade conforme as regras atuais do Render.

## Alternativa manual via Dashboard

Se nao usar Blueprint:

1. Crie o Render PostgreSQL.
2. Crie o Web Service.
3. Configure o build command:

```bash
pip install -e .
```

4. Configure o start command:

```bash
bash scripts/start.sh
```

5. Configure as variaveis de ambiente.
6. Configure o health check path:

```text
/api/v1/health/live
```

## Permissao do start script

Em ambientes Unix, o script pode receber permissao de execucao:

```bash
chmod +x scripts/start.sh
```

Quando a permissao nao for preservada, use o start command:

```bash
bash scripts/start.sh
```

## Validacao pos-deploy

Depois do deploy, valide:

```bash
curl https://<render-service-url>/api/v1/health/live
curl https://<render-service-url>/api/v1/health/ready
curl https://<render-service-url>/api/v1/health
curl https://<render-service-url>/api/v1/metrics
```

`/api/v1/health/live` nao depende do banco e e usado pelo Render. O readiness e
o health completo consultam o banco, portanto podem indicar falha quando o
PostgreSQL estiver indisponivel ou quando migrations falharem.

## Troubleshooting

- Se o deploy falhar no start, verifique os logs do comando `alembic upgrade
  head`.
- Se a aplicacao rejeitar a inicializacao, confirme `APP_ENV=production`,
  `DATABASE_URL` e `JWT_SECRET_KEY`.
- Se `JWT_SECRET_KEY` estiver como `change-me-in-production`, substitua por um
  segredo forte.
- Se o banco nao conectar, confirme se `DATABASE_URL` veio do Render Postgres.
- Se o health check falhar no Render, confirme se o path configurado e
  `/api/v1/health/live`.
- Se `/api/v1/health/ready` retornar `503`, investigue conectividade e estado
  das migrations no banco.
