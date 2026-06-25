# Fluxo de negócio

## Domínio do sistema

O Ticketly API será uma API REST para gestão de tickets de suporte técnico.

O sistema permitirá que clientes registrem solicitações de suporte, que atendentes acompanhem e respondam essas solicitações, e que administradores gerenciem usuários, papéis e configurações relacionadas ao atendimento.

## Principais atores

### Cliente

Pessoa ou organização que solicita suporte.

Responsabilidades previstas:

- abrir tickets;
- acompanhar seus tickets;
- adicionar comentários;
- visualizar mudanças de status.

### Atendente

Usuário responsável por analisar e responder tickets.

Responsabilidades previstas:

- visualizar tickets atribuídos;
- assumir ou receber atribuição de tickets;
- responder comentários;
- alterar status conforme o andamento do atendimento.

### Administrador

Usuário com permissões amplas para gerenciar o sistema.

Responsabilidades previstas:

- gerenciar usuários;
- gerenciar papéis;
- acompanhar tickets;
- configurar categorias, status e prioridades quando essas funcionalidades existirem.

## Fluxo básico de abertura de ticket

1. O cliente informa os dados necessários para abrir uma solicitação.
2. O sistema valida os dados de entrada.
3. O sistema cria um ticket associado ao cliente.
4. O ticket recebe status inicial.
5. O ticket recebe prioridade conforme regra futura definida.
6. O ticket fica disponível para acompanhamento e atendimento.

Regras previstas:

- Um cliente pode abrir vários tickets.
- Um ticket pertence a um cliente.
- Um ticket deve possuir status.
- Um ticket deve possuir prioridade.

## Fluxo básico de atendimento

1. Um atendente visualiza tickets disponíveis ou atribuídos a ele.
2. O ticket pode ser atribuído a um atendente.
3. O atendente analisa o conteúdo do ticket.
4. O atendente registra comentários ou atualizações.
5. O ticket evolui de status conforme o progresso do atendimento.

Regras previstas:

- Um ticket pode ser atribuído a um atendente.
- A atribuição deve respeitar permissões futuras.
- A regra de atendimento deve ficar na camada de services.

## Fluxo básico de comentários

1. Um usuário autorizado acessa um ticket.
2. O usuário envia um comentário.
3. O sistema valida se o usuário pode comentar naquele ticket.
4. O comentário é associado ao ticket.
5. O comentário fica disponível no histórico do ticket.

Regras previstas:

- Um ticket pode ter vários comentários.
- Comentários devem manter vínculo com o ticket.
- Comentários devem manter vínculo com o autor.
- Permissões de comentário dependerão do papel do usuário e do relacionamento com o ticket.

## Fluxo básico de mudança de status

1. Um usuário autorizado solicita a mudança de status de um ticket.
2. O sistema valida se a transição é permitida.
3. O sistema atualiza o status do ticket.
4. A mudança fica refletida no acompanhamento do ticket.

Status específicos serão definidos em fase futura.

Regras previstas:

- Um ticket possui status.
- Mudanças de status devem respeitar regras de domínio.
- Nem todo usuário poderá alterar status.
- A validação de mudança de status deverá ficar em services.

## Papéis previstos

### ADMIN

Papel administrativo com permissões amplas para gerenciar o sistema.

### AGENT

Papel de atendimento, voltado à triagem, resposta e atualização de tickets.

### CUSTOMER

Papel de cliente, voltado à abertura e acompanhamento dos próprios tickets.

## Permissões futuras

As permissões serão baseadas em papéis.

Regras iniciais previstas:

- Usuários terão papéis.
- Permissões serão baseadas em papéis.
- Clientes devem acessar apenas recursos permitidos para seu contexto.
- Atendentes devem acessar recursos relacionados ao atendimento.
- Administradores devem ter acesso a recursos de gestão.

## Modelagem inicial da Fase 4

A Fase 4 cria a representação persistida inicial das entidades previstas:

- usuários e papéis;
- clientes;
- tickets;
- comentários de tickets;
- categorias, status e prioridades de tickets.

Essa modelagem registra apenas a estrutura relacional inicial. Regras como
transições de status, permissões, atribuição de atendentes e validação de acesso
serão implementadas em services nas fases futuras.

## Contratos e persistência da Fase 5

A Fase 5 adiciona schemas e repositories iniciais para preparar a evolução do
domínio sem expor novos fluxos por HTTP.

Os schemas representam dados de entrada e saída para uso futuro pela API. Os
repositories encapsulam consultas e operações de persistência para que services
futuros possam coordenar regras de negócio.

Esta fase ainda não define regras de transição de status, permissões, atribuição
de atendentes, autenticação ou autorização.
