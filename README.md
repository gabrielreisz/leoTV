# 🦁 LeleoTV CS2 Stats

Uma plataforma de análise de estatísticas do CS2 construída com Python e Streamlit, originalmente criada como um projeto de estudo de Ciência da Computação e uma brincadeira entre amigos para gerar um ranking interno baseado nos dados do FACEIT.

## 🌟 Sobre o Projeto

O **LeleoTV CS2 Stats** nasceu da curiosidade em aplicar conhecimentos de programação para resolver um problema divertido: criar um sistema de ranking personalizado para um grupo de jogadores de Counter-Strike 2. O projeto utiliza a API pública do FACEIT para extrair dados de performance e apresenta-os de forma interativa através de uma interface moderna.

### Conceitos de Estudo:
* **Desenvolvimento Web com Python:** Uso do Streamlit para criar uma interface de usuário rica e interativa de maneira rápida.
* **Arquitetura em Camadas:** Implementação de uma arquitetura organizada separando responsabilidades em camadas de apresentação, negócio e dados.
* **Gerenciamento de Dados:** Utilização do SQLite para persistir informações dos jogadores e evitar chamadas repetitivas à API.
* **Sistema de Cache:** Implementação de cache inteligente para otimizar chamadas à API e melhorar performance.
* **Processamento de Dados:** Emprego da biblioteca Pandas para agregação, ordenação e visualização de estatísticas.
* **Criação de Métricas Customizadas:** Implementação da métrica **RWS (Round Win Share)** para avaliar a performance individual em partidas de maneira mais personalizada.

## 💻 Funcionalidades Principais

O aplicativo é dividido em várias seções de análise, conforme definido no menu de navegação:

* **🏠 Dashboard:** Página inicial com visão geral do sistema, métricas principais, top 5 ranking e análise rápida de jogadores com estatísticas como Win Rate, K/D, Headshot % e RWS.
* **🏆 Ranking:** Exibe uma tabela de classificação dos jogadores cadastrados, ordenada por ELO e Nível.
* **👥 Perfis:** Permite selecionar um jogador para visualizar seu ELO, Nível e estatísticas recentes, como Win Rate, K/D e Headshot %.
* **📊 Estatísticas:** Gráficos de barra e histogramas para visualizar a distribuição de ELO e Nível entre todos os jogadores.
* **📈 Análise de Desempenho:** Detalha o histórico das últimas partidas e exibe tendências de K/D Ratio e Headshots ao longo do tempo.
* **➕ Gerenciar Jogadores:** Ferramenta para adicionar ou remover jogadores da base de dados local.

## 🏗️ Arquitetura do Projeto

O projeto segue uma arquitetura em camadas bem definida:

```
leoTV/
├── app.py                          # Ponto de entrada da aplicação
├── config/
│   └── settings.py                 # Configurações e variáveis de ambiente
├── src/
│   ├── presentation/               # Camada de Apresentação
│   │   ├── components/
│   │   │   └── layout.py          # Componentes de layout e navegação
│   │   └── pages/                  # Páginas da aplicação
│   │       ├── dashboard_page.py
│   │       ├── ranking_page.py
│   │       ├── profiles_page.py
│   │       ├── statistics_page.py
│   │       ├── performance_page.py
│   │       └── manage_players_page.py
│   ├── business/                   # Camada de Negócio
│   │   ├── processors/
│   │   │   └── data_processor.py  # Processamento de dados e cálculos
│   │   └── services/               # Serviços de negócio
│   │       ├── player_service.py
│   │       ├── match_service.py
│   │       └── ranking_service.py
│   └── data/                       # Camada de Dados
│       ├── api/
│       │   └── faceit_api.py      # Integração com API FACEIT
│       ├── cache/
│       │   └── cache_manager.py   # Gerenciamento de cache
│       └── repositories/
│           └── player_repository.py # Acesso ao banco de dados
└── static/
    └── leleo.png                   # Assets estáticos
```

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Web Framework:** Streamlit (>=1.28.0)
* **Banco de Dados:** SQLite
* **API Externa:** FACEIT Open Data API
* **Análise de Dados:** Pandas (>=2.0.0)
* **Requisições HTTP:** Requests (>=2.31.0)
* **Gerenciamento de Ambiente:** python-dotenv (>=1.0.0)

## 🚀 Como Executar o Projeto

### Pré-requisitos

1. **Python** instalado (versão 3.8 ou superior recomendada).
2. Uma chave de API (Server-side) da **FACEIT Open Data API**.
   - Obtenha sua chave em: https://developers.faceit.com/

### 1. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/leoTV.git
cd leoTV
```

### 2. Crie um Ambiente Virtual (Recomendado)

```bash
python -m venv venv

# No Linux/Mac:
source venv/bin/activate

# No Windows:
venv\Scripts\activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configure a Chave de API

1. Copie o arquivo de exemplo:
```bash
cp env.example .env
```

2. Edite o arquivo `.env` e adicione sua chave de API:
```env
FACEIT_API_KEY="SUA_CHAVE_AQUI"
```

### 5. Execute a Aplicação

```bash
streamlit run app.py
```

A aplicação será aberta automaticamente no seu navegador em `http://localhost:8501`.

## 📊 Métrica RWS (Round Win Share)

O projeto implementa uma métrica customizada chamada **RWS (Round Win Share)** que mede o impacto do jogador nas vitórias da equipe.

### Fórmula:
- **Base:** `(Kills × 2.0) + (Assists × 1.0) + (Damage × 0.01)`
- **Bônus:** Multiplicado por 1.5 se a partida foi vencida

### Interpretação:
- **RWS > 20**: Desempenho excepcional
- **RWS 15-20**: Desempenho muito bom
- **RWS 10-15**: Desempenho bom
- **RWS < 10**: Desempenho abaixo da média

Quanto maior o RWS, maior o impacto do jogador nas vitórias da equipe.

## ⚙️ Configurações

As configurações principais podem ser ajustadas em `config/settings.py`:

- **Cache TTL:** Tempo de vida do cache para diferentes tipos de dados
- **Database Name:** Nome do arquivo do banco de dados SQLite
- **App Title/Icon:** Configurações de título e ícone da aplicação

## 📝 Estrutura de Dados

O banco de dados SQLite armazena informações dos jogadores incluindo:
- Nickname
- ID FACEIT
- ELO atual
- Nível FACEIT
- Avatar URL
- Data da última atualização

## 🤝 Contribuindo

Este é um projeto pessoal de estudo, mas sugestões e melhorias são sempre bem-vindas!

## 📄 Licença

Este projeto é de uso pessoal e educacional.

## 👨‍💻 Autor

Desenvolvido como projeto de estudo e diversão entre amigos.

---

**Nota:** Este projeto não é afiliado ou endossado pela FACEIT. Utilize a API respeitando os termos de uso e rate limits estabelecidos pela FACEIT.
