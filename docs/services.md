# Services

## Objetivo

A camada de services da Ticketly API coordena operações internas de CRUD usando
repositories e schemas Pydantic v2.

Services são o ponto de entrada para casos de uso da aplicação e mantêm regras
de domínio fora das rotas HTTP e fora dos repositories.

## Responsabilidades

Os services ficam em `app/services/` e representam a camada de casos de uso da
aplicação.

Responsabilidades atuais:

- buscar registros por identificador;
- listar registros com paginação simples;
- criar entidades a partir de schemas Pydantic de entrada;
- aplicar atualizações parciais com schemas `*Update`;
- remover entidades por identificador;
- expor consultas específicas já encapsuladas pelos repositories;
- manter a camada HTTP distante de regra de negócio e persistência.

## Limites

Os services não devem:

- depender de FastAPI ou objetos HTTP;
- fazer validações de autenticação ou autorização;
- implementar permissões;
- substituir repositories;
- acessar o banco fora dos repositories.

Repositories continuam responsáveis por acesso ao banco. Services coordenam o
fluxo de uso dessas operações.

## Padrão criado

`BaseService` concentra o CRUD comum:

- `get`;
- `list`;
- `create`;
- `update`;
- `delete`.

Services específicos expõem consultas relevantes para cada entidade, como:

- `UserService.get_by_email`;
- `UserService.list_by_role`;
- `CustomerService.get_by_user_id`;
- `TicketService.list_by_customer`;
- `TicketService.list_by_assignee`;
- `TicketService.list_by_status`;
- `TicketCommentService.list_by_ticket`;
- `TicketCommentService.list_public_by_ticket`;
- `TicketCategoryService.list_active`;
- `TicketStatusService.list_ordered`;
- `TicketPriorityService.list_ordered`.

## Senhas de usuário

`UserService` recebe uma função `password_hasher` por injeção de dependência.
Isso permite criar e atualizar usuários sem definir ainda uma estratégia final
de autenticação, que será adicionada em uma entrega própria.

O service converte o campo `password` dos schemas de entrada em
`hashed_password` no model SQLAlchemy, preservando o cuidado de não expor esse
campo nos schemas de leitura.

## Transações

Os repositories executam `flush` e `refresh` quando necessário, mas não fazem
`commit` automático.

O controle de transação é definido pela camada de aplicação por meio das
dependências de sessão usadas pelas rotas HTTP.
