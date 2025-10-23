# 🦁 LeleoTV CS2 Stats

Uma plataforma de análise de estatísticas do CS2 construída com Python e Streamlit, originalmente criada como um projeto de estudo de Ciência da Computação e uma brincadeira entre amigos para gerar um ranking interno baseado nos dados do FACEIT.

## 🌟 Sobre o Projeto

O **LeleoTV CS2 Stats** nasceu da curiosidade em aplicar conhecimentos de programação para resolver um problema divertido: criar um sistema de ranking personalizado para um grupo de jogadores de Counter-Strike 2. O projeto utiliza a API pública do FACEIT para extrair dados de performance e apresenta-os de forma interativa através de uma interface moderna.

### Conceitos de Estudo:
* **Desenvolvimento Web com Python:** Uso do Streamlit para criar uma interface de usuário rica e interativa de maneira rápida.
* **Gerenciamento de Dados:** Utilização do SQLite para persistir informações dos jogadores e evitar chamadas repetitivas à API.
* **Processamento de Dados:** Emprego da biblioteca Pandas para agregação, ordenação e visualização de estatísticas.
* **Criação de Métricas Customizadas:** Implementação da métrica **RWS-leoTV** para avaliar a performance individual em partidas de maneira mais personalizada.

## 💻 Funcionalidades Principais

O aplicativo é dividido em várias seções de análise, conforme definido no menu de navegação do `app.py`:

* **🏆 Ranking:** Exibe uma tabela de classificação dos jogadores cadastrados, ordenada por ELO e Nível.
* **👥 Perfis:** Permite selecionar um jogador para visualizar seu ELO, Nível e estatísticas recentes, como Win Rate, K/D e Headshot %.
* **📊 Estatísticas:** Gráficos de barra e histogramas para visualizar a distribuição de ELO e Nível entre todos os jogadores.
* **➕ Gerenciar Jogadores:** Ferramenta para adicionar ou remover jogadores da base de dados local.
* **📈 Análise de Desempenho:** Detalha o histórico das últimas partidas e exibe tendências de K/D Ratio e Headshots ao longo do tempo.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Web Framework:** Streamlit
* **Banco de Dados:** SQLite (`db_manager.py`)
* **API:** FACEIT Data API (`faceit_api.py`)
* **Análise:** Pandas

## 🚀 Como Executar o Projeto

### Pré-requisitos

1.  **Python** instalado (versão 3.x recomendada).
2.  Uma chave de API (Server-side) da **FACEIT Open Data API**.

### 1. Instalação de Dependências

Certifique-se de que todas as bibliotecas Python necessárias estejam instaladas.

```bash
# Você pode precisar criar um arquivo requirements.txt com as dependências
# (streamlit, pandas, requests, python-dotenv, sqlite3)
pip install streamlit pandas requests python-dotenv