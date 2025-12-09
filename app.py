import streamlit as st
import sys
from pathlib import Path

root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from config.settings import FACEIT_API_KEY, validate_api_key
from src.data.api.faceit_api import set_api_key
from src.data.repositories.player_repository import PlayerRepository
from src.business.services.player_service import PlayerService
from src.business.services.match_service import MatchService
from src.business.services.ranking_service import RankingService
from src.presentation.components.layout import setup_page_config, apply_custom_css, get_navigation_menu
from src.presentation.pages import (
    render_ranking_page,
    render_profiles_page,
    render_statistics_page,
    render_manage_players_page,
    render_performance_page
)

if not validate_api_key():
    st.error("""
        **ERRO DE CONFIGURAÇÃO:** A chave de API da FACEIT não foi encontrada ou é o placeholder.
        1. **Crie/edite o arquivo `.env`** na raiz do projeto.
        2. **Adicione sua chave real Server-side** no formato: `FACEIT_API_KEY="SUA_CHAVE_AQUI"`
    """)
    st.stop()

set_api_key(FACEIT_API_KEY)

player_repository = PlayerRepository()
player_service = PlayerService(player_repository)
match_service = MatchService()
ranking_service = RankingService(player_repository)

setup_page_config()
apply_custom_css()

menu = get_navigation_menu()

if menu == "🏆 Ranking":
    render_ranking_page(ranking_service)
elif menu == "👥 Perfis":
    render_profiles_page(player_service, match_service)
elif menu == "📊 Estatísticas":
    render_statistics_page(player_service)
elif menu == "➕ Gerenciar Jogadores":
    render_manage_players_page(player_service)
elif menu == "📈 Análise de Desempenho":
    render_performance_page(player_service, match_service)
