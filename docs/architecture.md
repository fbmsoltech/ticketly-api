# Arquitetura

## Visão geral

O Ticketly API será uma API REST moderna para gestão de tickets e suporte
técnico.

A arquitetura futura deverá seguir separação clara entre camadas, com foco em
legibilidade, testabilidade, manutenção e evolução incremental.

O projeto será organizado para evitar acoplamento excessivo entre HTTP, regra de
negócio e persistência de dados.

## Estado atual da arquitetura

A Fase 6 adiciona services para CRUD interno sobre os schemas e repositories
criados na Fase 5, sem implementar endpoints de domínio ou CRUD exposto por API.

Estrutura atual relevante:

```text
app/
|-- api/
|   `-- v1/
|       `-- routes/
|           `-- health.py
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
- `app/api/v1/routes/health.py`: expõe o endpoint simples de health check.
- `app/core/config.py`: centraliza configurações com Pydantic Settings,
  incluindo `DATABASE_URL`.
- `app/db/base.py`: define a base declarativa do SQLAlchemy.
- `app/db/session.py`: define engine e sessionmaker para uso futuro.
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

- endpoints de domínio;
- autenticação;
- autorização;
- CRUD exposto por API;
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

Na Fase 6, os services já oferecem CRUD interno básico e consultas específicas
das entidades base, mas ainda não são expostos por endpoints HTTP.

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

Nenhuma rota usa sessão de banco nesta fase. O uso em endpoints deverá acontecer
somente quando existirem models, repositories e services apropriados.

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
