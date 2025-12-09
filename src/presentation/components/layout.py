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
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            color: #E8E8E8;
        }
        
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        h1 {
            color: #A78BFA !important;
            font-weight: 700;
            letter-spacing: -0.5px;
            margin-bottom: 1rem;
        }
        
        h2, h3 {
            color: #C4B5FD !important;
            font-weight: 600;
        }
        
        .stMetric {
            background: rgba(139, 92, 246, 0.1);
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: 12px;
            padding: 1rem;
            backdrop-filter: blur(10px);
        }
        
        .stMetric label {
            color: #C4B5FD !important;
            font-size: 0.85rem;
            font-weight: 500;
        }
        
        .stMetric [data-testid="stMetricValue"] {
            color: #F3E8FF !important;
            font-size: 1.8rem;
            font-weight: 700;
        }
        
        .stButton>button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.6rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        
        .stDataFrame {
            background: rgba(30, 30, 30, 0.6);
            border-radius: 12px;
            padding: 1rem;
            backdrop-filter: blur(10px);
        }
        
        .dataframe {
            background-color: rgba(30, 30, 30, 0.8) !important;
            color: #E8E8E8 !important;
            border-radius: 8px;
        }
        
        .dataframe thead th {
            background-color: rgba(139, 92, 246, 0.2) !important;
            color: #C4B5FD !important;
            font-weight: 600;
        }
        
        .dataframe tbody tr:hover {
            background-color: rgba(139, 92, 246, 0.1) !important;
        }
        
        .stSelectbox>div>div {
            background-color: rgba(30, 30, 30, 0.8);
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: 8px;
        }
        
        .stSelectbox label {
            color: #C4B5FD !important;
            font-weight: 500;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: rgba(139, 92, 246, 0.1);
            border-radius: 8px 8px 0 0;
            color: #C4B5FD;
            font-weight: 500;
        }
        
        .stTabs [aria-selected="true"] {
            background: rgba(139, 92, 246, 0.3);
            color: #F3E8FF;
        }
        
        .stInfo {
            background: rgba(59, 130, 246, 0.1);
            border-left: 4px solid #3B82F6;
            border-radius: 8px;
        }
        
        .stSuccess {
            background: rgba(34, 197, 94, 0.1);
            border-left: 4px solid #22C55E;
            border-radius: 8px;
        }
        
        .stError {
            background: rgba(239, 68, 68, 0.1);
            border-left: 4px solid #EF4444;
            border-radius: 8px;
        }
        
        .stWarning {
            background: rgba(245, 158, 11, 0.1);
            border-left: 4px solid #F59E0B;
            border-radius: 8px;
        }
        
        [data-testid="stImage"] {
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        
        hr {
            border-color: rgba(139, 92, 246, 0.2);
            margin: 2rem 0;
        }
        
        .stSpinner > div {
            border-color: #8B5CF6;
        }
        
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        }
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: #E8E8E8;
        }
        
        [data-baseweb="radio"] {
            background: rgba(139, 92, 246, 0.1);
            border-radius: 8px;
            padding: 0.5rem;
        }
        
        [data-baseweb="radio"] label {
            color: #C4B5FD !important;
        }
        
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        }
    </style>
    """, unsafe_allow_html=True)

def get_navigation_menu():
    with st.sidebar:
        st.markdown("## 🦁 LeleoTV CS2")
        st.markdown("---")
        
        page = st.radio(
            "Navegação",
            ["🏠 Dashboard", "🏆 Ranking", "👥 Perfis", "📊 Estatísticas", "📈 Análise de Desempenho", "➕ Gerenciar"],
            key="navigation"
        )
        
        st.markdown("---")
        st.markdown("### ℹ️ Sobre")
        st.caption("Plataforma de análise de estatísticas CS2 baseada em dados FACEIT")
    
    return page

