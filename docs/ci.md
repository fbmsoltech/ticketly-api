# Integracao continua

## Objetivo

O Ticketly API usa GitHub Actions para validar automaticamente qualidade de
codigo, testes unitarios, migrations e testes de integracao antes que mudancas
sejam integradas ao branch principal.

O workflow de CI fica em:

```text
.github/workflows/ci.yml
```

## Quando o CI executa

O workflow executa em:

- pull requests;
- pushes para o branch `main`.

## Validacoes executadas

A pipeline executa as seguintes etapas:

- checkout do repositorio;
- configuracao do Python 3.13;
- instalacao do projeto com dependencias de desenvolvimento;
- Ruff;
- Black;
- Mypy;
- unit tests;
- Alembic migrations;
- integration tests.

Ordem dos steps principais:

```text
Ruff
Black
Mypy
Unit tests
Alembic migrations
Integration tests
```

## Banco de dados no CI

O CI usa um servico PostgreSQL isolado do GitHub Actions. As variaveis
`DATABASE_URL` e `TEST_DATABASE_URL` apontam para esse banco temporario durante a
execucao do workflow.

Os testes unitarios rodam antes das migrations e nao dependem do PostgreSQL. Os
testes de integracao rodam depois das migrations e usam o banco temporario.

Nenhum banco de producao ou ambiente externo deve ser usado pelo CI.

## Limites atuais

O workflow atual cobre apenas integracao continua.

Ele nao faz deploy, nao publica imagens Docker, nao usa Docker Hub e nao depende
de secrets reais.

Deploy e entrega continua devem ser tratados em documentacao e workflows
proprios quando esse escopo existir.
