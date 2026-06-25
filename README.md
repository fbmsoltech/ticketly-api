# Ticketly API

Ticketly API é uma API REST moderna para gestão de tickets e suporte técnico.

Este projeto tem como objetivo construir um backend profissional de portfólio,
com arquitetura limpa, domínio bem documentado, CRUD completo, autenticação,
autorização, banco relacional, testes automatizados, Docker, CI/CD e deploy.

> Status: Fase 6 concluída - services e CRUD interno das entidades base.

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

O projeto deverá evoluir por fases, evitando misturar responsabilidades e
evitando implementar funcionalidades antes do momento planejado.

## Roadmap inicial por fases

- Fase 1: documentação base do projeto.
- Fase 2: setup inicial Python/FastAPI, estrutura base da aplicação e
  ferramentas de qualidade.
- Fase 3: infraestrutura inicial de banco com PostgreSQL, SQLAlchemy 2.x e
  Alembic.
- Fase 4: modelagem inicial das entidades.
- Fase 5: schemas Pydantic v2 e repositories iniciais.
- Fase 6: services e CRUD interno das entidades base.
- Fase 7: autenticação e autorização.
- Fase 8: testes automatizados.
- Fase 9: Docker e Docker Compose.
- Fase 10: CI/CD com GitHub Actions.
- Fase 11: deploy no Render.

## Documentação

A documentação técnica e de negócio fica na pasta `docs/`.

Documentos iniciais:

- `docs/architecture.md`
- `docs/business-flow.md`
- `docs/database.md`
- `docs/development-guidelines.md`
- `docs/schemas-and-repositories.md`
- `docs/services.md`

## Execução local

Esta fase usa Python 3.13+ e inclui a modelagem inicial do domínio, schemas
Pydantic v2, repositories iniciais e services para CRUD interno. Ainda não há
endpoints de domínio, autenticação, CRUD exposto por API, testes automatizados,
Docker ou CI/CD.

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

Endpoint disponível nesta fase:

- `GET /api/v1/health`

O health check não consulta o banco de dados nesta fase.

## Banco de dados

A infraestrutura de banco usa PostgreSQL, SQLAlchemy 2.x e Alembic:

- `DATABASE_URL` configurado via ambiente;
- base declarativa em `app/db/base.py`;
- engine e sessionmaker em `app/db/session.py`;
- configuração inicial do Alembic em `alembic/`;
- models iniciais em `app/models/`;
- repositories iniciais em `app/repositories/`;
- schemas Pydantic v2 em `app/schemas/`;
- services de CRUD interno em `app/services/`;
- migration real em `alembic/versions/0002_initial_domain_models.py`.

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

Comandos recomendados:

```bash
ruff check .
black --check .
mypy .
```
