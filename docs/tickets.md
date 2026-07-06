# Tickets

## Objetivo

Tickets representam solicitacoes de suporte associadas a um cliente. Eles
centralizam o assunto, descricao, categoria, status, prioridade e responsavel
pelo atendimento quando houver atribuicao.

## Campos principais

- `id`: identificador do ticket;
- `title`: titulo curto da solicitacao;
- `description`: descricao detalhada do problema ou pedido;
- `customer_id`: cliente dono do ticket;
- `category_id`: categoria do atendimento;
- `status_id`: status atual;
- `priority_id`: prioridade atual;
- `assigned_agent_id`: usuario responsavel pelo atendimento, opcional;
- `created_at` e `updated_at`: datas de auditoria basica.

Internamente o model persistido usa `assignee_id`. O contrato publico da API usa
`assigned_agent_id` para deixar claro que a atribuicao deve apontar para um
usuario atendente ou administrador.

## Relacionamentos

- Um ticket pertence a um customer.
- Um ticket pertence a uma categoria.
- Um ticket possui um status.
- Um ticket possui uma prioridade.
- Um ticket pode ter um usuario responsavel.

## Criacao

`POST /api/v1/tickets` cria tickets para uso administrativo e de atendimento.

Regras aplicadas pelo `TicketService`:

- `customer_id` deve existir;
- `category_id` deve existir;
- `status_id` deve existir;
- `priority_id` deve existir;
- quando `assigned_agent_id` for informado, o usuario deve existir;
- quando `assigned_agent_id` for informado, o usuario deve ter papel `ADMIN` ou
  `AGENT`.

## Atualizacao

`PATCH /api/v1/tickets/{ticket_id}` permite atualizacao parcial de titulo,
descricao, cliente, categoria, status, prioridade e responsavel.

Ao alterar qualquer relacionamento, o service valida se o recurso relacionado
existe. O responsavel pode ser removido enviando `assigned_agent_id` como
`null`.

## Atribuicao

A atribuicao de responsavel e permitida apenas para usuarios com papel `ADMIN`
ou `AGENT`. Tentativas de atribuir um ticket a usuario com papel `CUSTOMER`
retornam erro de operacao invalida.

## Permissoes

- `ADMIN`: cria, lista, consulta, atualiza, atribui e exclui tickets.
- `AGENT`: cria, lista, consulta e atualiza tickets.
- `CUSTOMER`: nao acessa o CRUD de tickets nesta versao da API.

`DELETE /api/v1/tickets/{ticket_id}` exige papel `ADMIN`.

## Limitacoes atuais

- Abertura direta por cliente autenticado nao esta habilitada no CRUD de tickets.
- Comentarios de tickets nao fazem parte deste fluxo.
- Historico de mudancas nao e registrado.
- Anexos, upload, notificacoes, SLA, metricas e logging estruturado nao fazem
  parte deste fluxo.
- Nenhuma tabela nova foi criada para este comportamento.

## Proximos passos

- Permitir abertura direta por cliente autenticado usando o vinculo entre
  `User` e `Customer`.
- Definir regras de acesso para cliente consultar apenas os proprios tickets.
- Evoluir comentarios de tickets com permissoes especificas.
- Adicionar historico de mudancas quando houver regra de auditoria definida.
