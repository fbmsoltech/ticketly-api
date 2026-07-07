# Arquitetura

## Visão geral

O Ticketly API será uma API REST moderna para gestão de tickets e suporte
técnico.

A arquitetura segue separação clara entre camadas, com foco em legibilidade,
testabilidade, manutenção e evolução incremental.

O projeto será organizado para evitar acoplamento excessivo entre HTTP, regra de
negócio e persistência de dados.

## Estado atual da arquitetura

A aplicação expõe endpoints CRUD REST para as entidades base já cobertas por
schemas, repositories e services, mantendo rotas finas e delegando operações de
aplicação para services. O ambiente local usa Docker Compose para executar a API
e bancos PostgreSQL separados para desenvolvimento e testes. A qualidade do
projeto é validada por uma pipeline de CI no GitHub Actions. O deploy e
preparado para o Render com Web Service FastAPI, Render PostgreSQL e migrations
executadas antes do Uvicorn.

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
|           |-- metrics.py
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
|-- observability/
|   |-- logging.py
|   |-- metrics.py
|   `-- middleware.py
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
|   |-- ticket_service.py
|   |-- ticket_category.py
|   |-- ticket_comment.py
|   |-- ticket_comment_service.py
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
docker-compose.yml
Dockerfile
render.yaml
scripts/
`-- start.sh
.github/
`-- workflows/
    `-- ci.yml
```

Responsabilidades atuais:

- `app/main.py`: cria a instância FastAPI e registra as rotas da versão v1.
- `app/api/v1/dependencies/services.py`: monta services a partir da sessão de
  banco da requisição.
- `app/api/v1/routes/health.py`: expoe health check completo, liveness e
  readiness.
- `app/api/v1/routes/metrics.py`: expoe metricas basicas em memoria.
- `app/api/v1/routes/`: expõe endpoints CRUD REST para as entidades base.
- `app/core/config.py`: centraliza configurações com Pydantic Settings,
  incluindo `DATABASE_URL` e flags basicas de observabilidade.
- `app/db/base.py`: define a base declarativa do SQLAlchemy.
- `app/db/session.py`: define engine, sessionmaker e ciclo transacional da
  sessão por requisição.
- `app/models/`: define as entidades persistidas e seus relacionamentos.
- `app/observability/`: concentra logging estruturado, middleware de logging de
  requisicoes e coletor de metricas em memoria.
- `app/schemas/`: define contratos Pydantic v2 de criação, atualização e
  leitura para uso futuro pela API.
- `app/repositories/`: encapsula consultas e operações básicas de persistência
  com SQLAlchemy.
- `app/services/`: coordena casos de uso internos de CRUD usando schemas e
  repositories.
- `alembic/`: contém a configuração inicial de migrations.
- `Dockerfile`: define a imagem local da API.
- `docker-compose.yml`: orquestra a API, o PostgreSQL principal e o PostgreSQL
  de testes.
- `render.yaml`: documenta a infraestrutura Render via Blueprint.
- `scripts/start.sh`: executa migrations Alembic e inicia Uvicorn no deploy.
- `.github/workflows/ci.yml`: valida qualidade, migrations e testes no GitHub
  Actions.

O health check completo e readiness consultam o banco de dados por meio de
service. Liveness verifica apenas se a aplicacao esta viva.

## Visao de deploy

```text
Render Web Service
        |
Ticketly API
        |
Render PostgreSQL
```

O Render Web Service executa o build com `pip install -e .` e inicia a aplicacao
com `bash scripts/start.sh`. O script roda `alembic upgrade head` antes do
Uvicorn para manter o schema do Render PostgreSQL alinhado as migrations
versionadas.

O health check configurado no Render usa `/api/v1/health/live`, que nao consulta
o banco. A verificacao de readiness continua em `/api/v1/health/ready` e valida
a dependencia externa PostgreSQL.

## Integração contínua

A pipeline de CI executa fora da aplicação, sem alterar as responsabilidades das
camadas internas.

Ela valida:

- qualidade estática com Ruff, Black e Mypy;
- aplicação das migrations com Alembic;
- comportamento automatizado com Pytest.

O workflow usa um PostgreSQL temporário do GitHub Actions para validar
migrations e testes sem depender de banco de produção.

O deploy no Render e acionado pelo proprio Render via Blueprint, push conectado
ao servico ou configuracao manual no Dashboard. O GitHub Actions permanece
responsavel apenas por integracao continua.

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

Os services são chamados pelas rotas HTTP para expor CRUD REST das entidades
base.

O fluxo de tickets usa `TicketService` para validar customer, categoria, status,
prioridade e usuario responsavel antes de persistir criacoes ou atualizacoes.
Rotas de tickets nao acessam repositories diretamente e aplicam somente
dependencias HTTP de autenticacao e autorizacao.

O fluxo de comentarios usa `TicketCommentService` para validar ticket, validar
autor usuario, aplicar a autoria do usuario autenticado, filtrar comentarios
internos quando solicitado e manter commits/rollbacks das escritas fora das
rotas. O repository de comentarios apenas encapsula consultas por ticket.

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

### Observability

A camada `app/observability/` concentra recursos transversais de visibilidade da
aplicacao:

- configuracao de logging com a biblioteca padrao;
- middleware de logging de requisicoes HTTP;
- coletor simples de metricas em memoria.

Essa camada nao contem regras de negocio de dominio e nao registra bodies,
senhas, tokens ou headers sensiveis.

## Camada de banco

A camada `app/db/` prepara a persistência relacional da aplicação.

A camada contém:

- uma base declarativa do SQLAlchemy;
- uma engine configurada por `DATABASE_URL`;
- um `sessionmaker` para criação de sessões.

As rotas CRUD recebem uma sessão por dependência. A sessão confirma a transação
ao final de requisições bem-sucedidas e executa rollback quando ocorre exceção.
No ambiente Docker Compose, essa sessão usa o serviço `db` por meio da variável
`DATABASE_URL`.

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

## Fluxo de tickets

```text
Cliente autenticado
  |
Route /api/v1/tickets
  |
require_roles ou require_admin
  |
TicketCreate ou TicketUpdate
  |
TicketService
  |
Repositories de ticket e entidades relacionadas
  |
Banco de dados
```

O service concentra as regras de existencia das entidades relacionadas e a regra
de atribuicao para `ADMIN` ou `AGENT`. O repository apenas encapsula consultas e
filtros de persistencia.

## Fluxo de comentarios de tickets

```text
Cliente autenticado
  |
Route /api/v1/tickets/{ticket_id}/comments
  |
require_roles ou require_admin
  |
TicketCommentCreate ou TicketCommentUpdate
  |
TicketCommentService
  |
TicketRepository, UserRepository e TicketCommentRepository
  |
Banco de dados
```

A rota define HTTP, autenticacao e autorizacao. O service garante que o ticket
existe, que o autor usuario existe e que a criacao usa o usuario autenticado
como autor. Comentarios internos podem ser filtrados via `include_internal`.

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

## Camada de seguranca

A autenticacao e autorizacao ficam separadas entre core, services e dependencies
HTTP.

Componentes principais:

- `app/core/security.py`: gera hash de senha, valida senha, cria JWT e decodifica
  JWT sem importar FastAPI;
- `app/services/auth_service.py`: autentica usuario por e-mail e senha, valida
  usuario ativo e gera access token;
- `app/services/user.py`: coordena CRUD de usuarios, valida role, valida e-mail
  duplicado e salva apenas `hashed_password`;
- `app/api/v1/dependencies/auth.py`: converte Bearer Token em usuario atual e
  aplica autorizacao por papel;
- `app/api/v1/routes/auth.py`: expoe login e usuario atual;
- `app/api/v1/routes/users.py`: expoe CRUD de usuarios protegido por `ADMIN`.

Fluxo de autenticacao:

```text
Cliente
  |
POST /api/v1/auth/login
  |
AuthService.authenticate
  |
UserRepository.get_by_email
  |
verify_password
  |
create_access_token
  |
TokenResponse
```

Fluxo de autorizacao:

```text
Cliente com Bearer Token
  |
Dependency get_current_user
  |
decode_access_token
  |
UserRepository.get
  |
require_roles
  |
Endpoint protegido
```

As rotas continuam finas: elas recebem entrada HTTP, aplicam dependencies,
chamam services e retornam schemas publicos. Regras de negocio de autenticacao e
usuarios ficam nos services.
