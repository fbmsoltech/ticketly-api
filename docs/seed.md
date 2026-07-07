# Seed inicial

## Objetivo

O seed inicial prepara um banco vazio ou parcialmente populado com os dados
minimos para operar o Ticketly API: roles, status de tickets, prioridades,
categorias basicas e, opcionalmente, um usuario administrador inicial.

## Dados criados

Roles:

- `ADMIN`
- `AGENT`
- `CUSTOMER`

Status de tickets:

- `OPEN`
- `IN_PROGRESS`
- `WAITING_CUSTOMER`
- `RESOLVED`
- `CLOSED`

Prioridades:

- `LOW`
- `MEDIUM`
- `HIGH`
- `URGENT`

Categorias:

- `GENERAL`
- `TECHNICAL`
- `BILLING`
- `ACCESS`

## Idempotencia

O seed e idempotente. Ele cria apenas registros ausentes, nao duplica dados, nao
apaga registros existentes e nao sobrescreve customizacoes ou senhas.

## Admin inicial

O usuario administrador inicial e opcional e depende de variaveis de ambiente:

```env
CREATE_INITIAL_ADMIN=true
INITIAL_ADMIN_NAME=Admin
INITIAL_ADMIN_EMAIL=admin@example.com
INITIAL_ADMIN_PASSWORD=uma-senha-forte
```

Quando `CREATE_INITIAL_ADMIN=false`, apenas os dados base sao criados. A senha
do admin nunca deve ser versionada, nunca e logada e sempre e salva como hash.

A senha inicial nao pode ser vazia, nao pode ser `change-me` e deve ter pelo
menos 8 caracteres. Em producao, defina uma senha forte no ambiente do provedor.
Depois do primeiro deploy, troque a senha do admin ou defina
`CREATE_INITIAL_ADMIN=false` se nao quiser revalidar esse usuario a cada
restart.

## Execucao local

```bash
python scripts/seed_initial_data.py
```

Via Docker:

```bash
docker compose exec api python scripts/seed_initial_data.py
```

## Execucao no Render

O seed e executado automaticamente pelo `scripts/start.sh` apos as migrations:

```text
alembic upgrade head
seed_initial_data
uvicorn
```

Secrets reais devem ser configurados como variaveis de ambiente no Render e
nunca devem ser salvos no repositorio.
