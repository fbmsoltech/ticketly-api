# Services

## Objetivo da Fase 6

A Fase 6 adiciona a camada de services da Ticketly API para coordenar operaÃ§Ãµes
internas de CRUD usando os repositories criados na fase anterior.

Esta fase ainda nÃ£o cria endpoints HTTP de domÃ­nio, autenticaÃ§Ã£o,
autorizaÃ§Ã£o, testes automatizados, Docker, Docker Compose ou CI/CD.

## Responsabilidades

Os services ficam em `app/services/` e representam a camada de casos de uso da
aplicaÃ§Ã£o.

Responsabilidades atuais:

- buscar registros por identificador;
- listar registros com paginaÃ§Ã£o simples;
- criar entidades a partir de schemas Pydantic de entrada;
- aplicar atualizaÃ§Ãµes parciais com schemas `*Update`;
- remover entidades por identificador;
- expor consultas especÃ­ficas jÃ¡ encapsuladas pelos repositories;
- manter a futura camada HTTP distante de regra de negÃ³cio e persistÃªncia.

## Limites

Os services desta fase nÃ£o devem:

- expor CRUD por API;
- depender de FastAPI ou objetos HTTP;
- fazer validaÃ§Ãµes de autenticaÃ§Ã£o ou autorizaÃ§Ã£o;
- implementar permissÃµes;
- substituir repositories;
- acessar o banco fora dos repositories.

Repositories continuam responsÃ¡veis por acesso ao banco. Services coordenam o
fluxo de uso dessas operaÃ§Ãµes.

## PadrÃ£o criado

`BaseService` concentra o CRUD comum:

- `get`;
- `list`;
- `create`;
- `update`;
- `delete`.

Services especÃ­ficos expÃµem consultas relevantes para cada entidade, como:

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

## Senhas de usuÃ¡rio

`UserService` recebe uma funÃ§Ã£o `password_hasher` por injeÃ§Ã£o de dependÃªncia.
Isso permite criar e atualizar usuÃ¡rios sem definir ainda uma estratÃ©gia final
de autenticaÃ§Ã£o, que pertence a uma fase futura.

O service converte o campo `password` dos schemas de entrada em
`hashed_password` no model SQLAlchemy, preservando o cuidado de nÃ£o expor esse
campo nos schemas de leitura.

## TransaÃ§Ãµes

Os repositories executam `flush` e `refresh` quando necessÃ¡rio, mas nÃ£o fazem
`commit` automÃ¡tico.

O controle de transaÃ§Ã£o deverÃ¡ continuar sendo definido pela camada de
aplicaÃ§Ã£o ou por dependÃªncias futuras quando os endpoints forem criados.
