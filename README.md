# Fyyur Backend Project

Aplicação Flask profissional para agendamento de shows musicais entre artistas e venues.

## 📋 Visão Geral

Fyyur é uma plataforma que facilita a descoberta e agendamento de shows entre artistas locais e venues musicais. A aplicação permite:

- ✅ Listar novos artistas e venues
- ✅ Descobrir artistas e venues existentes
- ✅ Agendar shows entre artistas e venues
- ✅ Buscar artistas e venues por nome, cidade e estado
- ✅ Visualizar detalhes completos de artistas e venues
- ✅ Distinguir entre shows passados e futuros

## 🏗️ Arquitetura

O projeto segue uma arquitetura em camadas profissional:

```
fyyur-backend-project/
├── app/                          # Pacote principal da aplicação
│   ├── __init__.py              # Application Factory
│   ├── models/                  # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   ├── base.py             # Modelo base e configuração SQLAlchemy
│   │   ├── artist.py           # Modelo Artist
│   │   ├── venue.py            # Modelo Venue
│   │   ├── show.py             # Modelo Show
│   │   └── genre.py            # Modelo Genre
│   ├── schemas/                 # Schemas Pydantic para validação
│   │   ├── __init__.py
│   │   ├── common.py           # Schemas base
│   │   ├── artist_schema.py    # Schemas de Artist
│   │   ├── venue_schema.py     # Schemas de Venue
│   │   └── show_schema.py      # Schemas de Show
│   ├── repositories/            # Camada de acesso a dados
│   │   ├── __init__.py
│   │   ├── base.py             # Repository base
│   │   ├── artist_repository.py
│   │   ├── venue_repository.py
│   │   ├── show_repository.py
│   │   └── genre_repository.py
│   ├── services/                # Camada de lógica de negócio
│   │   ├── __init__.py
│   │   ├── base.py             # Service base
│   │   ├── artist_service.py
│   │   ├── venue_service.py
│   │   ├── show_service.py
│   │   └── genre_service.py
│   ├── controllers/             # Camada de controle (rotas)
│   │   ├── __init__.py
│   │   ├── main.py             # Rotas principais
│   │   ├── artists.py          # Rotas de artistas
│   │   ├── venues.py           # Rotas de venues
│   │   └── shows.py            # Rotas de shows
│   ├── exceptions/              # Exceções customizadas
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── errors.py
│   └── utils/                   # Utilitários
│       ├── __init__.py
│       ├── validators.py       # Validadores customizados
│       ├── formatters.py       # Formatadores
│       └── constants.py        # Constantes
├── templates/                   # Templates Jinja2
│   ├── layouts/
│   ├── pages/
│   ├── forms/
│   └── errors/
├── static/                      # Arquivos estáticos
│   ├── css/
│   ├── js/
│   ├── img/
│   └── ico/
├── migrations/                  # Migrações do banco
├── scripts/                    # Scripts utilitários
│   ├── seed.py                # Script para popular banco
│   ├── db_utils.py
│   └── check_db.py
├── tests/                      # Testes automatizados
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── docs/                       # Documentação
├── app.py                      # Ponto de entrada da aplicação
├── config.py                   # Configurações
├── forms.py                    # Formulários WTForms
├── requirements.txt            # Dependências Python
├── pyproject.toml             # Configuração do projeto
└── README.md                  # Este arquivo
```

## 🚀 Tecnologias Utilizadas

### Backend
- **Python 3.13** - Linguagem principal
- **Flask** - Framework web
- **SQLAlchemy** - ORM para banco de dados
- **Flask-Migrate** - Migrações de banco
- **Pydantic** - Validação de dados e schemas
- **PostgreSQL/SQLite** - Banco de dados
- **WTForms** - Formulários web

### Ferramentas de Desenvolvimento
- **uv** - Gerenciador de pacotes e ambiente virtual
- **ruff** - Linter e formatador Python
- **pytest** - Framework de testes
- **Bootstrap 3** - Framework CSS frontend

## 📦 Instalação e Configuração

### 1. Clonar o Repositório
```bash
git clone <repository-url>
cd fyyur-backend-project
```

### 2. Configurar Ambiente Virtual
```bash
# Instalar uv (se não estiver instalado)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Criar e ativar ambiente virtual
uv venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate      # Windows
```

### 3. Instalar Dependências

#### Opção A: Usando pip (Recomendado para Revisão)
```bash
pip install -r requirements.txt
```

#### Opção B: Usando uv (Desenvolvimento Moderno)
```bash
# Instalar uv (se não estiver instalado)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Instalar dependências
uv pip install -r requirements.txt
# ou
uv sync
```

### 4. Configurar Banco de Dados
```bash
# Copiar arquivo de configuração
cp env.example .env

# Editar .env com suas configurações de banco
# Para SQLite (desenvolvimento):
DATABASE_URL=sqlite:///fyyur.db

# Para PostgreSQL (produção):
# DATABASE_URL=postgresql://user:password@localhost:5432/fyyur
```

### 5. Executar Migrações
```bash
# Inicializar migrações (primeira vez)
flask db init

# Criar migração
flask db migrate -m "Initial migration"

# Aplicar migrações
flask db upgrade
```

### 6. Popular Banco com Dados de Exemplo
```bash
python scripts/seed.py
```

### 7. Executar Aplicação

#### Opção A: Usando pip
```bash
python app.py
```

#### Opção B: Usando uv
```bash
uv run python app.py
```

A aplicação estará disponível em: `http://127.0.0.1:5000`

## 🧪 Testes

### Executar Todos os Testes
```bash
pytest
```

### Executar Testes com Cobertura
```bash
pytest --cov=app tests/
```

### Executar Testes Específicos
```bash
pytest tests/unit/test_models.py
pytest tests/unit/test_controllers.py
```

## 📊 Funcionalidades Implementadas

### ✅ Critérios Obrigatórios Atendidos

#### **Modelos de Dados**
- ✅ Modelos relacionais e normalizados (3NF)
- ✅ Relacionamentos corretos entre Artist, Venue e Show
- ✅ Chaves estrangeiras implementadas
- ✅ Conexão com PostgreSQL/SQLite
- ✅ Migrações com Flask-Migrate

#### **Funcionalidades da Aplicação**
- ✅ Criação de novos venues, artists e shows
- ✅ Busca por venues e artists (case-insensitive, partial matching)
- ✅ Páginas de detalhes para artistas e venues específicos
- ✅ Distinção entre shows passados e futuros
- ✅ Agrupamento de venues por cidade e estado
- ✅ Links funcionais entre artistas e venues nos shows

#### **Qualidade do Código**
- ✅ Arquitetura em camadas (Models, Repositories, Services, Controllers)
- ✅ Separação de responsabilidades
- ✅ Validação de formulários com Pydantic
- ✅ Tratamento de erros customizado
- ✅ Código bem documentado e comentado

### 🌟 Funcionalidades Extras Implementadas

#### **Recursos Avançados**
- ✅ **API RESTful** - Endpoints JSON para integração
- ✅ **Schemas Pydantic** - Validação robusta de dados
- ✅ **Arquitetura em Camadas** - Separação clara de responsabilidades
- ✅ **Repositories Pattern** - Abstração de acesso a dados
- ✅ **Services Pattern** - Lógica de negócio centralizada
- ✅ **Exceções Customizadas** - Tratamento de erros profissional
- ✅ **Logging Configurado** - Sistema de logs estruturado
- ✅ **Testes Automatizados** - Cobertura de testes unitários
- ✅ **Linting e Formatação** - Código padronizado com ruff
- ✅ **Documentação Completa** - README e documentação técnica

## 🔧 Configuração de Desenvolvimento

### Variáveis de Ambiente
```bash
# .env
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=sqlite:///fyyur.db
SECRET_KEY=your-secret-key-here
```

### Comandos Úteis
```bash
# Formatar código
ruff format .

# Verificar linting
ruff check .

# Executar aplicação em modo debug
FLASK_ENV=development python app.py

# Criar nova migração
flask db migrate -m "Description of changes"

# Aplicar migrações
flask db upgrade

# Reverter migração
flask db downgrade
```

## 📈 Estrutura do Banco de Dados

### Tabelas Principais
- **artists** - Informações dos artistas
- **venues** - Informações dos venues
- **shows** - Shows agendados (relaciona artistas e venues)
- **genres** - Gêneros musicais
- **artist_genres** - Relacionamento many-to-many entre artistas e gêneros
- **venue_genres** - Relacionamento many-to-many entre venues e gêneros

### Relacionamentos
- **Artist ↔ Show** - One-to-Many (um artista pode ter vários shows)
- **Venue ↔ Show** - One-to-Many (um venue pode ter vários shows)
- **Artist ↔ Genre** - Many-to-Many (um artista pode ter vários gêneros)
- **Venue ↔ Genre** - Many-to-Many (um venue pode ter vários gêneros)

## 🚀 Deploy

### Desenvolvimento Local
```bash
python app.py
```

### Produção
```bash
# Usar WSGI server como Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🐛 Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'dotenv'"
```bash
# Instalar python-dotenv especificamente
pip install python-dotenv==1.1.1

# Ou reinstalar todas as dependências
pip install -r requirements.txt
```

### Erro: "ModuleNotFoundError: No module named 'flask'" (com uv)
```bash
# Usar uv para executar
uv run python app.py

# Ou ativar ambiente virtual primeiro
source .venv/bin/activate
python app.py
```

### Erro: "Address already in use" / "Port 5000 is in use"
```bash
# A aplicação agora encontra automaticamente uma porta livre
# Se 5000 estiver ocupada, usará 5001, 5002, etc.
python app.py

# Ou matar processos na porta 5000
lsof -ti:5000 | xargs kill -9
python app.py
```

### Erro: "No such file or directory: 'fyyur.db'"
```bash
# Executar migrações para criar o banco
flask db upgrade

# Ou executar o seed que cria o banco automaticamente
python scripts/seed.py
```

### Erro: "Template not found"
```bash
# Verificar se está executando do diretório correto
cd /path/to/fyyur-backend-project
python app.py
```

### Verificar Instalação
```bash
# Testar importação do dotenv
python -c "from dotenv import load_dotenv; print('python-dotenv OK')"

# Testar configuração
python -c "import config; print('Config OK')"

# Testar aplicação Flask
python -c "from app import create_app; print('Flask App OK')"
```

## 📚 Documentação Adicional

- **[Guia de Teste](./docs/TESTING_GUIDE.md)** - Instruções detalhadas para testar a aplicação
- **[Plano de Implementação](./docs/fyuur_backend_implementation_plan2.md)** - Documentação técnica completa
- **[Índice da Documentação](./docs/INDEX.md)** - Navegação de todos os documentos

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](./docs/LICENSE.txt) para detalhes.

## 👥 Autores

- **Fyyur Team** - Desenvolvimento inicial
- **Backend Developer** - Implementação e melhorias

## 🙏 Agradecimentos

- Udacity pelo projeto base
- Comunidade Flask pela documentação
- Contribuidores do SQLAlchemy e Pydantic

---

**🎵 Fyyur - Conectando Artistas e Venues Musicalmente! 🎵**