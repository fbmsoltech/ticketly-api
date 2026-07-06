# Comentarios de tickets

## Objetivo

Comentarios permitem registrar comunicacao e notas operacionais dentro de um
ticket. Eles complementam o ticket sem alterar status, prioridade, categoria ou
responsavel.

## Campos principais

- `id`: identificador do comentario;
- `ticket_id`: ticket ao qual o comentario pertence;
- `author_user_id`: usuario autenticado que criou o comentario;
- `author_customer_id`: reservado para fluxo futuro de portal do cliente;
- `content`: texto do comentario;
- `is_internal`: indica se o comentario e interno;
- `created_at` e `updated_at`: datas de criacao e atualizacao.

No banco atual, o model persiste `author_id` e `body`. A API publica esses
campos como `author_user_id` e `content` para manter o contrato alinhado ao
dominio.

## Relacao com tickets

Todo comentario pertence a um ticket existente. O service valida o ticket antes
de criar ou listar comentarios. A rota usa sempre o `ticket_id` da URL:

```text
/api/v1/tickets/{ticket_id}/comments
```

## Autoria

Comentarios criados pela API autenticada usam o usuario atual como autor. O
payload nao pode definir autor arbitrario. Campos como `author_user_id` ou
`author_id` enviados no body sao ignorados na criacao.

`author_customer_id` permanece reservado para o portal do cliente. Como o fluxo
de cliente autenticado vinculado a `Customer` ainda nao esta completo,
comentarios de cliente nao sao criados por estes endpoints.

## Comentarios internos e visibilidade

`is_internal=true` representa uma nota interna da equipe de atendimento.

Visibilidade atual:

- `ADMIN` ve comentarios publicos e internos;
- `AGENT` ve comentarios publicos e internos;
- `CUSTOMER` nao acessa os endpoints de comentarios.

A visibilidade para clientes sera completada quando existir o fluxo de portal do
cliente autenticado.

## Permissoes

- `POST /tickets/{ticket_id}/comments`: `ADMIN` ou `AGENT`;
- `GET /tickets/{ticket_id}/comments`: `ADMIN` ou `AGENT`;
- `GET /tickets/{ticket_id}/comments/{comment_id}`: `ADMIN` ou `AGENT`;
- `PATCH /tickets/{ticket_id}/comments/{comment_id}`: `ADMIN` ou `AGENT`;
- `DELETE /tickets/{ticket_id}/comments/{comment_id}`: somente `ADMIN`.

A atualizacao por autor especifico ainda nao foi separada porque os endpoints
atuais sao restritos a `ADMIN` e `AGENT`.

## Limitacoes atuais

- nao ha anexos;
- nao ha upload de arquivos;
- nao ha notificacoes;
- nao ha SLA;
- nao ha historico avancado de mudancas;
- nao ha metricas;
- clientes autenticados ainda nao acessam comentarios;
- comentarios de cliente ainda nao sao criados.

## Proximos passos

- concluir o fluxo de portal do cliente;
- expor comentarios publicos para clientes autorizados;
- implementar autoria por `author_customer_id`;
- avaliar regras de atualizacao pelo proprio autor quando houver necessidade de
  permissao mais granular.
