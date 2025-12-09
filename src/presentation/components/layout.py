import streamlit as st
import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(root_dir))

from config.settings import APP_TITLE, APP_ICON, APP_LAYOUT

def setup_page_config():
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout=APP_LAYOUT,
        initial_sidebar_state="expanded"
    )

def apply_custom_css():
    st.markdown("""
    <style>
        .stApp {
            background-color: #0A0A0A;
            color: #E0E0E0;
        }
        .css-1d391kg {
            background-color: #1E1E1E;
        }
        .stButton>button {
            background-color: #6B46C1;
            color: white;
            border: none;
        }
        .stButton>button:hover {
            background-color: #805AD5;
        }
        h1, h2, h3 {
            color: #9F7AEA !important;
        }
        .dataframe {
            background-color: #1E1E1E;
            color: #E0E0E0;
        }
        .stSelectbox>div>div {
            background-color: #1E1E1E;
        }
    </style>
    """, unsafe_allow_html=True)

def get_navigation_menu():
    return st.selectbox(
        "Navegação",
        ["🏆 Ranking", "👥 Perfis", "📊 Estatísticas", "➕ Gerenciar Jogadores", "📈 Análise de Desempenho"],
        key="navigation",
        label_visibility="collapsed"
    )

