# Schema PostgreSQL

## Objetivo

A Ticketly API pode usar um schema PostgreSQL proprio para isolar suas tabelas
dentro de um banco fisico compartilhado.

Essa configuracao e util no Render, onde o projeto pode compartilhar um unico
banco PostgreSQL gratuito com outros projetos de portfolio sem misturar tabelas
no schema `public`.

## Banco fisico e schema

Um banco fisico PostgreSQL pode conter varios schemas. O banco e a unidade de
conexao configurada em `DATABASE_URL`; o schema e um namespace interno onde as
tabelas ficam agrupadas.

Exemplo com `DATABASE_SCHEMA=ticketly`:

```text
ticketly.roles
ticketly.users
ticketly.customers
ticketly.ticket_categories
ticketly.ticket_statuses
ticketly.ticket_priorities
ticketly.tickets
ticketly.ticket_comments
ticketly.alembic_version
```

## Variavel de ambiente

Configure:

```env
DATABASE_SCHEMA=ticketly
```

O default da aplicacao e `public` para manter compatibilidade local quando a
variavel nao estiver definida. Para deploy compartilhado no Render, o valor
recomendado e `ticketly`.

O nome do schema deve conter apenas letras, numeros e underscore. Valores vazios,
com espacos, pontos, aspas ou ponto e virgula sao rejeitados na inicializacao da
aplicacao.

## Alembic

O Alembic le `DATABASE_SCHEMA` pelas settings da aplicacao. Antes de executar as
migrations, ele cria o schema caso nao exista e ajusta o `search_path` da
conexao:

```sql
CREATE SCHEMA IF NOT EXISTS "ticketly";
SET search_path TO "ticketly";
```

A tabela de versao do Alembic tambem fica no schema configurado:

```text
ticketly.alembic_version
```

As migrations existentes continuam sem `schema=...` explicito e dependem do
`search_path` configurado pelo `alembic/env.py`. Essa decisao evita hardcode de
`ticketly` nos scripts versionados e permite trocar o schema por ambiente.

## Aplicacao e seed

O engine SQLAlchemy configura o `search_path` em conexoes PostgreSQL. A metadata
dos models usa o schema configurado quando ele nao e `public`.

O seed inicial usa a mesma `SessionLocal` da aplicacao, portanto grava roles,
status, prioridades, categorias e admin opcional no schema configurado sem
precisar conhecer o nome do schema.

## Cuidados

- Nao misture tabelas de projetos diferentes no mesmo schema.
- Nao crie tabelas da Ticketly no `public` quando `DATABASE_SCHEMA=ticketly`.
- Nao hardcode schema em services, repositories, routes ou regras de negocio.
- Nao use esse ajuste para migrar dados automaticamente de `public` para
  `ticketly`.
- Revise migrations novas para garantir que respeitam o schema configurado.

## Validacao no PostgreSQL

Verificar se o schema existe:

```sql
SELECT schema_name
FROM information_schema.schemata
WHERE schema_name = 'ticketly';
```

Listar tabelas do schema:

```sql
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema = 'ticketly'
ORDER BY table_name;
```

Consultar a versao do Alembic:

```sql
SELECT *
FROM ticketly.alembic_version;
```
