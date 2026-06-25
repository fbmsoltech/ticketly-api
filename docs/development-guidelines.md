# Diretrizes de desenvolvimento

## Padrão de branches

As branches devem seguir o padrão:

```text
feature/phase-XX-short-description
```

Exemplos:

- `feature/phase-01-documentation-foundation`
- `feature/phase-02-python-tooling`
- `feature/phase-03-fastapi-bootstrap`

Cada branch deve representar uma fase ou uma entrega pequena e bem delimitada.

## Padrão de commits

Os commits devem usar mensagens semânticas.

Prefixos aceitos:

- `chore:`
- `feat:`
- `fix:`
- `docs:`
- `test:`
- `refactor:`
- `ci:`

Exemplos:

- `docs: add initial project documentation`
- `chore: configure python tooling`
- `feat: add ticket creation use case`
- `test: add ticket service tests`

## Padrão de PRs

Pull requests devem ser objetivos e relacionados a uma única fase ou mudança coesa.

Um PR deve conter:

- resumo da mudança;
- fase relacionada;
- arquivos ou áreas impactadas;
- evidências de validação quando houver código;
- observações sobre documentação atualizada.

PRs não devem misturar documentação, infraestrutura, domínio e endpoints sem necessidade clara.

## Regra de uma fase por vez

O projeto deve evoluir incrementalmente.

Durante uma fase:

- implementar apenas o que pertence ao escopo atual;
- evitar antecipar funcionalidades;
- não criar arquivos ou estruturas de fases futuras sem solicitação explícita;
- manter o repositório simples e coerente com o estágio atual.

Na Fase 1, apenas documentação e guias iniciais devem ser criados.

Na Fase 2, o escopo permitido é:

- criar o setup inicial Python 3.13+;
- configurar FastAPI, Uvicorn e Pydantic Settings;
- criar a estrutura inicial `app/`;
- criar o endpoint simples `GET /api/v1/health`;
- configurar Ruff, Black e Mypy;
- atualizar a documentação relacionada.

Na Fase 2, ainda não devem ser criados:

- banco de dados;
- SQLAlchemy;
- Alembic;
- psycopg;
- Docker;
- autenticação;
- CRUD;
- models, schemas, repositories ou services de domínio;
- testes automatizados;
- GitHub Actions.

## Ferramentas de qualidade

A Fase 2 configura as ferramentas iniciais de qualidade no `pyproject.toml`.

Comandos recomendados:

```bash
ruff check .
black --check .
mypy .
```

O Ruff deve validar, no mínimo, as famílias de regras `E`, `F`, `I`, `B` e
`UP`. O Black e o Ruff usam linha máxima de 88 caracteres. O Mypy inicia em
modo estrito para manter a base tipada desde o primeiro código Python.

## Regra de atualização de documentação

A documentação deve acompanhar a evolução do projeto.

Atualizações esperadas:

- mudanças arquiteturais devem atualizar `docs/architecture.md`;
- mudanças de fluxo de negócio devem atualizar `docs/business-flow.md`;
- mudanças no processo de desenvolvimento devem atualizar `docs/development-guidelines.md`;
- mudanças relevantes para agentes devem atualizar `AGENTS.md`;
- mudanças de visão geral, execução ou status devem atualizar `README.md`.

Documentação desatualizada deve ser tratada como débito técnico.

## Boas práticas de código

Quando a implementação começar, o código deverá seguir as práticas abaixo:

- usar tipagem sempre que possível;
- manter funções e classes com responsabilidades claras;
- evitar duplicação de código;
- evitar controller gordo;
- evitar regra de negócio em repositories;
- evitar acesso direto ao banco em rotas;
- preferir nomes claros e explícitos;
- manter separação entre API, services, repositories, models e schemas;
- usar Pydantic v2 para contratos de entrada e saída;
- usar SQLAlchemy 2.x em estilo moderno;
- usar migrations com Alembic.

## Boas práticas de testes

Quando a fase de testes começar, os testes deverão seguir as práticas abaixo:

- usar Pytest;
- testar regras de negócio relevantes;
- testar endpoints importantes;
- evitar dependência do banco de produção;
- manter testes automatizados no CI;
- escrever testes legíveis e focados em comportamento;
- cobrir fluxos de sucesso e falha quando fizer sentido.

## Boas práticas de revisão

Toda revisão deve priorizar:

- aderência ao escopo da fase;
- respeito à arquitetura definida;
- clareza do código;
- ausência de regra de negócio nas rotas;
- ausência de regra de negócio em repositories;
- cobertura de testes quando aplicável;
- atualização da documentação;
- impacto em segurança, autenticação e autorização quando essas áreas existirem.

Antes de aprovar uma mudança, verifique se ela não cria funcionalidades fora da fase atual.
