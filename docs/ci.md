# Integração contínua

## Objetivo

O Ticketly API usa GitHub Actions para validar automaticamente a qualidade do
código, a aplicação das migrations e a suíte de testes antes que mudanças sejam
integradas ao branch principal.

O workflow de CI fica em:

```text
.github/workflows/ci.yml
```

## Quando o CI executa

O workflow executa em:

- pull requests;
- pushes para o branch `main`.

## Validações executadas

A pipeline executa as seguintes etapas:

- checkout do repositório;
- configuração do Python 3.13;
- instalação do projeto com dependências de desenvolvimento;
- validação com Ruff;
- validação de formatação com Black;
- checagem de tipos com Mypy;
- aplicação das migrations com Alembic;
- execução dos testes com Pytest.

## Banco de dados no CI

O CI usa um serviço PostgreSQL isolado do GitHub Actions. As variáveis
`DATABASE_URL` e `TEST_DATABASE_URL` apontam para esse banco temporário durante a
execução do workflow.

Nenhum banco de produção ou ambiente externo deve ser usado pelo CI.

## Limites atuais

O workflow atual cobre apenas integração contínua.

Ele não faz deploy, não publica imagens Docker, não usa Docker Hub e não depende
de secrets reais.

Deploy e entrega contínua devem ser tratados em documentação e workflows
próprios quando esse escopo existir.
