# Autenticacao

## Estrategia

O Ticketly API usa autenticacao stateless com JWT assinado e envio por Bearer
Token no header `Authorization`.

O login recebe e-mail e senha em `POST /api/v1/auth/login`. Quando as
credenciais sao validas, a API retorna um access token. Esse token deve ser
enviado nas rotas protegidas:

```text
Authorization: Bearer <TOKEN>
```

## Hashing de senha

Senhas nunca devem ser salvas em texto puro.

`app/core/security.py` usa `pwdlib[argon2]` para gerar e validar hashes. O campo
persistido no banco e `hashed_password`; ele nunca deve aparecer em respostas da
API.

## JWT

Tokens sao gerados e validados em `app/core/security.py` com `pyjwt`.

Claims usadas:

- `sub`: ID do usuario autenticado;
- `exp`: data e hora de expiracao do token.

Configuracoes:

- `JWT_SECRET_KEY`;
- `JWT_ALGORITHM`;
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`.

Use um segredo forte em ambientes reais. O valor de exemplo existe apenas para
desenvolvimento local.

## Usuario atual

`GET /api/v1/auth/me` exige token valido e retorna os dados publicos do usuario
autenticado, incluindo `role_name`.

O retorno nao inclui `hashed_password`.

## Papeis e permissoes

Papeis iniciais:

- `ADMIN`;
- `AGENT`;
- `CUSTOMER`.

Permissoes atuais:

- `/roles`: somente `ADMIN`;
- `/users`: somente `ADMIN`;
- `/ticket-categories`: somente `ADMIN`;
- `/ticket-statuses`: somente `ADMIN`;
- `/ticket-priorities`: somente `ADMIN`;
- `/customers`: `ADMIN` ou `AGENT`.

Rotas publicas:

- `GET /api/v1/health`;
- `POST /api/v1/auth/login`.

Token ausente ou invalido retorna `401`. Usuario inativo ou papel insuficiente
retorna `403`.

## Limitacoes atuais

Ainda nao ha seed automatico. Para testes manuais, crie uma role `ADMIN` e um
usuario admin diretamente no banco ou por fluxo ja autorizado em ambiente de
desenvolvimento.

Ainda nao fazem parte da autenticacao:

- refresh token;
- recuperacao de senha;
- confirmacao de e-mail;
- login social;
- OAuth externo;
- MFA.
