# Banco de dados

## Objetivo

O Ticketly API usa PostgreSQL como banco relacional planejado, SQLAlchemy 2.x
para mapeamento e sessões, e Alembic para versionamento de schema.

O projeto inclui:

- PostgreSQL como banco planejado;
- SQLAlchemy 2.x para engine, sessões e mapeamento;
- Alembic para migrations;
- `DATABASE_URL` como variável de ambiente;
- base declarativa para models;
- models iniciais em `app/models/`;
- migration para criação das tabelas do domínio.

Os endpoints CRUD usam a infraestrutura de banco por meio de services e
repositories. O ambiente local com Docker Compose fornece um banco principal e
um banco separado para testes.

## Variável de ambiente

A aplicação espera a variável `DATABASE_URL` no formato abaixo:

```env
DATABASE_URL=postgresql+psycopg://ticketly_user:ticketly_user@localhost:5432/ticketly_db
```

O arquivo `.env.example` contém os valores de referência para desenvolvimento
local.

No Docker Compose, a aplicação acessa os bancos pelos nomes dos serviços:

```env
DATABASE_URL=postgresql+psycopg://ticketly_user:ticketly_user@db:5432/ticketly_db
TEST_DATABASE_URL=postgresql+psycopg://ticketly_user:ticketly_user@test-db:5432/ticketly_test_db
```

Ao conectar a partir da máquina host, use as portas publicadas pelo Compose:

```env
DATABASE_URL=postgresql+psycopg://ticketly_user:ticketly_user@localhost:5432/ticketly_db
TEST_DATABASE_URL=postgresql+psycopg://ticketly_user:ticketly_user@localhost:5433/ticketly_test_db
```

## Ambiente com Docker Compose

Para subir a API e os bancos locais:

```bash
docker compose up --build
```

O serviço `api` aplica as migrations com `alembic upgrade head` antes de iniciar
o Uvicorn.

Serviços disponíveis:

- `api`: aplicação FastAPI exposta em `localhost:8000`;
- `db`: PostgreSQL principal exposto em `localhost:5432`;
- `test-db`: PostgreSQL de testes exposto em `localhost:5433`;
- `test`: execução de `pytest` usando o banco `test-db`.

Para executar a suíte de testes no banco PostgreSQL de testes:

```bash
docker compose --profile test run --rm test
```

Para remover containers, rede e volumes dos bancos locais:

```bash
docker compose down -v
```

## Preparação local do PostgreSQL

Antes de executar `alembic upgrade head`, o banco e o usuário informados em
`DATABASE_URL` precisam existir no PostgreSQL local.

Usando um usuário administrador do PostgreSQL, como `postgres`, execute:

```sql
CREATE USER ticketly_user WITH PASSWORD 'ticketly_user';
CREATE DATABASE ticketly_db OWNER ticketly_user;
GRANT ALL PRIVILEGES ON DATABASE ticketly_db TO ticketly_user;
```

No Windows, uma forma comum de executar esses comandos é abrir o `psql` como
usuário `postgres`:

```powershell
psql -U postgres
```

Depois disso, valide a conexão com:

```powershell
psql "postgresql://ticketly_user:ticketly_user@localhost:5432/ticketly_db"
```

Se o usuário já existir com outra senha, ajuste a senha no PostgreSQL:

```sql
ALTER USER ticketly_user WITH PASSWORD 'ticketly_user';
```

Ou altere o valor de `DATABASE_URL` no seu arquivo `.env` para refletir o
usuário, senha, host, porta e banco reais do ambiente local.

## Arquivos criados

- `app/db/base.py`: define a base declarativa `Base`.
- `app/db/session.py`: define `engine`, `SessionLocal`, `get_db_session` e o
  ciclo transacional por requisição.
- `app/models/`: define os models iniciais de domínio.
- `alembic.ini`: configura o Alembic.
- `alembic/env.py`: conecta Alembic às settings e à metadata do SQLAlchemy.
- `alembic/script.py.mako`: template de novas migrations.
- `alembic/versions/`: armazena migrations versionadas.

## Tabelas iniciais

A migration `0002_initial_domain_models.py` cria as tabelas:

- `roles`;
- `users`;
- `customers`;
- `ticket_categories`;
- `ticket_statuses`;
- `ticket_priorities`;
- `tickets`;
- `ticket_comments`.

Os relacionamentos iniciais representam os vínculos estruturais do domínio, como
usuário e papel, cliente e ticket, ticket e comentários, status, prioridade,
categoria e atendente atribuído.

## Migrations

A migration `0001_initial_database_setup.py` permanece vazia porque representa
apenas a configuração inicial. A migration `0002_initial_domain_models.py`
cria as primeiras tabelas reais do banco de dados.

Comandos úteis:

```bash
alembic current
alembic upgrade head
alembic downgrade -1
```

Quando os models forem alterados, novas migrations deverão ser geradas a partir
da metadata do SQLAlchemy:

```bash
alembic revision --autogenerate -m "describe change"
```

## Limites atuais

O endpoint `GET /api/v1/health` não consulta o banco de dados.

Rotas CRUD recebem services por dependência. A sessão SQLAlchemy é injetada no
service por meio dos repositories, confirma a transação ao final de requisições
bem-sucedidas e executa rollback quando ocorre exceção.
