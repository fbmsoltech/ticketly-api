# Arquitetura

## Visão geral

O Ticketly API será uma API REST moderna para gestão de tickets e suporte técnico.

A arquitetura futura deverá seguir separação clara entre camadas, com foco em legibilidade, testabilidade, manutenção e evolução incremental.

O projeto será organizado para evitar acoplamento excessivo entre HTTP, regra de negócio e persistência de dados.

## Estado atual da arquitetura

A Fase 2 introduz a aplicação FastAPI mínima e a estrutura inicial do pacote
`app`.

Estrutura criada nesta fase:

```text
app/
|-- api/
|   `-- v1/
|       `-- routes/
|           `-- health.py
|-- core/
|   `-- config.py
`-- main.py
```

Responsabilidades atuais:

- `app/main.py`: cria a instância FastAPI e registra as rotas da versão v1.
- `app/api/v1/routes/health.py`: expõe o endpoint simples de health check.
- `app/core/config.py`: centraliza configurações iniciais com Pydantic Settings.

O endpoint de health check desta fase não consulta banco de dados nem qualquer
dependência externa.

Ainda não fazem parte desta fase:

- banco de dados;
- SQLAlchemy;
- Alembic;
- models;
- schemas de domínio;
- repositories;
- services de domínio;
- autenticação;
- CRUD;
- testes automatizados;
- Docker;
- GitHub Actions.

## Separação de responsabilidades

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

Services concentrarão as regras de negócio e os casos de uso da aplicação.

Responsabilidades esperadas:

- validar regras do domínio;
- coordenar fluxos como criação, atribuição, comentário e mudança de status de tickets;
- chamar repositories;
- decidir erros de negócio;
- manter a lógica fora das rotas.

### Repositories

Repositories concentrarão o acesso ao banco de dados.

Responsabilidades esperadas:

- criar consultas;
- buscar registros;
- persistir entidades;
- atualizar dados;
- remover ou desativar registros quando aplicável.

Repositories não devem conter regra de negócio. Eles devem oferecer operações de persistência para que os services coordenem o comportamento da aplicação.

### Models

Models representarão tabelas e relacionamentos do banco de dados usando SQLAlchemy 2.x.

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

## Por que evitar controller gordo

Controller gordo ocorre quando rotas acumulam validação de regra de negócio, acesso ao banco, transformação de dados e decisões de fluxo.

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
  ↓
API route
  ↓
Schema de entrada
  ↓
Service
  ↓
Repository
  ↓
Banco de dados
  ↓
Repository
  ↓
Service
  ↓
Schema de saída
  ↓
Resposta HTTP
```

Exemplo conceitual:

1. Um cliente envia uma requisição para abrir um ticket.
2. A rota recebe a requisição e valida o payload com schema Pydantic.
3. A rota chama um service de tickets.
4. O service valida as regras de domínio.
5. O service chama o repository para persistir o ticket.
6. O repository interage com o banco.
7. O service devolve o resultado.
8. A rota retorna a resposta HTTP adequada.

## Estrutura futura de pastas

```text
supportflow-api/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── routes/
│   │       └── dependencies/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   ├── observability/
│   └── main.py
├── alembic/
├── docs/
├── tests/
├── scripts/
├── .github/
│   └── workflows/
├── AGENTS.md
├── README.md
├── pyproject.toml
├── docker-compose.yml
├── Dockerfile
└── .env.example
```

O nome da pasta raiz pode variar conforme o ambiente local. A organização interna deverá respeitar essa separação quando a implementação começar.
