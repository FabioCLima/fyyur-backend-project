# Plano de Implementação — fyyur-backend-project

> Documento-guia em **Markdown** para implementar o backend profissional e didático do projeto **fyyur-backend-project**.
> Usa `uv` (substituto moderno do pip) para criação/gerenciamento de ambiente e dependências, **Pydantic** para schemas e validação, SQLAlchemy + Flask-Migrate para ORM e migrações.

---

## Sumário
1. Visão Geral / Objetivos
2. Arquitetura proposta
3. Estrutura de pastas (sugerida)
4. Ambiente de desenvolvimento com `uv`
5. Dependências principais
6. Modelagem do banco (ER / SQLAlchemy)
7. Pydantic: schemas & validações (request/response)
8. Flask + Blueprints: rotas e controladores
9. Formulários / Compatibilidade com templates existentes
10. Migrações e seed data
11. Testes automatizados
12. Checklist de aceitação (mapeamento com critérios)
13. Tarefas passo-a-passo (roadmap com comandos)
14. Dicas de qualidade, segurança e deploy
15. Anexos: snippets de código importantes

---

## 1. Visão Geral / Objetivos
- Completar a aplicação Fyyur: trocar *mock data* por modelos reais (PostgreSQL) e endpoints que manipulam os dados.
- Tornar projeto profissional, com validação robusta (Pydantic), migrações (Flask-Migrate), testes e padrão de projeto claro (separação de responsabilidades).
- Usar `uv` em vez de `pip` para gerenciar ambiente + dependências.
- Documentar tudo para que possa ser exportado para a pasta do projeto e servir como guia.

---

## 2. Arquitetura proposta (alto nível)

```
Client (browser) <---> Flask app (app.py / blueprints) <---> SQLAlchemy models (models.py)
                                         |--> Pydantic schemas (schemas.py)
                                         |--> Services / Repositories (services/)
                                         |--> Migrations (migrations/ via Flask-Migrate)
                                         |--> Tests (tests/)
```

- **Flask (WSGI)** para servir templates (já existentes) e endpoints. Mantemos o `app.py` como *entry point* mínimo, mas refatoramos para usar **Blueprints** (`venues`, `artists`, `shows`, `main`).
- **SQLAlchemy** para ORM; definimos os modelos normalizados em `models.py`.
- **Flask-Migrate** para gerenciar migrações (Alembic).
- **Pydantic** para validação de payloads (quando criamos endpoints JSON/REST) e para checar dados vindos de formulários antes de persistir no DB.
- **Services / Repositories**: lógica de negócio e queries complexas ficam em `services/`.
- **Tests** com pytest e factory-boy (ou fixtures) para criar dados.

---

## 3. Estrutura de pastas (sugerida)

```
project_root/
├── app.py                      # entrypoint - cria app e registra blueprints
├── config.py
├── models.py                   # SQLAlchemy models (normalized)
├── schemas.py                  # Pydantic schemas (requests/responses)
├── services/                   # regras de negócio / abstração com DB
│   ├── __init__.py
│   ├── venue_service.py
│   └── artist_service.py
├── controllers/                # blueprints (venues, artists, shows)
│   ├── __init__.py
│   ├── venues.py
│   ├── artists.py
│   └── shows.py
├── templates/                   # já existe
├── static/                      # já existe
├── forms.py                    # mantém compatibilidade com frontend
├── migrations/                 # gerado pelo flask-migrate
├── requirements.txt            # lock mínimo (compatibilidade)
├── pyproject.toml              # opcional (uv-friendly)
├── README.md
├── fabfile.py                  # já existe - mantém utilidades
└── tests/
    ├── conftest.py
    ├── test_venues.py
    └── test_artists.py
```

> Observação: manter `forms.py` para os templates WTForms. Pydantic será usado nas validações do backend API / endpoints JSON e também como um validador adicional no controller antes de persistir dados.

---

## 4. Ambiente de desenvolvimento com `uv`

Assumimos que o usuário quer usar **`uv`** (o novo package manager/venv tool criado por Astral) — ferramenta compatível com substituição de `python -m venv` + `pip`.

### Instalação rápida (local)
```bash
# instale uv (ex.: via cargo / prebuilt). Exemplo com brew (macOS) ou cargo:
# macOS (Homebrew)
brew install uv
# ou (Linux) via curl/prebuilt — siga docs oficiais: https://astral.sh/uv/
```

### Criar ambiente & instalar dependências
```bash
# inicializar projeto (opcional)
uv init

# criar virtualenv (cria .venv por padrão)
uv venv

# ativar (se quiser usar shell), uv também oferece 'uv run'
source .venv/bin/activate

# instalar dependências a partir de requirements (uv add ou uv add -r?)
# uv suporta comandos análogos, por exemplo:
uv add -r requirements.txt

# ou adicionar pacotes manualmente
uv add flask flask-sqlalchemy flask-migrate pydantic psycopg[binary] pytest
```

> `uv add` é o modo equivalente a `pip install`; `uv venv` cria ambientes. Consulte `uv` docs se desejar travar um lockfile ou usar `pyproject.toml`.

---

## 5. Dependências principais (sugeridas)
- flask
- flask_sqlalchemy
- flask_migrate
- flask_wtf (para compatibilidade com templates existentes)
- python-dotenv (para variáveis de ambiente locais)
- pydantic
- psycopg[binary] (driver PostgreSQL)
- uv (ferramenta do dev)
- pytest, pytest-flask (para testes)

Adicione versões compatíveis ao `requirements.txt` ou gere `pyproject.toml` e use `uv` para instalar.

---

## 6. Modelagem do banco (ER) — proposta

Entidades: `Venue`, `Artist`, `Show`.

- `Venue` (1) --- (M) `Show` (M) --- (1) `Artist`

### Colunas principais (sugestão)
**Venue**
- id: Integer PK
- name: String (not null)
- city: String
- state: String(2) (use enum ou validacao)
- address: String
- phone: String
- image_link: String
- facebook_link: String
- website_link: String
- genres: ARRAY / association table (prefer normalizar: venue_genres)
- seeking_talent: Boolean default False
- seeking_description: Text
- created_at / updated_at: timestamps

**Artist**
- id: Integer PK
- name: String not null
- city / state
- phone
- image_link
- facebook_link
- website_link
- genres: ARRAY / association table
- seeking_venue: Boolean
- seeking_description: Text
- availability (optional advanced)
- created_at / updated_at

**Show**
- id: Integer PK
- artist_id: FK -> Artist.id
- venue_id: FK -> Venue.id
- start_time: DateTime not null
- created_at

> Recomendo modelar `genres` como uma tabela auxiliar `genres` + association tables (`artist_genres`, `venue_genres`) para ficar 3NF. Se quiser praticidade e compatibilidade com deploy local, usar um `db.Column(db.ARRAY(db.String))` também funciona no Postgres.

### Exemplo (SQLAlchemy snippet) — ver seção de anexos.

---

## 7. Pydantic: schemas & validações

Criar `schemas.py` com classes Pydantic que representam payloads de entrada e saída.

### Benefícios
- validação rigorosa antes de salvar no DB
- conversões automáticas (ISO datetimes)
- documentação clara dos campos

### Exemplo de Schemas
```py
from pydantic import BaseModel, HttpUrl, constr
from datetime import datetime
from typing import List, Optional

class VenueCreate(BaseModel):
    name: constr(min_length=1)
    city: str
    state: constr(min_length=2, max_length=2)
    address: str
    phone: Optional[str] = None
    image_link: Optional[HttpUrl] = None
    facebook_link: Optional[HttpUrl] = None
    website_link: Optional[HttpUrl] = None
    genres: List[str]
    seeking_talent: Optional[bool] = False
    seeking_description: Optional[str] = None

class ShowCreate(BaseModel):
    artist_id: int
    venue_id: int
    start_time: datetime
```

### Onde usar
- em endpoints que consomem JSON
- ao processar `form.data` do Flask-WTF — crie um objeto `VenueCreate(**form.data)` antes de persistir

---

## 8. Flask + Blueprints: rotas e controladores

Refatore `app.py` para ter registro de blueprints. Cada blueprint deve:
- validar entrada com Pydantic
- chamar `services` para executar operações com o DB
- retornar templates já existentes com dados vindos do DB (formatação conforme mocks originais)

### Exemplos de endpoints principais
- `GET /venues` — lista agrupada por city/state (agregação)
- `POST /venues/create` — criar venue (validar via Pydantic), flash success/failure
- `GET /venues/<id>` — exibir detalhes: separar shows em past / upcoming (compare `start_time`)
- `POST /venues/search` — partial, case-insensitive query (`ilike('%term%')`)
- Análogos para `artists` e `shows`

---

## 9. Formulários / Compatibilidade com templates existentes

O projeto já vem com templates e `forms.py` (WTForms). Estratégia:
- manter WTForms para render/form handling (frontend compatibility);
- ao submeter, ainda use `form.validate_on_submit()`; em seguida converta os dados para Pydantic schema (ex.: `VenueCreate(**form.data)`) para camadas extras de validação e normalização (por ex., garantir `state` len=2, `genres` não vazio, facebook url válido).

---

## 10. Migrações e seed data

### Configuração Flask-Migrate
- inicialize `migrate = Migrate(app, db)` em `app.py` após `db = SQLAlchemy(app)`
- comandos úteis:
  - `flask db init` (uma vez)
  - `flask db migrate -m "create models"`
  - `flask db upgrade`

### Seed (opcional)
Criar script `scripts/seed.py` que adiciona alguns venues, artists e shows — útil para desenvolvimento.

---

## 11. Testes automatizados
- `pytest` + `pytest-flask`
- criar fixtures para app e banco (usar sqlite in-memory ou um postgres container) — preferir Postgres para paridade.
- testes a cobrir:
  - criação de venue/artist/show
  - search funciona (case-insensitive, partial)
  - show listing mostra upcoming/past corretamente
  - endpoints retorno status 200 e templates corretos

---

## 12. Checklist de aceitação (mapeamento com critérios)
Cada item abaixo descreve o que deve estar implementado para atender os critérios do projeto.

- [ ] Conexão funcional com PostgreSQL (`SQLALCHEMY_DATABASE_URI` configurado) — *config.py*.
- [ ] Modelos completos (Venue, Artist, Show) e normalizados — *models.py*.
- [ ] Migrações funcionam: `flask db migrate` + `flask db upgrade` criam tabelas.
- [ ] Não há mock data hardcoded nas views (usar DB queries para preencher dados).
- [ ] Criação de registros via formulários (create endpoints) persistem no DB.
- [ ] `/artists` e `/venues` exibem dados reais do DB.
- [ ] `/artists/<id>` e `/venues/<id>` mostram dados reais e separam past/upcoming shows.
- [ ] Busca parcial e case-insensitive implementada (ilike)
- [ ] Relações FK e integridade referencial entre Show-Artist-Venue.
- [ ] Documentação de como rodar com `uv` incluída.

---

## 13. Tarefas passo-a-passo (roadmap com comandos)

1. **Preparar ambiente com uv**
```bash
uv venv
source .venv/bin/activate
uv add -r requirements.txt pydantic flask-migrate psycopg[binary]
```

2. **Refatorar projeto (arquivos principais)**
- mover models para `models.py`
- criar `schemas.py` com Pydantic
- criar `controllers/` com blueprints
- criar `services/` para consultas pesadas

3. **Configurar config.py**
- usar `python-dotenv` ou variáveis de ambiente. Exemplo:
```py
import os
from dotenv import load_dotenv
load_dotenv()
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'postgresql://postgres@127.0.0.1:5432/fyyur'
```

4. **Instalar e configurar Flask-Migrate**
```py
from flask_migrate import Migrate
migrate = Migrate(app, db)
```

5. **Criar migrações**
```bash
flask db init    # se ainda não existir
flask db migrate -m "initial models"
flask db upgrade
```

6. **Implementar controllers + services**
- substituir mock data por queries SQLAlchemy
- garantir agrupamento por cidade/estado para /venues

7. **Validar formulários com Pydantic**
- converter `form.data` -> `VenueCreate(**form.data)`;
- em caso de erro: `flash` com mensagem amigável e voltar ao form

8. **Testes**
```bash
pytest -q
```

---

## 14. Dicas de qualidade, segurança e deploy
- **Nunca** commitar credenciais. Use `.env` e `python-dotenv` para desenvolvimento.
- Adicione `flask db migrate` e `flask db upgrade` ao `fabfile.py` se desejar facilitar deploy.
- Configurar `error.log` e logging — app já tem um handler.
- Sanitizar entrada e validar com Pydantic.
- Considerar criar endpoints JSON (API) para futura integração com frontend JS.

---

## 15. Anexos: snippets de código (copiar para files indicados)

### 15.1 `models.py` (exemplo resumido)
```py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

artist_genres = db.Table(
    'artist_genres',
    db.Column('artist_id', db.Integer, db.ForeignKey('artists.id'), primary_key=True),
    db.Column('genre', db.String, primary_key=True)
)

venue_genres = db.Table(
    'venue_genres',
    db.Column('venue_id', db.Integer, db.ForeignKey('venues.id'), primary_key=True),
    db.Column('genre', db.String, primary_key=True)
)

class Venue(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(2))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(200))
    website_link = db.Column(db.String(200))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    artists = db.relationship('Show', back_populates='venue', cascade='all, delete-orphan')

class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(2))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(200))
    website_link = db.Column(db.String(200))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    shows = db.relationship('Show', back_populates='artist', cascade='all, delete-orphan')

class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    artist = db.relationship('Artist', back_populates='shows')
    venue = db.relationship('Venue', back_populates='artists')
```

### 15.2 `schemas.py` (Pydantic)
```py
from pydantic import BaseModel, HttpUrl, constr
from datetime import datetime
from typing import List, Optional

class VenueCreate(BaseModel):
    name: constr(min_length=1)
    city: str
    state: constr(min_length=2, max_length=2)
    address: str
    phone: Optional[str] = None
    image_link: Optional[HttpUrl] = None
    facebook_link: Optional[HttpUrl] = None
    website_link: Optional[HttpUrl] = None
    genres: List[str]
    seeking_talent: Optional[bool] = False
    seeking_description: Optional[str] = None

class ShowCreate(BaseModel):
    artist_id: int
    venue_id: int
    start_time: datetime
```

### 15.3 Query exemplo para search (case-insensitive partial)
```py
from sqlalchemy import func

term = '%{}%'.format(search_term)
venues = Venue.query.filter(func.lower(Venue.name).ilike(func.lower(term))).all()
# or simpler with ilike on Postgres
venues = Venue.query.filter(Venue.name.ilike(f"%{search_term}%")).all()
```

---

## Final — Roadmap mínimo de entrega (sprint)
- **Dia 1:** setup `uv`, instalar deps, mover `models.py`, config DB.
- **Dia 2:** implementar models + flask-migrate + executar `flask db upgrade`.
- **Dia 3:** implementar controllers que substituem mock data por queries; validacao com Pydantic.
- **Dia 4:** testes básicos e seed data; corrigir bugs.
- **Dia 5:** finalizar docs, checklist e refinamentos (artist availability extra se houver tempo).

---

Se desejar, eu já gero os arquivos `models.py`, `schemas.py` e um `controllers/venues.py` baseado nos arquivos atuais (`app.py`, `forms.py`, `config.py`) e preparo o `fabfile.py`/scripts para rodar `flask db migrate` e `uv` commands. Quer que eu crie estes arquivos agora no diretório do projeto (posso gerar o conteúdo pronto para você copiar/colar)?

