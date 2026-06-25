# Arquitetura

## Visão geral

O Ticketly API será uma API REST moderna para gestão de tickets e suporte
técnico.

A arquitetura futura deverá seguir separação clara entre camadas, com foco em
legibilidade, testabilidade, manutenção e evolução incremental.

O projeto será organizado para evitar acoplamento excessivo entre HTTP, regra de
negócio e persistência de dados.

## Estado atual da arquitetura

A Fase 7 expõe endpoints CRUD REST para as entidades base já cobertas por
schemas, repositories e services, mantendo rotas finas e delegando operações de
aplicação para services.

Estrutura atual relevante:

```text
app/
|-- api/
|   `-- v1/
|       |-- dependencies/
|       |   `-- services.py
|       `-- routes/
|           |-- common.py
|           |-- customers.py
|           |-- health.py
|           |-- roles.py
|           |-- ticket_categories.py
|           |-- ticket_comments.py
|           |-- ticket_priorities.py
|           |-- ticket_statuses.py
|           |-- tickets.py
|           `-- users.py
|-- core/
|   `-- config.py
|-- db/
|   |-- __init__.py
|   |-- base.py
|   `-- session.py
|-- models/
|   |-- customer.py
|   |-- role.py
|   |-- ticket.py
|   |-- ticket_category.py
|   |-- ticket_comment.py
|   |-- ticket_priority.py
|   |-- ticket_status.py
|   `-- user.py
|-- repositories/
|   |-- base.py
|   |-- customer.py
|   |-- role.py
|   |-- ticket.py
|   |-- ticket_category.py
|   |-- ticket_comment.py
|   |-- ticket_priority.py
|   |-- ticket_status.py
|   `-- user.py
|-- schemas/
|   |-- base.py
|   |-- customer.py
|   |-- role.py
|   |-- ticket.py
|   |-- ticket_category.py
|   |-- ticket_comment.py
|   |-- ticket_priority.py
|   |-- ticket_status.py
|   `-- user.py
|-- services/
|   |-- base.py
|   |-- customer.py
|   |-- role.py
|   |-- ticket.py
|   |-- ticket_category.py
|   |-- ticket_comment.py
|   |-- ticket_priority.py
|   |-- ticket_status.py
|   `-- user.py
`-- main.py
alembic/
|-- versions/
|   |-- .gitkeep
|   `-- 0001_initial_database_setup.py
|   `-- 0002_initial_domain_models.py
|-- env.py
`-- script.py.mako
```

Responsabilidades atuais:

- `app/main.py`: cria a instância FastAPI e registra as rotas da versão v1.
- `app/api/v1/dependencies/services.py`: monta services a partir da sessão de
  banco da requisição.
- `app/api/v1/routes/health.py`: expõe o endpoint simples de health check.
- `app/api/v1/routes/`: expõe endpoints CRUD REST para as entidades base.
- `app/core/config.py`: centraliza configurações com Pydantic Settings,
  incluindo `DATABASE_URL`.
- `app/db/base.py`: define a base declarativa do SQLAlchemy.
- `app/db/session.py`: define engine, sessionmaker e ciclo transacional da
  sessão por requisição.
- `app/models/`: define as entidades persistidas e seus relacionamentos.
- `app/schemas/`: define contratos Pydantic v2 de criação, atualização e
  leitura para uso futuro pela API.
- `app/repositories/`: encapsula consultas e operações básicas de persistência
  com SQLAlchemy.
- `app/services/`: coordena casos de uso internos de CRUD usando schemas e
  repositories.
- `alembic/`: contém a configuração inicial de migrations.

O endpoint de health check não consulta banco de dados nem qualquer dependência
externa nesta fase.

Ainda não fazem parte desta fase:

- autenticação;
- autorização;
- testes automatizados;
- Docker;
- Docker Compose;
- GitHub Actions.

## Separaçao de responsabilidades

### API routes

As rotas serão responsáveis pela camada HTTP.

Responsabilidades esperadas:

- declarar endpoints;
- receber parâmetros de rota, query e corpo da requisição;
- aplicar dependências;
- chamar services;
- retornar respostas HTTP.

Rotas não devem conter regra de negócio.

### Services

Services concentram as regras de negócio e os casos de uso da aplicação.

Responsabilidades esperadas:

- validar regras do domínio;
- coordenar fluxos como criação, atribuição, comentário e mudança de status de
  tickets;
- chamar repositories;
- decidir erros de negócio;
- manter a lógica fora das rotas.

Na Fase 7, os services são chamados pelas rotas HTTP para expor CRUD REST das
entidades base.

### Repositories

Repositories concentrarão o acesso ao banco de dados.

Responsabilidades esperadas:

- criar consultas;
- buscar registros;
- persistir entidades;
- atualizar dados;
- remover ou desativar registros quando aplicável.

Repositories não devem conter regra de negócio. Eles devem oferecer operações de
persistência para que os services coordenem o comportamento da aplicação.

### Models

Models representarão tabelas e relacionamentos do banco de dados usando
SQLAlchemy 2.x.

Responsabilidades esperadas:

- mapear entidades persistidas;
- definir colunas;
- definir relacionamentos;
- representar constraints relevantes.

Models não devem ser usados como schemas públicos da API.

### Schemas

Schemas representarão contratos de entrada e saída da API usando Pydantic v2.

Responsabilidades esperadas:

- validar payloads de entrada;
- formatar respostas;
- separar dados internos do banco de dados dos contratos públicos da API.

## Camada de banco

A camada `app/db/` prepara a persistência relacional para fases futuras.

Nesta fase ela contém apenas:

- uma base declarativa do SQLAlchemy;
- uma engine configurada por `DATABASE_URL`;
- um `sessionmaker` para criação de sessões.

As rotas CRUD recebem uma sessão por dependência. A sessão confirma a transação
ao final de requisições bem-sucedidas e executa rollback quando ocorre exceção.

## Por que evitar controller gordo

Controller gordo ocorre quando rotas acumulam validação de regra de negócio,
acesso ao banco, transformação de dados e decisões de fluxo.

Esse padrão deve ser evitado porque:

- dificulta testes;
- aumenta duplicação;
- acopla HTTP com regra de negócio;
- torna refatorações mais arriscadas;
- reduz a clareza sobre onde cada decisão do sistema acontece.

No Ticketly API, rotas devem ser finas e delegar a execução para services.

## Fluxo esperado de uma requisição

Fluxo futuro esperado:

```text
Cliente HTTP
  |
API route
  |
Schema de entrada
  |
Service
  |
Repository
  |
Banco de dados
  |
Repository
  |
Service
  |
Schema de saída
  |
Resposta HTTP
```

## Estrutura futura de pastas

```text
ticketly-api/
|-- app/
|   |-- api/
|   |   `-- v1/
|   |       |-- routes/
|   |       `-- dependencies/
|   |-- core/
|   |-- db/
|   |-- models/
|   |-- repositories/
|   |-- schemas/
|   |-- services/
|   |-- observability/
|   `-- main.py
|-- alembic/
|-- docs/
|-- tests/
|-- scripts/
|-- .github/
|   `-- workflows/
|-- AGENTS.md
|-- README.md
|-- pyproject.toml
|-- docker-compose.yml
|-- Dockerfile
`-- .env.example
```

O nome da pasta raiz pode variar conforme o ambiente local. A organização
interna deverá respeitar essa separação conforme as fases evoluírem.
