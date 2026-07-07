# Ticketly API

Ticketly API é uma API REST moderna para gestão de tickets e suporte técnico.

Este projeto tem como objetivo construir um backend profissional de portfólio,
com arquitetura limpa, domínio bem documentado, CRUD completo, autenticação,
autorização, banco relacional, testes automatizados, Docker, CI/CD e deploy.

> Status: API com CRUD das entidades base, CRUD de tickets com regras de
> negocio, autenticacao JWT, autorizacao por papeis, observabilidade basica,
> testes automatizados, ambiente local com Docker Compose, CI com GitHub
> Actions e preparo de deploy no Render.

## Stack planejada

- Python 3.13+
- FastAPI
- SQLAlchemy 2.x
- PostgreSQL
- Alembic
- Pydantic v2
- Pytest
- Docker
- Docker Compose
- Ruff
- Black
- Mypy
- GitHub Actions
- Render

## Visão geral do domínio

O Ticketly API será uma plataforma backend para organizar o atendimento de
suporte técnico por meio de tickets.

O domínio previsto envolve clientes, atendentes, administradores, tickets,
comentários, categorias, status, prioridades e permissões baseadas em papéis.

As principais entidades previstas são:

- User
- Role
- Customer
- Ticket
- TicketComment
- TicketCategory
- TicketStatus
- TicketPriority

## Objetivo do projeto

O objetivo é demonstrar a construção incremental de uma API backend realista,
seguindo boas práticas de arquitetura, qualidade, testes, documentação e
entrega.

O projeto deverá evoluir incrementalmente, evitando misturar responsabilidades e
evitando implementar funcionalidades antes do momento planejado.

## Roadmap

- Documentação base do projeto.
- Setup inicial Python/FastAPI, estrutura base da aplicação e ferramentas de
  qualidade.
- Infraestrutura inicial de banco com PostgreSQL, SQLAlchemy 2.x e Alembic.
- Modelagem inicial das entidades.
- Schemas Pydantic v2 e repositories iniciais.
- Services e CRUD interno das entidades base.
- Endpoints CRUD REST das entidades base.
- Testes automatizados.
- Docker e Docker Compose para desenvolvimento local.
- CI com GitHub Actions.
- Autenticação e autorização.
- CD com GitHub Actions.
- Deploy no Render.

## Documentação

A documentação técnica e de negócio fica na pasta `docs/`.

Documentos iniciais:

- `docs/architecture.md`
- `docs/authentication.md`
- `docs/api-endpoints.md`
- `docs/business-flow.md`
- `docs/database.md`
- `docs/development-guidelines.md`
- `docs/testing.md`
- `docs/ci.md`
- `docs/tickets.md`
- `docs/ticket-comments.md`
- `docs/observability.md`
- `docs/schemas-and-repositories.md`
- `docs/services.md`
- `docs/deployment.md`
- `docs/seed.md`

## Execução local

O projeto usa Python 3.13+ e inclui a modelagem inicial do dominio, schemas
Pydantic v2, repositories, services, endpoints CRUD REST para as entidades base,
autenticacao JWT, autorizacao por papeis, testes automatizados com Pytest e
ambiente local com Docker Compose. O deploy no Render e documentado
separadamente e nao e executado pelo GitHub Actions.

Para subir o ambiente local completo com API, PostgreSQL principal e PostgreSQL
para testes:

```bash
docker compose up --build
```

A API ficará disponível em:

```text
http://localhost:8000
```

Os endpoints de observabilidade ficam em:

```text
GET http://localhost:8000/api/v1/health
GET http://localhost:8000/api/v1/health/live
GET http://localhost:8000/api/v1/health/ready
GET http://localhost:8000/api/v1/metrics
GET http://localhost:8000/api/v1/docs
```

Exemplos com `curl`:

```bash
curl http://localhost:8000/api/v1/health
curl http://localhost:8000/api/v1/health/live
curl http://localhost:8000/api/v1/health/ready
curl http://localhost:8000/api/v1/metrics
```

Para executar os testes usando o banco PostgreSQL de testes do Docker Compose:

```bash
docker compose exec api pytest -m unit
docker compose exec api pytest -m integration
docker compose exec api pytest
docker compose --profile test run --rm test
```

Para parar os containers:

```bash
docker compose down
```

Para remover também os volumes locais dos bancos:

```bash
docker compose down -v
```

Também é possível executar a aplicação diretamente no ambiente Python local.

Para preparar o ambiente local:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

No Windows PowerShell, a ativação do ambiente virtual pode ser feita com:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

Copie as variáveis de exemplo para um arquivo `.env` local e ajuste quando
necessário:

```bash
cp .env.example .env
```

No Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Para iniciar a API:

```bash
uvicorn app.main:app --reload
```

## Seed inicial

Consulte `docs/seed.md`.

Exemplo local para criar um administrador inicial:

```env
CREATE_INITIAL_ADMIN=true
INITIAL_ADMIN_NAME=Admin
INITIAL_ADMIN_EMAIL=admin@example.com
INITIAL_ADMIN_PASSWORD=uma-senha-forte
```

Nao use senha real em arquivos versionados. O seed roda automaticamente no
`scripts/start.sh` depois das migrations e nao duplica dados.

Endpoints disponíveis:

- `GET /api/v1/health`
- `GET /api/v1/health/live`
- `GET /api/v1/health/ready`
- `GET /api/v1/metrics`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- CRUD de `roles` em `/api/v1/roles`
- CRUD de `users` em `/api/v1/users`
- CRUD de `customers` em `/api/v1/customers`
- CRUD de `ticket-statuses` em `/api/v1/ticket-statuses`
- CRUD de `ticket-priorities` em `/api/v1/ticket-priorities`
- CRUD de `ticket-categories` em `/api/v1/ticket-categories`
- CRUD de `tickets` em `/api/v1/tickets`
- Comentarios de tickets em `/api/v1/tickets/{ticket_id}/comments`

O health check completo e o readiness consultam o banco de dados. O liveness nao
consulta dependencias externas. As metricas ficam em memoria e sao publicas para
uso local; em producao, devem ser protegidas ou expostas apenas internamente.

## Deploy no Render

Consulte `docs/deployment.md`.

Endpoints para validacao apos o deploy:

```text
/api/v1/health/live
/api/v1/health/ready
/api/v1/docs
```

A documentacao interativa do FastAPI permanece disponivel em `/api/v1/docs`.

## Autenticacao e autorizacao

A API usa JWT com Bearer Token. Configure as variaveis abaixo no `.env`:

```env
JWT_SECRET_KEY=change-me-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Use um segredo forte fora do ambiente local. Nunca versione secrets reais.

Papeis existentes:

- `ADMIN`
- `AGENT`
- `CUSTOMER`

Rotas protegidas:

- `/api/v1/roles`: somente `ADMIN`;
- `/api/v1/users`: somente `ADMIN`;
- `/api/v1/ticket-categories`: somente `ADMIN`;
- `/api/v1/ticket-statuses`: somente `ADMIN`;
- `/api/v1/ticket-priorities`: somente `ADMIN`;
- `/api/v1/customers`: `ADMIN` ou `AGENT`.
- `/api/v1/tickets`: `ADMIN` ou `AGENT`, exceto `DELETE`, que exige `ADMIN`.
- `/api/v1/tickets/{ticket_id}/comments`: `ADMIN` ou `AGENT`, exceto `DELETE`,
  que exige `ADMIN`.

Os health checks, `/api/v1/metrics` e `/api/v1/auth/login` sao publicos.

O seed inicial cria as roles base automaticamente. Um usuario admin inicial pode
ser criado por variaveis de ambiente quando `CREATE_INITIAL_ADMIN=true`.

Login:

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin123"
  }'
```

Uso do token:

```bash
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer <TOKEN>"
```

No Swagger, clique em Authorize e informe:

```text
Bearer <TOKEN>
```

## Tickets

O CRUD de tickets fica em `/api/v1/tickets` e exige Bearer Token.

Exemplo de criacao:

```bash
curl -X POST http://localhost:8000/api/v1/tickets \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Cannot access dashboard",
    "description": "The dashboard returns an error.",
    "customer_id": 1,
    "category_id": 1,
    "status_id": 1,
    "priority_id": 1,
    "assigned_agent_id": 2
  }'
```

`assigned_agent_id` e opcional. Quando informado, deve apontar para usuario com
papel `ADMIN` ou `AGENT`. A abertura direta por cliente autenticado sera tratada
separadamente; neste momento o CRUD de tickets e administrativo/de atendimento.

## Comentarios de tickets

Comentarios ficam aninhados em tickets e exigem Bearer Token.

Exemplo de criacao:

```bash
curl -X POST http://localhost:8000/api/v1/tickets/1/comments \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "We are checking this ticket.",
    "is_internal": false
  }'
```

O autor e sempre o usuario autenticado. O body nao aceita sobrescrever
`author_user_id`. Comentarios internos (`is_internal=true`) sao visiveis para
`ADMIN` e `AGENT`; o acesso de `CUSTOMER` aos comentarios sera tratado em fluxo
proprio.

## Banco de dados

A infraestrutura de banco usa PostgreSQL, SQLAlchemy 2.x e Alembic:

- `DATABASE_URL` configurado via ambiente;
- base declarativa em `app/db/base.py`;
- engine, sessionmaker e ciclo transacional por requisição em
  `app/db/session.py`;
- configuração inicial do Alembic em `alembic/`;
- models iniciais em `app/models/`;
- repositories iniciais em `app/repositories/`;
- schemas Pydantic v2 em `app/schemas/`;
- services de CRUD interno em `app/services/`;
- migration real em `alembic/versions/0002_initial_domain_models.py`.
- Docker Compose com um banco principal em `db` e um banco isolado de testes em
  `test-db`.

Para validar a configuração do Alembic sem aplicar mudanças:

```bash
alembic current
```

As tabelas iniciais representam usuários, papéis, clientes, tickets,
comentários, categorias, status e prioridades.

Antes de executar `alembic upgrade head`, confirme que o banco e o usuário do
`DATABASE_URL` existem no PostgreSQL local. Veja o passo a passo em
`docs/database.md`.

## Qualidade

Ferramentas configuradas:

- Ruff
- Black
- Mypy
- Pytest
- GitHub Actions

Comandos recomendados:

```bash
ruff check .
black --check .
mypy app tests
pytest -m unit
pytest -m integration
pytest
```

Testes unitarios ficam em `tests/unit`, usam o marker `unit` e nao dependem de
banco ou infraestrutura externa. Testes de integracao ficam em
`tests/integration`, usam o marker `integration` e validam API, services,
repositories e PostgreSQL de teste.

## CI

O projeto possui integração contínua em `.github/workflows/ci.yml`.

A pipeline executa em pull requests e pushes para `main`, usando Python 3.13 e
PostgreSQL temporário para validar:

- Ruff;
- Black;
- Mypy;
- testes unitarios;
- migrations com Alembic;
- testes de integracao.

O workflow não realiza deploy, publicação de imagens Docker ou uso de secrets
reais.
