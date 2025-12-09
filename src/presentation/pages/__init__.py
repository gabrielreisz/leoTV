"""
Páginas da aplicação Streamlit.
"""
from .ranking_page import render_ranking_page
from .profiles_page import render_profiles_page
from .statistics_page import render_statistics_page
from .manage_players_page import render_manage_players_page
from .performance_page import render_performance_page

__all__ = [
    'render_ranking_page',
    'render_profiles_page',
    'render_statistics_page',
    'render_manage_players_page',
    'render_performance_page'
]

