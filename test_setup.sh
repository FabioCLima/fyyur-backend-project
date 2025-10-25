#!/bin/bash

# Script de Teste Rápido para o Projeto Fyyur
# Este script testa se todas as dependências estão funcionando

echo "🧪 Testando Projeto Fyyur..."
echo "================================"

# Teste 1: Verificar Python
echo "1. Verificando Python..."
python3 --version
if [ $? -eq 0 ]; then
    echo "   ✅ Python OK"
else
    echo "   ❌ Python não encontrado"
    exit 1
fi

# Teste 2: Verificar se uv está disponível
echo "2. Verificando uv..."
if command -v uv &> /dev/null; then
    echo "   ✅ uv disponível"
    UV_AVAILABLE=true
else
    echo "   ⚠️  uv não encontrado - usando pip"
    UV_AVAILABLE=false
fi

# Teste 3: Instalar dependências
echo "3. Instalando dependências..."
if [ "$UV_AVAILABLE" = true ]; then
    echo "   Usando uv..."
    uv pip install -r requirements.txt
else
    echo "   Usando pip..."
    pip install -r requirements.txt
fi

if [ $? -eq 0 ]; then
    echo "   ✅ Dependências instaladas"
else
    echo "   ❌ Erro ao instalar dependências"
    exit 1
fi

# Teste 4: Testar importações
echo "4. Testando importações..."
if [ "$UV_AVAILABLE" = true ]; then
    uv run python3 -c "from dotenv import load_dotenv; print('   ✅ python-dotenv OK')"
    uv run python3 -c "import config; print('   ✅ Config OK')"
    uv run python3 -c "from app import create_app; print('   ✅ Flask App OK')"
else
    python3 -c "from dotenv import load_dotenv; print('   ✅ python-dotenv OK')"
    python3 -c "import config; print('   ✅ Config OK')"
    python3 -c "from app import create_app; print('   ✅ Flask App OK')"
fi

# Teste 5: Executar migrações
echo "5. Executando migrações..."
if [ "$UV_AVAILABLE" = true ]; then
    uv run flask db upgrade
else
    flask db upgrade
fi

if [ $? -eq 0 ]; then
    echo "   ✅ Migrações executadas"
else
    echo "   ⚠️  Migrações falharam - tentando criar banco manualmente"
fi

# Teste 6: Popular banco com dados
echo "6. Populando banco com dados..."
if [ "$UV_AVAILABLE" = true ]; then
    uv run python3 scripts/seed.py
else
    python3 scripts/seed.py
fi

if [ $? -eq 0 ]; then
    echo "   ✅ Banco populado com sucesso"
else
    echo "   ⚠️  Erro ao popular banco"
fi

echo ""
echo "🎉 Testes concluídos!"
echo ""
echo "Para executar a aplicação:"
if [ "$UV_AVAILABLE" = true ]; then
    echo "   uv run python3 app.py"
else
    echo "   python3 app.py"
fi
echo ""
echo "A aplicação encontrará automaticamente uma porta livre (5000-5010)"
echo "Acesse a URL mostrada no console quando a aplicação iniciar"
echo ""
echo "Se a porta 5000 estiver ocupada, a aplicação usará 5001, 5002, etc."
