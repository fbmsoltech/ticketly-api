# Banco de dados

## Objetivo da Fase 3

A Fase 3 prepara a infraestrutura inicial de persistência relacional do
Ticketly API.

Esta fase adiciona:

- PostgreSQL como banco planejado;
- SQLAlchemy 2.x para engine, sessões e mapeamento futuro;
- Alembic para migrations;
- `DATABASE_URL` como variável de ambiente;
- base declarativa para models futuros.

Esta fase não cria CRUD, endpoints de domínio, models de domínio, schemas,
repositories, services, autenticação, Docker, testes ou CI/CD.

## Variável de ambiente

A aplicação espera a variável `DATABASE_URL` no formato abaixo:

```env
DATABASE_URL=postgresql+psycopg://supportflow_user:supportflow_password@localhost:5432/supportflow_db
```

O arquivo `.env.example` contém os valores de referência para desenvolvimento
local.

## Preparação local do PostgreSQL

Antes de executar `alembic upgrade head`, o banco e o usuário informados em
`DATABASE_URL` precisam existir no PostgreSQL local.

Usando um usuário administrador do PostgreSQL, como `postgres`, execute:

```sql
CREATE USER supportflow_user WITH PASSWORD 'supportflow_password';
CREATE DATABASE supportflow_db OWNER supportflow_user;
GRANT ALL PRIVILEGES ON DATABASE supportflow_db TO supportflow_user;
```

No Windows, uma forma comum de executar esses comandos é abrir o `psql` como
usuário `postgres`:

```powershell
psql -U postgres
```

Depois disso, valide a conexão com:

```powershell
psql "postgresql://supportflow_user:supportflow_password@localhost:5432/supportflow_db"
```

Se o usuário já existir com outra senha, ajuste a senha no PostgreSQL:

```sql
ALTER USER supportflow_user WITH PASSWORD 'supportflow_password';
```

Ou altere o valor de `DATABASE_URL` no seu arquivo `.env` para refletir o
usuário, senha, host, porta e banco reais do ambiente local.

## Arquivos criados

- `app/db/base.py`: define a base declarativa `Base`.
- `app/db/session.py`: define `engine`, `SessionLocal` e `get_db_session`.
- `alembic.ini`: configura o Alembic.
- `alembic/env.py`: conecta Alembic às settings e à metadata do SQLAlchemy.
- `alembic/script.py.mako`: template de novas migrations.
- `alembic/versions/`: armazena migrations versionadas.

## Migrations

A migration inicial é vazia porque ainda não existem models de domínio.

Comandos úteis:

```bash
alembic current
alembic upgrade head
alembic downgrade -1
```

Quando os models forem criados em fase futura, novas migrations deverão ser
geradas a partir da metadata do SQLAlchemy:

```bash
alembic revision --autogenerate -m "describe change"
```

## Limites da fase

O endpoint `GET /api/v1/health` não consulta o banco de dados nesta fase.

O acesso ao banco por rotas deverá acontecer apenas em fases futuras, com
separação adequada entre routes, services e repositories.
