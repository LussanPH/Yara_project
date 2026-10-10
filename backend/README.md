# Sentinela Saúde — Backend

API do **Sentinela Saúde**, aplicativo para monitoramento de notificações registradas por **Agentes Comunitários de Saúde (ACS)** e **Agentes de Combate a Endemias (ACE)**.

O backend expõe endpoints REST consumidos pelo frontend em React, organizando as notificações por município e superintendência regional, e gera relatórios em PDF.

> 🔗 Frontend: `TODO: link do repositório do frontend`
> 🌐 API em produção: `TODO: URL do serviço no Render`

---

## Sumário

- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Como rodar localmente](#como-rodar-localmente)
- [Variáveis de ambiente](#variáveis-de-ambiente)
- [Migrações do banco (Alembic)](#migrações-do-banco-alembic)
- [Documentação da API](#documentação-da-api)
- [Deploy](#deploy)
- [Segurança e dados sensíveis](#segurança-e-dados-sensíveis)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

---

## Funcionalidades

- Cadastro e consulta de notificações de ACS/ACE
- Filtro de notificações por superintendência regional e município
- Geração de relatórios em PDF das notificações
- `TODO: autenticação/login, perfis de usuário, outras funcionalidades`

## Tecnologias

| Camada         | Ferramenta                                           | Uso no projeto                                       |
| -------------- | ---------------------------------------------------- | ---------------------------------------------------- |
| Linguagem      | Python `TODO: versão`                                | Base do backend                                      |
| Framework web  | [FastAPI](https://fastapi.tiangolo.com/)             | Criação dos endpoints REST                           |
| Servidor ASGI  | [Uvicorn](https://www.uvicorn.org/)                  | Execução da aplicação                                |
| ORM            | [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/) | Mapeamento das tabelas e consultas                   |
| Validação      | [Pydantic v2](https://docs.pydantic.dev/)            | Schemas de entrada e saída                           |
| Migrações      | [Alembic](https://alembic.sqlalchemy.org/)           | Versionamento do esquema do banco                    |
| Banco de dados | [PostgreSQL](https://www.postgresql.org/)            | Persistência (em container Docker no ambiente local) |
| Driver         | [psycopg 3](https://www.psycopg.org/psycopg3/)       | Conexão Python ↔ Postgres                            |
| Relatórios     | [ReportLab](https://docs.reportlab.com/)             | Geração de PDFs                                      |
| Pacotes        | [uv](https://docs.astral.sh/uv/)                     | Gerenciamento de dependências e ambiente virtual     |
| Containers     | [Docker](https://www.docker.com/)                    | Banco Postgres local                                 |
| Deploy         | [Render](https://render.com/)                        | Hospedagem da API e do banco em produção             |

## Estrutura do projeto

> `TODO: ajustar para a árvore real do repositório`

```
backend/
├── alembic/
│   ├── versions/        # Arquivos de migração gerados pelo Alembic
│   └── env.py           # Configuração das migrações (lê a DATABASE_URL)
├── routers/             # Endpoints agrupados por recurso
├── schemas/             # Modelos Pydantic (entrada/saída da API)
├── config.py            # Configurações e DATABASE_URL
├── database.py          # Engine, sessão e dependência get_session
├── models.py            # Base e modelos SQLAlchemy
├── main.py              # Instância do FastAPI e registro dos routers
├── alembic.ini
├── pyproject.toml
├── uv.lock
└── .env.example
```

## Pré-requisitos

- [uv](https://docs.astral.sh/uv/getting-started/installation/) instalado
- [Docker](https://docs.docker.com/get-docker/) instalado e em execução
- Git

## Como rodar localmente

### 1. Clonar o repositório

```bash
git clone TODO: url-do-repositorio
cd TODO: pasta-do-backend
```

### 2. Instalar as dependências

```bash
uv sync
```

O `uv` cria o ambiente virtual (`.venv`) e instala as versões fixadas no `uv.lock`.

### 3. Subir o banco Postgres em um container

```bash
docker run -d \
  --name sentinela-postgres \
  -e POSTGRES_USER=TODO_usuario \
  -e POSTGRES_PASSWORD=TODO_senha \
  -e POSTGRES_DB=TODO_banco \
  -p 5433:5432 \
  -v sentinela-pgdata:/var/lib/postgresql/data \
  postgres:TODO_versao
```

> A porta **5433** do host é usada para não conflitar com um Postgres instalado nativamente na porta 5432. O volume `sentinela-pgdata` mantém os dados quando o container é recriado.

> `TODO: se o projeto usar docker-compose.yml, substituir este passo por "docker compose up -d"`

### 4. Configurar as variáveis de ambiente

```bash
cp .env.example .env
```

Edite o `.env` com os dados do container (veja [Variáveis de ambiente](#variáveis-de-ambiente)).

### 5. Aplicar as migrações

```bash
uv run alembic upgrade head
```

### 6. Iniciar a API

```bash
uv run uvicorn main:app --reload
```

A API ficará disponível em `http://localhost:8000`.

> `--reload` reinicia o servidor a cada alteração no código. Use **apenas em desenvolvimento**.

## Variáveis de ambiente

| Variável       | Descrição                                                | Exemplo                                                   |
| -------------- | -------------------------------------------------------- | --------------------------------------------------------- |
| `DATABASE_URL` | String de conexão com o Postgres                         | `postgresql+psycopg://usuario:senha@localhost:5433/banco` |
| `TODO`         | `TODO: chave secreta de autenticação, origens CORS etc.` |                                                           |

> ⚠️ Nunca versione o arquivo `.env`. Mantenha apenas o `.env.example`, sem valores reais.

## Migrações do banco (Alembic)

O esquema do banco é versionado com Alembic. O `alembic/env.py` lê a mesma `DATABASE_URL` da aplicação, garantindo que migrações e API usem o mesmo banco.

```bash
# Gerar uma nova migração a partir das alterações em models.py
uv run alembic revision --autogenerate -m "descricao da alteracao"

# Aplicar todas as migrações pendentes
uv run alembic upgrade head

# Desfazer a última migração
uv run alembic downgrade -1

# Ver a revisão atual do banco
uv run alembic current
```

> Sempre revise o arquivo gerado em `alembic/versions/` antes de aplicar: o `--autogenerate` não detecta tudo (por exemplo, renomeação de colunas).

## Documentação da API

Com a API rodando, o FastAPI gera a documentação interativa automaticamente:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

### Principais endpoints

> `TODO: completar com os endpoints reais`

| Método | Rota                 | Descrição               |
| ------ | -------------------- | ----------------------- |
| `GET`  | `/notificacoes`      | Lista as notificações   |
| `GET`  | `/notificacoes/{id}` | Detalha uma notificação |
| `GET`  | `TODO`               | Gera relatório em PDF   |

## Deploy

O backend é hospedado no **Render**, com banco PostgreSQL gerenciado.

| Configuração  | Valor                                                                                                                          |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Build command | `uv sync --frozen && uv cache prune --ci`                                                                                      |
| Start command | `uv run alembic upgrade head && uv run uvicorn main:app --host 0.0.0.0 --port $PORT --proxy-headers --forwarded-allow-ips="*"` |

As migrações são aplicadas automaticamente a cada deploy, antes de a API iniciar.

## Segurança e dados sensíveis

O sistema lida com **dados de saúde**, considerados dados pessoais sensíveis pela LGPD (Lei nº 13.709/2018). Por isso:

- Não versione credenciais, `.env` ou dumps do banco
- Não use dados reais em ambiente de desenvolvimento
- Endpoints de detalhe devem verificar se o recurso pertence à superintendência do usuário autenticado
- Faça backup (`pg_dump`) antes de operações destrutivas no banco

## Contribuindo

1. Crie uma branch a partir da `main`: `git checkout -b feature/nome-da-feature`
2. Faça commits pequenos e descritivos
3. Se alterar `models.py`, gere e revise a migração do Alembic
4. Abra um Pull Request descrevendo o que mudou e como testar

## Licença

`TODO: definir licença (ex.: MIT) ou indicar "uso restrito"`

## Autor

**Pedro** — `TODO: GitHub / LinkedIn`
