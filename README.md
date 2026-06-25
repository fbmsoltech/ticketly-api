# Ticketly API

Ticketly API é uma API REST moderna para gestão de tickets e suporte técnico.

Este projeto tem como objetivo construir um backend profissional de portfólio, com arquitetura limpa, domínio bem documentado, CRUD completo, autenticação, autorização, banco relacional, testes automatizados, Docker, CI/CD e deploy.

> Status: projeto em construção.

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

O Ticketly API será uma plataforma backend para organizar o atendimento de suporte técnico por meio de tickets.

O domínio previsto envolve clientes, atendentes, administradores, tickets, comentários, categorias, status, prioridades e permissões baseadas em papéis.

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

O objetivo é demonstrar a construção incremental de uma API backend realista, seguindo boas práticas de arquitetura, qualidade, testes, documentação e entrega.

O projeto deverá evoluir por fases, evitando misturar responsabilidades e evitando implementar funcionalidades antes do momento planejado.

## Roadmap inicial por fases

- Fase 1: documentação base do projeto.
- Fase 2: configuração inicial do ambiente Python e ferramentas de qualidade.
- Fase 3: estrutura base da aplicação FastAPI.
- Fase 4: configuração de banco de dados, SQLAlchemy e Alembic.
- Fase 5: modelagem inicial das entidades.
- Fase 6: CRUDs principais.
- Fase 7: autenticação e autorização.
- Fase 8: testes automatizados.
- Fase 9: Docker e Docker Compose.
- Fase 10: CI/CD com GitHub Actions.
- Fase 11: deploy no Render.

## Documentação

A documentação técnica e de negócio ficará na pasta `docs/`.

Documentos iniciais:

- `docs/architecture.md`
- `docs/business-flow.md`
- `docs/development-guidelines.md`
