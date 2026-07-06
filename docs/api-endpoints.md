# Endpoints da API

Base path:

```text
/api/v1
```

## Rotas publicas

- `GET /health`: health check simples, sem consulta ao banco;
- `POST /auth/login`: autentica usuario e retorna access token.

### POST /auth/login

Payload:

```json
{
  "email": "admin@example.com",
  "password": "admin123"
}
```

Resposta `200`:

```json
{
  "access_token": "<TOKEN>",
  "token_type": "bearer"
}
```

Credenciais invalidas retornam `401`.

## Rotas autenticadas

### GET /auth/me

Exige Bearer Token valido.

Retorna o usuario atual com `role_name` e sem `hashed_password`.

## Rotas administrativas

As rotas abaixo exigem usuario com papel `ADMIN`:

- CRUD de roles em `/roles`;
- CRUD de users em `/users`;
- CRUD de ticket statuses em `/ticket-statuses`;
- CRUD de ticket priorities em `/ticket-priorities`;
- CRUD de ticket categories em `/ticket-categories`.

As rotas de customers exigem `ADMIN` ou `AGENT`:

- CRUD de customers em `/customers`.

As rotas de tickets exigem autenticacao:

- `POST /tickets`: `ADMIN` ou `AGENT`;
- `GET /tickets`: `ADMIN` ou `AGENT`;
- `GET /tickets/{ticket_id}`: `ADMIN` ou `AGENT`;
- `PATCH /tickets/{ticket_id}`: `ADMIN` ou `AGENT`;
- `DELETE /tickets/{ticket_id}`: somente `ADMIN`.

## Users

- `POST /users`: cria usuario;
- `GET /users`: lista usuarios com `offset` e `limit`;
- `GET /users/{user_id}`: busca usuario por ID;
- `PATCH /users/{user_id}`: atualiza usuario;
- `DELETE /users/{user_id}`: remove usuario.

`POST /users` retorna `201`. `DELETE /users/{user_id}` retorna `204`.

Responses de usuario nunca incluem `hashed_password`.

## Tickets

- `POST /tickets`: cria ticket e retorna `201`;
- `GET /tickets`: lista tickets com `offset`, `limit` e filtros opcionais;
- `GET /tickets/{ticket_id}`: busca ticket por ID;
- `PATCH /tickets/{ticket_id}`: atualiza ticket parcialmente;
- `DELETE /tickets/{ticket_id}`: remove ticket e retorna `204`.

Filtros aceitos em `GET /tickets`:

- `customer_id`;
- `status_id`;
- `priority_id`;
- `assigned_agent_id`;
- `offset`;
- `limit`.

Payload basico de criacao:

```json
{
  "title": "Cannot access dashboard",
  "description": "The dashboard returns an error.",
  "customer_id": 1,
  "category_id": 1,
  "status_id": 1,
  "priority_id": 1,
  "assigned_agent_id": 2
}
```

`assigned_agent_id` e opcional. Quando informado, o usuario deve ter papel
`ADMIN` ou `AGENT`.

## Codigos relevantes

- `401`: token ausente, token invalido ou credenciais invalidas;
- `403`: usuario inativo ou papel insuficiente;
- `404`: recurso inexistente;
- `400`: operacao invalida, como atribuicao de ticket para usuario sem papel de
  atendimento;
- `409`: conflito, como e-mail de usuario duplicado.
