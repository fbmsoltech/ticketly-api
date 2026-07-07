# Schemas e repositories

## Objetivo

Schemas Pydantic v2 e repositories compõem as camadas de contrato de dados e
persistência da Ticketly API.

## Schemas

Os schemas ficam em `app/schemas/` e representam contratos de entrada e saída
para uso pela camada HTTP.

Responsabilidades:

- validar formato básico dos dados;
- declarar campos esperados para criação, atualização e leitura;
- separar contratos públicos da API dos models SQLAlchemy;
- habilitar serialização a partir de objetos ORM com `from_attributes=True`.

Limites:

- schemas não substituem models de banco;
- schemas não devem acessar banco de dados;
- schemas não devem conter regra de negócio complexa;
- validações de domínio, permissões e fluxos devem ficar em services.

Padrão criado:

- `*Create`: dados esperados para criação;
- `*Update`: campos opcionais para atualização parcial;
- `*Read`: dados esperados em respostas.

Os schemas de leitura não expõem campos internos sensíveis, como
`hashed_password`.

## Repositories

Os repositories ficam em `app/repositories/` e encapsulam o acesso ao banco com
SQLAlchemy 2.x.

Responsabilidades:

- buscar registros por identificadores e campos naturais;
- listar registros com filtros simples;
- adicionar e remover entidades dentro de uma sessão recebida;
- manter consultas SQLAlchemy fora de rotas e services.

Limites:

- repositories não fazem commit automático;
- repositories não decidem fluxo de caso de uso;
- repositories não aplicam regra de negócio;
- repositories não validam permissões;
- repositories não devem ser chamados diretamente por rotas.

A transação é coordenada pela camada de aplicação.

## Fluxo esperado

```text
API route
  |
Schema de entrada
  |
Service
  |
Repository
  |
Model SQLAlchemy
  |
Banco de dados
```

Esse fluxo é usado pelos endpoints CRUD das entidades base.
