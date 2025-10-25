# 🧪 Guia de Teste - Fyyur Backend Project

Este guia fornece instruções passo a passo para testar todas as funcionalidades do projeto Fyyur como usuário.

## 📋 Pré-requisitos

- ✅ Projeto configurado e rodando
- ✅ Banco de dados populado com dados de exemplo
- ✅ Servidor Flask executando na porta 5000

## 🚀 Iniciando o Projeto

### 1. Ativar Ambiente Virtual
```bash
source .venv/bin/activate
```

### 2. Executar o Servidor
```bash
uv run python app.py
```

### 3. Verificar se está Rodando
```bash
curl -I http://127.0.0.1:5000
# Deve retornar: HTTP/1.1 200 OK
```

## 🌐 Testando a Interface Web

### 1. Acessar a Homepage
- **URL:** http://127.0.0.1:5000
- **O que verificar:**
  - ✅ Página carrega sem erros
  - ✅ Logo "🔥" aparece no topo
  - ✅ Menu de navegação (Venues, Artists, Shows)
  - ✅ Campos de busca aparecem conforme a página

### 2. Testar Navegação Principal

#### 📍 Página de Venues
- **URL:** http://127.0.0.1:5000/venues/
- **O que verificar:**
  - ✅ Lista de venues é exibida
  - ✅ Campo "Find a venue" aparece no topo
  - ✅ Botão "List a new venue" funciona

#### 🎤 Página de Artists
- **URL:** http://127.0.0.1:5000/artists/
- **O que verificar:**
  - ✅ Lista de artistas é exibida
  - ✅ Campo "Find an artist" aparece no topo
  - ✅ Botão "List a new artist" funciona

#### 🎭 Página de Shows
- **URL:** http://127.0.0.1:5000/shows/
- **O que verificar:**
  - ✅ Lista de shows é exibida
  - ✅ Botão "List a new show" funciona

## 🔍 Testando Funcionalidades de Busca

### 1. Buscar Venues
- **Como testar:**
  1. Acesse http://127.0.0.1:5000/venues/
  2. Digite "Musical" no campo "Find a venue"
  3. Pressione Enter
- **Resultado esperado:**
  - ✅ Página de resultados aparece
  - ✅ Mostra "Number of search results for 'Musical': 1"
  - ✅ Lista "The Musical Hop" nos resultados

### 2. Buscar Artists
- **Como testar:**
  1. Acesse http://127.0.0.1:5000/artists/
  2. Digite "Guns" no campo "Find an artist"
  3. Pressione Enter
- **Resultado esperado:**
  - ✅ Página de resultados aparece
  - ✅ Mostra "Number of search results for 'Guns': 1"
  - ✅ Lista "Guns N Petals" nos resultados

## ➕ Testando Formulários de Criação

### 1. Criar Novo Venue
- **Como testar:**
  1. Acesse http://127.0.0.1:5000/venues/create
  2. Preencha o formulário:
     - **Name:** "Test Venue"
     - **City:** "São Paulo"
     - **State:** "SP"
     - **Phone:** "11-99999-9999"
     - **Genres:** Selecione "Rock n Roll"
  3. Clique em "Create Venue"
- **Resultado esperado:**
  - ✅ Venue é criado com sucesso
  - ✅ Redirecionamento para página de venues
  - ✅ Novo venue aparece na lista

### 2. Criar Novo Show
- **Como testar:**
  1. Acesse http://127.0.0.1:5000/shows/create
  2. Preencha o formulário:
     - **Artist:** Selecione um artista da lista
     - **Venue:** Selecione um venue da lista
     - **Start Time:** Escolha uma data futura
  3. Clique em "Create Show"
- **Resultado esperado:**
  - ✅ Show é criado com sucesso
  - ✅ Redirecionamento para página de shows
  - ✅ Novo show aparece na lista

## 👁️ Testando Visualização de Detalhes

### 1. Ver Detalhes de Venue
- **Como testar:**
  1. Acesse http://127.0.0.1:5000/venues/
  2. Clique no nome de um venue
- **Resultado esperado:**
  - ✅ Página de detalhes do venue carrega
  - ✅ Informações completas são exibidas
  - ✅ Shows futuros são listados

### 2. Ver Detalhes de Artist
- **Como testar:**
  1. Acesse http://127.0.0.1:5000/artists/
  2. Clique no nome de um artista
- **Resultado esperado:**
  - ✅ Página de detalhes do artista carrega
  - ✅ Informações completas são exibidas
  - ✅ Shows futuros são listados

## 🔧 Testando APIs

### 1. API de Estatísticas
- **URL:** http://127.0.0.1:5000/api/stats
- **Como testar:**
```bash
curl http://127.0.0.1:5000/api/stats
```
- **Resultado esperado:**
```json
{
  "venues": 3,
  "artists": 3,
  "shows": 5,
  "show_stats": {...}
}
```

### 2. API de Venues
- **URL:** http://127.0.0.1:5000/api/venues
- **Como testar:**
```bash
curl http://127.0.0.1:5000/api/venues
```
- **Resultado esperado:** Lista JSON de venues

### 3. API de Artists
- **URL:** http://127.0.0.1:5000/api/artists
- **Como testar:**
```bash
curl http://127.0.0.1:5000/api/artists
```
- **Resultado esperado:** Lista JSON de artistas

## 🐛 Testando Tratamento de Erros

### 1. Página Não Encontrada (404)
- **Como testar:**
  1. Acesse http://127.0.0.1:5000/pagina-inexistente
- **Resultado esperado:**
  - ✅ Página de erro 404 aparece
  - ✅ Link "Back" funciona corretamente

### 2. Venue Não Encontrado
- **Como testar:**
  1. Acesse http://127.0.0.1:5000/venues/999
- **Resultado esperado:**
  - ✅ Página de erro aparece
  - ✅ Mensagem de erro apropriada

## 📱 Testando Responsividade

### 1. Teste Mobile
- **Como testar:**
  1. Abra o DevTools do navegador (F12)
  2. Ative o modo responsivo
  3. Teste diferentes tamanhos de tela
- **Resultado esperado:**
  - ✅ Layout se adapta ao tamanho da tela
  - ✅ Menu funciona em dispositivos móveis

## ✅ Checklist de Funcionalidades

### Navegação
- [ ] Homepage carrega corretamente
- [ ] Menu de navegação funciona
- [ ] Links internos funcionam
- [ ] Botões de ação funcionam

### Busca
- [ ] Busca de venues funciona
- [ ] Busca de artists funciona
- [ ] Resultados são exibidos corretamente
- [ ] Busca vazia retorna mensagem apropriada

### CRUD Operations
- [ ] Criar venue funciona
- [ ] Criar artist funciona
- [ ] Criar show funciona
- [ ] Visualizar detalhes funciona
- [ ] Editar funciona (se implementado)
- [ ] Deletar funciona (se implementado)

### APIs
- [ ] API de estatísticas funciona
- [ ] API de venues funciona
- [ ] API de artists funciona
- [ ] APIs retornam JSON válido

### Tratamento de Erros
- [ ] Erro 404 é tratado
- [ ] Erro 500 é tratado
- [ ] Mensagens de erro são apropriadas
- [ ] Links de retorno funcionam

## 🚨 Problemas Conhecidos

### 1. Favicon
- **Problema:** Favicon pode não carregar
- **Status:** ✅ Resolvido - arquivo criado

### 2. Formulários WTForms
- **Problema:** Templates esperavam objetos WTForms
- **Status:** ✅ Resolvido - convertido para HTML simples

### 3. Links de Busca
- **Problema:** Links de busca não funcionavam
- **Status:** ✅ Resolvido - rotas implementadas corretamente

## 📊 Dados de Teste Disponíveis

Após executar `python scripts/seed.py`, você terá:

- **19 Genres:** Alternative, Blues, Classical, Country, Electronic, Folk, Funk, Hip-Hop, Heavy Metal, Instrumental, Jazz, Musical Theatre, Pop, Punk, R&B, Reggae, Rock n Roll, Soul, Other
- **3 Venues:** The Musical Hop, The Dueling Pianos Bar, Park Square Live Music & Coffee
- **3 Artists:** Guns N Petals, Matt Quevedo, The Wild Sax Band
- **5 Shows:** Shows passados e futuros para teste

## 🎯 Cenários de Teste Recomendados

### Cenário 1: Usuário Buscando Venue
1. Acesse a homepage
2. Clique em "Venues"
3. Busque por "Musical"
4. Verifique resultados
5. Clique em um venue para ver detalhes

### Cenário 2: Usuário Criando Show
1. Acesse "Shows"
2. Clique em "List a new show"
3. Preencha o formulário
4. Submeta o formulário
5. Verifique se o show aparece na lista

### Cenário 3: Usuário Explorando APIs
1. Teste a API de estatísticas
2. Teste a API de venues
3. Teste a API de artists
4. Verifique se os dados são consistentes

## 📝 Relatório de Testes

Após completar os testes, documente:

- ✅ Funcionalidades que funcionam corretamente
- ❌ Funcionalidades com problemas
- 🔧 Melhorias sugeridas
- 📊 Performance observada

---

**🎉 Parabéns!** Se todos os testes passaram, o projeto Fyyur está funcionando corretamente e pronto para uso!
