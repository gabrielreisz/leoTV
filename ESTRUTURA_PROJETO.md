# 📁 Estrutura do Projeto LeleoTV CS2 Stats

## 🏗️ Arquitetura em Camadas

O projeto foi reorganizado seguindo o padrão de **Arquitetura em Camadas (Layered Architecture)**, separando responsabilidades e facilitando manutenção e escalabilidade.

### 📂 Estrutura de Diretórios

```
leoTV/
├── app.py                          # Entry point da aplicação
├── requirements.txt                 # Dependências do projeto
├── README.md                       # Documentação principal
├── ANALISE_E_MELHORIAS.md          # Análise e sugestões de melhorias
├── ESTRUTURA_PROJETO.md            # Este arquivo
│
├── config/                         # 🔧 Configurações
│   └── settings.py                 # Configurações centralizadas
│
├── src/                            # 📦 Código fonte principal
│   ├── presentation/               # 🎨 Camada de Apresentação
│   │   ├── pages/                  # Páginas Streamlit
│   │   │   ├── ranking_page.py
│   │   │   ├── profiles_page.py
│   │   │   ├── statistics_page.py
│   │   │   ├── manage_players_page.py
│   │   │   └── performance_page.py
│   │   └── components/             # Componentes reutilizáveis
│   │       └── layout.py          # Layout e CSS
│   │
│   ├── business/                   # 💼 Camada de Lógica de Negócio
│   │   ├── services/               # Serviços de negócio
│   │   │   ├── player_service.py
│   │   │   ├── match_service.py
│   │   │   └── ranking_service.py
│   │   └── processors/            # Processadores de dados
│   │       └── data_processor.py  # Processamento de estatísticas
│   │
│   └── data/                       # 💾 Camada de Acesso a Dados
│       ├── repositories/           # Repositórios (banco de dados)
│       │   └── player_repository.py
│       ├── api/                    # Integração com APIs externas
│       │   └── faceit_api.py
│       └── cache/                  # Sistema de cache
│           └── cache_manager.py
│
├── static/                         # 🖼️ Arquivos estáticos
│   └── leleo.png                   # Ícone da aplicação
│
└── tests/                          # 🧪 Testes (futuro)
    └── (arquivos de teste)
```

## 🎯 Camadas da Arquitetura

### 1. **Camada de Apresentação** (`src/presentation/`)
**Responsabilidade:** Interface do usuário e interação

- **Pages**: Páginas Streamlit que renderizam a UI
- **Components**: Componentes reutilizáveis (layout, CSS, etc.)

**Características:**
- Não contém lógica de negócio
- Apenas renderização e coleta de dados do usuário
- Comunica-se apenas com a camada de negócio

### 2. **Camada de Lógica de Negócio** (`src/business/`)
**Responsabilidade:** Regras de negócio e orquestração

- **Services**: Serviços que orquestram operações complexas
- **Processors**: Processamento e cálculos de métricas

**Características:**
- Contém toda a lógica de negócio
- Não conhece detalhes de implementação de UI ou banco de dados
- Coordena chamadas entre repositórios e APIs

### 3. **Camada de Acesso a Dados** (`src/data/`)
**Responsabilidade:** Persistência e integração com fontes externas

- **Repositories**: Acesso ao banco de dados SQLite
- **API**: Integração com API FACEIT
- **Cache**: Sistema de cache em memória

**Características:**
- Isolamento de detalhes de implementação
- Facilita troca de tecnologias (ex: SQLite → PostgreSQL)
- Abstração de fontes de dados

## 🔄 Fluxo de Dados

```
┌─────────────────┐
│   app.py        │  Entry point
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Presentation   │  UI (Streamlit)
│  Layer          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Business       │  Lógica de Negócio
│  Layer          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Data Layer     │  Repositórios, API, Cache
└─────────────────┘
```

## 📝 Exemplo de Fluxo: Adicionar Jogador

1. **Presentation Layer** (`manage_players_page.py`)
   - Usuário preenche formulário
   - Chama `player_service.add_player(nickname)`

2. **Business Layer** (`player_service.py`)
   - Valida dados
   - Chama API via `get_player_id()`
   - Chama repositório via `repository.add_player()`
   - Retorna resultado formatado

3. **Data Layer**
   - `faceit_api.py`: Busca dados na API FACEIT
   - `player_repository.py`: Salva no banco de dados
   - `cache_manager.py`: Armazena em cache

## ✅ Benefícios da Arquitetura em Camadas

### 1. **Separação de Responsabilidades**
- Cada camada tem uma responsabilidade clara
- Facilita manutenção e debug

### 2. **Testabilidade**
- Cada camada pode ser testada independentemente
- Facilita criação de mocks e testes unitários

### 3. **Reutilização**
- Serviços podem ser reutilizados em diferentes contextos
- Componentes de UI são reutilizáveis

### 4. **Escalabilidade**
- Fácil adicionar novas funcionalidades
- Fácil trocar implementações (ex: banco de dados)

### 5. **Manutenibilidade**
- Código organizado e fácil de encontrar
- Mudanças isoladas em suas respectivas camadas

## 🔧 Configuração

Todas as configurações estão centralizadas em `config/settings.py`:
- Chave de API FACEIT
- Configurações de cache (TTL)
- Configurações do banco de dados
- Configurações da aplicação

## 🚀 Como Executar

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
streamlit run app.py
```

## 📚 Convenções de Código

- **Nomes de arquivos**: `snake_case.py`
- **Nomes de classes**: `PascalCase`
- **Nomes de funções**: `snake_case`
- **Imports**: Absolutos a partir do diretório raiz

## 🔄 Migração do Código Antigo

Os arquivos antigos foram reorganizados:
- `db_manager.py` → `src/data/repositories/player_repository.py`
- `faceit_api.py` → `src/data/api/faceit_api.py`
- `data_processor.py` → `src/business/processors/data_processor.py`
- `cache_manager.py` → `src/data/cache/cache_manager.py`
- `app.py` → Refatorado para usar a nova estrutura

## 📈 Próximos Passos

1. Adicionar testes unitários para cada camada
2. Implementar logging estruturado
3. Adicionar tratamento de erros mais robusto
4. Implementar validação de dados
5. Adicionar documentação de API (docstrings)

