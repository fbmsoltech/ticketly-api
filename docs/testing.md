# Testes

## Objetivo

Os testes automatizados do Ticketly API validam o comportamento dos services e
dos contratos HTTP expostos pela API.

Eles devem proteger regras de negócio, fluxos relevantes e integrações com a
camada de persistência sem depender de banco de produção.

## Estrutura

Os testes ficam na pasta `tests/`.

Arquivos atuais:

- `tests/conftest.py`: configura fixtures compartilhadas, sessão de banco e
  cliente de teste da API;
- `tests/factories.py`: concentra dados auxiliares para os testes;
- `tests/test_services.py`: valida comportamento dos services;
- `tests/test_api_endpoints.py`: valida contratos HTTP dos endpoints.

## Execução local

Para rodar a suíte diretamente no ambiente Python local:

```bash
pytest
```

Para executar os testes usando o PostgreSQL de testes do Docker Compose:

```bash
docker compose --profile test run --rm test
```

## Execução no CI

No GitHub Actions, o workflow cria um PostgreSQL temporário, aplica as migrations
com Alembic e executa:

```bash
pytest
```

As variáveis `DATABASE_URL` e `TEST_DATABASE_URL` apontam para o banco temporário
do CI durante a execução.

## Boas práticas

- testes de service devem validar regras e casos de uso;
- testes de API devem validar status HTTP, payloads e contratos públicos;
- testes não devem usar banco de produção;
- fixtures devem manter os cenários claros e isolados;
- novas regras de negócio devem ser acompanhadas por testes automatizados.
