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

## Users

- `POST /users`: cria usuario;
- `GET /users`: lista usuarios com `offset` e `limit`;
- `GET /users/{user_id}`: busca usuario por ID;
- `PATCH /users/{user_id}`: atualiza usuario;
- `DELETE /users/{user_id}`: remove usuario.

`POST /users` retorna `201`. `DELETE /users/{user_id}` retorna `204`.

Responses de usuario nunca incluem `hashed_password`.

## Codigos relevantes

- `401`: token ausente, token invalido ou credenciais invalidas;
- `403`: usuario inativo ou papel insuficiente;
- `404`: recurso inexistente;
- `409`: conflito, como e-mail de usuario duplicado.
