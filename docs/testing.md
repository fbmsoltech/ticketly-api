# Testes

## Objetivo

Os testes automatizados do Ticketly API validam regras isoladas, services,
repositories, contratos HTTP e integracao com banco de dados.

Eles devem proteger regras de negocio, fluxos relevantes e integracoes com a
camada de persistencia sem depender de banco de producao.

## Estrutura

Os testes ficam na pasta `tests/`.

Estrutura atual:

- `tests/conftest.py`: configura fixtures compartilhadas, sessao de banco e
  cliente de teste da API;
- `tests/factories.py`: concentra dados auxiliares para os testes;
- `tests/unit/`: testes unitarios sem banco ou infraestrutura externa;
- `tests/integration/services/`: testes de services com repositories e banco
  reais;
- `tests/integration/api/`: testes de endpoints com `TestClient` e banco real;
- `tests/unit/observability/`: testes unitarios do coletor de metricas.

## Unit Tests

Testes unitarios devem ser rapidos, isolados e marcados com
`pytest.mark.unit`.

Eles nao devem usar:

- banco real;
- SQLAlchemy `Session` real;
- `TestClient` com banco;
- Alembic;
- PostgreSQL.

Quando precisarem de colaborador externo, devem usar mocks, stubs ou fakes.

## Integration Tests

Testes de integracao devem ser marcados com `pytest.mark.integration`.

Eles podem usar:

- PostgreSQL real de teste;
- session real;
- repositories reais;
- services com banco real;
- `TestClient` chamando endpoints reais;
- constraints, relacionamentos, migrations e transacoes.

Esses testes dependem de `TEST_DATABASE_URL` quando executados contra
PostgreSQL. Sem essa variavel, a suite usa o banco de teste configurado nas
fixtures locais.

## Execucao Local

Para rodar a suite diretamente no ambiente Python local:

```bash
pytest -m unit
pytest -m integration
pytest
```

Para executar os testes usando o ambiente Docker Compose:

```bash
docker compose exec api pytest -m unit
docker compose exec api pytest -m integration
docker compose exec api pytest
```

Tambem existe o servico dedicado de testes:

```bash
docker compose --profile test run --rm test
```

## Execucao no CI

No GitHub Actions, o workflow cria um PostgreSQL temporario, executa testes
unitarios, aplica as migrations com Alembic e executa testes de integracao:

```bash
pytest -m unit
alembic upgrade head
pytest -m integration
```

As variaveis `DATABASE_URL` e `TEST_DATABASE_URL` apontam para o banco
temporario do CI durante a execucao.

## Boas Praticas

- testes de service devem validar regras e casos de uso;
- testes de API devem validar status HTTP, payloads e contratos publicos;
- testes nao devem usar banco de producao;
- fixtures devem manter os cenarios claros e isolados;
- unit tests nao devem depender de infraestrutura externa;
- testes com banco real devem ficar em `tests/integration`;
- novos testes devem usar marker `unit` ou `integration`.

## Fixtures

As fixtures compartilhadas criam roles `ADMIN`, `AGENT` e `CUSTOMER`, usuarios,
tokens JWT, headers autorizados e entidades de dominio para testes de
integracao.

Fixtures principais:

- `admin_role`;
- `agent_role`;
- `customer_role`;
- `admin_user`;
- `agent_user`;
- `customer_user`;
- `customer`;
- `ticket_category`;
- `ticket_status`;
- `second_ticket_status`;
- `ticket_priority`;
- `ticket`;
- `admin_token`;
- `agent_token`;
- `customer_token`;
- `admin_auth_headers`;
- `agent_auth_headers`;
- `customer_auth_headers`.

## Testes de Tickets

Os testes de tickets cobrem:

- criacao, busca, listagem, atualizacao e exclusao via service;
- validacao de customer, categoria, status e prioridade;
- atribuicao para `AGENT` e `ADMIN`;
- rejeicao de atribuicao para `CUSTOMER`;
- endpoints protegidos por Bearer Token;
- permissoes por papel, incluindo exclusao exclusiva para `ADMIN`;
- filtros de listagem e codigos `400`, `401`, `403` e `404`.

## Testes de Comentarios de Tickets

Os testes de comentarios cobrem:

- criacao com usuario autenticado como autor;
- busca por ID;
- listagem por ticket;
- listagem incluindo e excluindo comentarios internos;
- atualizacao de `content` e `is_internal`;
- exclusao;
- erros para ticket, autor e comentario inexistentes;
- endpoints protegidos por Bearer Token;
- permissao de criacao/listagem/consulta/atualizacao para `ADMIN` ou `AGENT`;
- exclusao restrita a `ADMIN`;
- rejeicao de `CUSTOMER`;
- garantia de que o body nao sobrescreve o autor.

## Testes de Observabilidade

Os testes de observabilidade cobrem estado inicial do coletor de metricas,
incremento de requisicoes, contadores por metodo e status code, total de
respostas 5xx, estrutura do snapshot, health checks e endpoint de metricas.
