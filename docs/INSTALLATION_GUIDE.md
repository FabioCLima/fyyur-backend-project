# Instruções de Instalação e Execução

## 🚀 Como Executar o Projeto Fyyur

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python) OU uv (gerenciador moderno)

## 📦 Opção 1: Usando pip (Recomendado para Revisão)

### 1. Instalar Dependências
```bash
# Instalar todas as dependências do requirements.txt
pip install -r requirements.txt
```

### 2. Executar a Aplicação
```bash
# Executar a aplicação Flask
python app.py
```

## ⚡ Opção 2: Usando uv (Desenvolvimento Moderno)

### 1. Instalar uv (se não estiver instalado)
```bash
# Instalar uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Ou usando pip
pip install uv
```

### 2. Instalar Dependências
```bash
# Instalar dependências usando uv
uv pip install -r requirements.txt

# Ou sincronizar com pyproject.toml
uv sync
```

### 3. Executar a Aplicação
```bash
# Executar usando uv (recomendado)
uv run python app.py

# Ou ativar ambiente e executar
source .venv/bin/activate
python app.py
```

### 2. Configurar Banco de Dados

```bash
# Copiar arquivo de configuração de exemplo
cp env.example .env

# Editar .env com suas configurações (opcional para desenvolvimento)
# Para SQLite (padrão): não precisa alterar nada
# Para PostgreSQL: descomente e configure DATABASE_URL
```

### 3. Executar Migrações do Banco

```bash
# Inicializar migrações (primeira vez apenas)
flask db init

# Criar migração inicial
flask db migrate -m "Initial migration"

# Aplicar migrações ao banco
flask db upgrade
```

### 4. Popular Banco com Dados de Exemplo

```bash
# Executar script de seed para popular o banco
python scripts/seed.py
```

### 5. Executar a Aplicação

```bash
# Executar a aplicação Flask
python app.py
```

A aplicação estará disponível em: **http://127.0.0.1:5000**

## 🔧 Comandos Alternativos

### Usando Flask CLI
```bash
# Definir variável de ambiente
export FLASK_APP=app.py

# Executar aplicação
flask run
```

### Usando Python diretamente
```bash
# Executar arquivo principal
python app.py
```

## 🧪 Executar Testes

```bash
# Executar todos os testes
pytest

# Executar testes com cobertura
pytest --cov=app tests/

# Executar testes específicos
pytest tests/unit/test_models.py
```

## 📋 Verificação de Funcionamento

Após executar a aplicação, você deve conseguir:

1. **Acessar a página inicial**: http://127.0.0.1:5000
2. **Navegar pelos menus**: Venues, Artists, Shows
3. **Criar novos registros**: Venues, Artists, Shows
4. **Buscar registros**: Por nome, cidade, estado
5. **Visualizar detalhes**: Páginas individuais de venues e artists

## 🐛 Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'dotenv'"
```bash
# Instalar python-dotenv
pip install python-dotenv

# Ou reinstalar todas as dependências
pip install -r requirements.txt
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

## 📁 Estrutura do Projeto

```
fyyur-backend-project/
├── app/                    # Código principal da aplicação
├── templates/             # Templates HTML
├── static/               # Arquivos estáticos (CSS, JS, imagens)
├── migrations/           # Migrações do banco de dados
├── scripts/             # Scripts utilitários
├── tests/               # Testes automatizados
├── docs/                # Documentação
├── app.py               # Ponto de entrada da aplicação
├── config.py            # Configurações
├── requirements.txt     # Dependências Python
└── README.md           # Documentação principal
```

## ✅ Checklist de Verificação

- [ ] Python 3.8+ instalado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Banco de dados configurado (`flask db upgrade`)
- [ ] Dados de exemplo carregados (`python scripts/seed.py`)
- [ ] Aplicação executando (`python app.py`)
- [ ] Página inicial acessível (http://127.0.0.1:5000)
- [ ] Funcionalidades testadas (criar, buscar, visualizar)

---

**🎵 Fyyur - Conectando Artistas e Venues Musicalmente! 🎵**
