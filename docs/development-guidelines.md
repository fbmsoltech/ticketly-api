# Diretrizes de desenvolvimento

## Padrão de branches

As branches devem seguir o padrão:

```text
feature/phase-XX-short-description
```

Exemplos:

- `feature/phase-01-documentation-foundation`
- `feature/phase-02-python-tooling`
- `feature/phase-03-database-infrastructure`

Cada branch deve representar uma fase ou uma entrega pequena e bem delimitada.

## Padrão de commits

Os commits devem usar mensagens semânticas.

Prefixos aceitos:

- `chore:`
- `feat:`
- `fix:`
- `docs:`
- `test:`
- `refactor:`
- `ci:`

Exemplos:

- `docs: add initial project documentation`
- `chore: configure python tooling`
- `chore: configure database infrastructure`
- `feat: add ticket creation use case`
- `test: add ticket service tests`

## Padrão de PRs

Pull requests devem ser objetivos e relacionados a uma mudança coesa.

Um PR deve conter:

- resumo da mudança;
- arquivos ou áreas impactadas;
- evidências de validação quando houver código;
- observações sobre documentação atualizada.

PRs não devem misturar documentação, infraestrutura, domínio e endpoints sem
necessidade clara.

## Regra de escopo incremental

O projeto deve evoluir incrementalmente.

Durante uma entrega:

- implementar apenas o que pertence ao escopo atual;
- evitar antecipar funcionalidades;
- não criar arquivos ou estruturas futuras sem solicitação explícita;
- manter o repositório simples e coerente com o estágio atual.

## Ferramentas de qualidade

As ferramentas iniciais de qualidade ficam configuradas no `pyproject.toml`.

Comandos recomendados:

```bash
ruff check .
black --check .
mypy .
pytest
```

O Ruff deve validar, no mínimo, as famílias de regras `E`, `F`, `I`, `B` e
`UP`. O Black e o Ruff usam linha máxima de 88 caracteres. O Mypy inicia em modo
estrito para manter a base tipada desde o primeiro código Python.

## Banco de dados e migrations

O banco é configurado por meio da variável `DATABASE_URL`.

O Alembic deve ler a URL a partir das settings da aplicação, evitando duplicação
de configuração entre aplicação e migrations.

Comandos úteis:

```bash
alembic current
alembic revision --autogenerate -m "describe change"
alembic upgrade head
alembic downgrade -1
```

Migrations devem refletir mudanças reais de schema e permanecer alinhadas à
metadata dos models SQLAlchemy.

## Regra de atualização de documentação

A documentação deve acompanhar a evolução do projeto.

Atualizações esperadas:

- mudanças arquiteturais devem atualizar `docs/architecture.md`;
- mudanças de fluxo de negócio devem atualizar `docs/business-flow.md`;
- mudanças de banco devem atualizar `docs/database.md`;
- mudanças no processo de desenvolvimento devem atualizar
  `docs/development-guidelines.md`;
- mudanças em schemas e repositories devem atualizar
  `docs/schemas-and-repositories.md`;
- mudanças em services devem atualizar `docs/services.md`;
- mudanças em testes devem atualizar `docs/testing.md`;
- mudanças em CI devem atualizar `docs/ci.md`;
- mudanças relevantes para agentes devem atualizar `AGENTS.md`;
- mudanças de visão geral, execução ou status devem atualizar `README.md`.

Documentação desatualizada deve ser tratada como débito técnico.

## Boas práticas de código

O código deverá seguir as práticas abaixo:

- usar tipagem sempre que possível;
- manter funções e classes com responsabilidades claras;
- evitar duplicação de código;
- evitar controller gordo;
- evitar regra de negócio em repositories;
- evitar acesso direto ao banco em rotas;
- preferir nomes claros e explícitos;
- manter separação entre API, services, repositories, models e schemas;
- usar Pydantic v2 para contratos de entrada e saída;
- usar SQLAlchemy 2.x em estilo moderno;
- usar migrations com Alembic.

## Observabilidade

- nao logar senha;
- nao logar token;
- nao logar header `Authorization`;
- nao logar cookies ou headers sensiveis;
- nao logar body de requisicao por padrao;
- usar readiness para validar dependencias como banco de dados;
- usar liveness apenas para verificar se o processo da aplicacao esta vivo;
- manter metricas basicas sem dados pessoais ou segredos.

## Services de dominio

Services de dominio devem receber a sessao ou repositories necessarios para
coordenar o caso de uso sem importar FastAPI.

Regras esperadas:

- validar existencia de entidades relacionadas antes de persistir dados;
- lancar excecoes de service, como `ResourceNotFoundError` ou
  `InvalidOperationError`;
- fazer `commit` em operacoes de escrita quando forem donos do caso de uso;
- fazer `rollback` em erro;
- manter regras de negocio fora de routes e repositories;
- usar schemas Pydantic de entrada para criar e atualizar models.

Rotas continuam responsaveis por HTTP, autenticacao, autorizacao e serializacao
de resposta. Repositories continuam responsaveis apenas por acesso ao banco.

## Regras para comentarios de tickets

- rotas de comentarios devem ficar aninhadas em `/tickets/{ticket_id}/comments`;
- o `ticket_id` da URL prevalece sobre qualquer valor enviado no body;
- o autor usuario deve ser o usuario autenticado;
- campos de autoria enviados no body devem ser ignorados;
- `author_customer_id` fica reservado para fluxo futuro de portal do cliente;
- comentarios internos usam `is_internal`;
- `ADMIN` e `AGENT` podem ver comentarios internos;
- `CUSTOMER` nao acessa endpoints de comentarios enquanto o fluxo de cliente
  autenticado nao estiver completo;
- repositories nao devem decidir visibilidade por papel.

## Boas práticas de testes

Os testes automatizados usam Pytest e ficam na pasta `tests/`.

Comando recomendado:

```bash
pytest
```

Para executar os testes no PostgreSQL de testes gerenciado pelo Docker Compose:

```bash
docker compose --profile test run --rm test
```

No CI, os testes rodam em um PostgreSQL temporário criado pelo GitHub Actions,
depois da validação das migrations com Alembic.

Os testes devem seguir as práticas abaixo:

- usar Pytest;
- marcar novos testes com `unit` ou `integration`;
- nao chamar teste com banco real de unitario;
- manter testes com banco, repositories reais ou `TestClient` em
  `tests/integration`;
- manter unit tests em `tests/unit` sem dependencia de infraestrutura externa;
- testar regras de negócio relevantes;
- testar endpoints importantes;
- evitar dependência do banco de produção;
- manter testes automatizados no CI;
- escrever testes legíveis e focados em comportamento;
- cobrir fluxos de sucesso e falha quando fizer sentido.

## Docker Compose

O ambiente local containerizado contém:

- `api`: aplicação FastAPI;
- `db`: PostgreSQL principal;
- `test-db`: PostgreSQL isolado para testes;
- `test`: serviço sob profile `test` para executar `pytest`.

Comandos úteis:

```bash
docker compose up --build
docker compose --profile test run --rm test
docker compose down
docker compose down -v
```

O arquivo `AGENTS.md` deve permanecer fora do Git e fora do contexto de build da
imagem Docker.

## Integração contínua

O workflow de CI fica em `.github/workflows/ci.yml`.

Ele deve validar:

- Ruff;
- Black;
- Mypy;
- Alembic;
- Pytest.

O CI deve executar em pull requests e pushes para `main`, usando banco
PostgreSQL temporário para migrations e testes.

O workflow atual não deve fazer deploy, entrega contínua, build e push de
imagem Docker, configuração de Docker Hub ou uso de secrets reais.

## Boas práticas de revisão

Toda revisão deve priorizar:

- aderência ao escopo da fase;
- respeito à arquitetura definida;
- clareza do código;
- ausência de regra de negócio nas rotas;
- ausência de regra de negócio em repositories;
- cobertura de testes quando aplicável;
- atualização da documentação;
- impacto em segurança, autenticação e autorização quando essas áreas existirem.

Antes de aprovar uma mudança, verifique se ela não cria funcionalidades fora da
fase atual.

## Boas praticas de seguranca

- nunca salvar senha em texto puro;
- nunca retornar `hashed_password` em schemas ou respostas da API;
- services nao devem importar FastAPI nem lancar `HTTPException`;
- rotas protegidas devem usar dependencies de autenticacao e autorizacao;
- regras de papel devem comparar o nome da role;
- secrets reais nao devem ser versionados;
- `AGENTS.md` nao deve ser versionado, alterado sem necessidade ou aparecer em
  commits e PRs.
