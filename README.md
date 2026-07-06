# Ticketly API

Ticketly API é uma API REST moderna para gestão de tickets e suporte técnico.

Este projeto tem como objetivo construir um backend profissional de portfólio,
com arquitetura limpa, domínio bem documentado, CRUD completo, autenticação,
autorização, banco relacional, testes automatizados, Docker, CI/CD e deploy.

> Status: API com CRUD das entidades base, testes automatizados, ambiente local
> com Docker Compose e CI com GitHub Actions.

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
- `docs/business-flow.md`
- `docs/database.md`
- `docs/development-guidelines.md`
- `docs/testing.md`
- `docs/ci.md`
- `docs/schemas-and-repositories.md`
- `docs/services.md`

## Execução local

O projeto usa Python 3.13+ e inclui a modelagem inicial do domínio, schemas
Pydantic v2, repositories, services, endpoints CRUD REST para as entidades base,
testes automatizados com Pytest e ambiente local com Docker Compose. Ainda não
há autenticação, autorização, CD ou deploy.

Para subir o ambiente local completo com API, PostgreSQL principal e PostgreSQL
para testes:

```bash
docker compose up --build
```

A API ficará disponível em:

```text
http://localhost:8000
```

O health check fica em:

```text
GET http://localhost:8000/api/v1/health
```

Para executar os testes usando o banco PostgreSQL de testes do Docker Compose:

```bash
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

Endpoints disponíveis:

- `GET /api/v1/health`
- CRUD de `roles` em `/api/v1/roles`
- CRUD de `users` em `/api/v1/users`
- CRUD de `customers` em `/api/v1/customers`
- CRUD de `ticket-statuses` em `/api/v1/ticket-statuses`
- CRUD de `ticket-priorities` em `/api/v1/ticket-priorities`
- CRUD de `ticket-categories` em `/api/v1/ticket-categories`
- CRUD de `tickets` em `/api/v1/tickets`
- CRUD de `ticket-comments` em `/api/v1/ticket-comments`

O health check não consulta o banco de dados.

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
mypy .
pytest
```

## CI

O projeto possui integração contínua em `.github/workflows/ci.yml`.

A pipeline executa em pull requests e pushes para `main`, usando Python 3.13 e
PostgreSQL temporário para validar:

- Ruff;
- Black;
- Mypy;
- migrations com Alembic;
- testes com Pytest.

O workflow não realiza deploy, publicação de imagens Docker ou uso de secrets
reais.
