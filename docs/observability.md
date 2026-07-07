# Observabilidade

## Objetivo

A observabilidade do Ticketly API oferece verificacoes basicas de saude,
logging estruturado de requisicoes e metricas simples em memoria para apoiar
execucao local, testes e diagnostico inicial.

Ela nao substitui uma plataforma completa de monitoramento. Prometheus,
OpenTelemetry, tracing distribuido, dashboards, alertas e integracoes externas
de logs ficam como evolucoes futuras.

## Health Check

O endpoint `GET /api/v1/health` retorna o estado geral da aplicacao, incluindo o
componente `database`.

Quando todos os componentes estao saudaveis, o status geral e `ok`. Quando o
banco falha, o status geral passa a `degraded` e o componente `database` retorna
`error` sem expor stack trace ou erro bruto da aplicacao.

## Liveness

O endpoint `GET /api/v1/health/live` verifica apenas se o processo da aplicacao
esta vivo.

Ele nao consulta o banco de dados e deve ser usado para checks que nao dependem
de servicos externos.

## Readiness

O endpoint `GET /api/v1/health/ready` verifica se a aplicacao esta pronta para
receber trafego.

Esse endpoint consulta o banco com `SELECT 1`. Se o banco estiver indisponivel,
a resposta retorna `503` e payload com status `degraded`.

## Logging estruturado

A aplicacao configura logging com a biblioteca padrao do Python. O nivel e
controlado por `LOG_LEVEL`.

O middleware de requisicoes registra metodo HTTP, path, status code e duracao em
milissegundos.

Exemplo:

```text
method=GET path=/api/v1/health status_code=200 duration_ms=12.34
```

Bodies, senhas, tokens e headers sensiveis nao sao registrados.

## Metricas basicas

O endpoint `GET /api/v1/metrics` retorna um snapshot em memoria com uptime,
total de requisicoes, totais por metodo HTTP, totais por status code, total de
respostas 5xx e ultima duracao registrada.

As metricas ficam apenas na memoria do processo. Reinicios da aplicacao zeram os
contadores.

## Configuracao

```env
LOG_LEVEL=INFO
ENABLE_REQUEST_LOGGING=true
ENABLE_METRICS=true
```

## Cuidados de seguranca

Nao registre senha, token, header `Authorization`, cookies de sessao ou payloads
com dados sensiveis.

O endpoint `/metrics` e publico para simplificar uso local. Em producao, ele
deve ser protegido por autenticacao ou exposto apenas em rede interna.

## Proximos passos possiveis

Evolucoes futuras podem incluir Prometheus, OpenTelemetry, dashboards, tracing
distribuido, alertas e integracao com servicos externos de logs.
