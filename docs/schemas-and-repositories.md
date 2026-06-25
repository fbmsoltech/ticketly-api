# Schemas e repositories

## Objetivo da Fase 5

A Fase 5 adiciona as primeiras camadas de schemas Pydantic v2 e repositories da
Ticketly API.

Esta fase cria contratos de dados e adaptadores de persistência, mas ainda não
cria endpoints de domínio, services, autenticação, autorização, testes
automatizados, Docker ou CI/CD.

## Schemas

Os schemas ficam em `app/schemas/` e representam contratos de entrada e saída
para uso futuro pela camada HTTP.

Responsabilidades:

- validar formato básico dos dados;
- declarar campos esperados para criação, atualização e leitura;
- separar contratos públicos da API dos models SQLAlchemy;
- habilitar serialização a partir de objetos ORM com `from_attributes=True`.

Limites:

- schemas não substituem models de banco;
- schemas não devem acessar banco de dados;
- schemas não devem conter regra de negócio complexa;
- validações de domínio, permissões e fluxos devem ficar em services futuros.

Padrão criado:

- `*Create`: dados esperados para criação;
- `*Update`: campos opcionais para atualização parcial futura;
- `*Read`: dados esperados em respostas futuras.

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
- repositories não devem ser chamados diretamente por rotas futuras.

A transação deverá ser coordenada por services ou pela camada de aplicação em
fases futuras.

## Fluxo esperado futuro

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

Nesta fase o fluxo ainda não está exposto por endpoints de domínio. As camadas
foram preparadas para uso incremental nas próximas fases.
