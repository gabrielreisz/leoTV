import streamlit as st
import faceit_api
import data_processor
import db_manager
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

# --- Load environment variables ---
load_dotenv() 
API_KEY = os.environ.get("FACEIT_API_KEY")

# --- API Key verification ---
if not API_KEY or API_KEY == "CHAVE_DE_API_DO_PROJETO_LEOTV":
    st.error("""
        **ERRO DE CONFIGURAÇÃO:** A chave de API da FACEIT não foi encontrada ou é o placeholder.
        1. **Crie/edite o arquivo `.env`** na raiz do projeto.
        2. **Adicione sua chave real Server-side** no formato: `FACEIT_API_KEY="SUA_CHAVE_AQUI"`
    """)
    st.stop()

# --- Initialize API and Database ---
faceit_api.API_KEY = API_KEY
db_manager.init_db()

# --- Streamlit App Config ---
st.set_page_config(
    page_title="LeleoTV CS2 Stats",
    page_icon="leleo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for dark purple theme ---
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

# --- Navigation Menu ---
menu = st.selectbox(
    "Navegação",
    ["🏆 Ranking", "👥 Perfis", "📊 Estatísticas", "➕ Gerenciar Jogadores", "📈 Análise de Desempenho"],
    key="navigation",
    label_visibility="collapsed")


# --- Main Content ---
if menu == "🏆 Ranking":
    st.title("🏆 Ranking LeleoTV CS2")
    st.caption("Baseado na performance dos jogadores nas últimas 20 partidas")
    
    players = db_manager.get_all_players()
    if players:
        df = pd.DataFrame(players, columns=['Nickname', 'ID FACEIT', 'ELO', 'Level', 'Avatar', 'Last Updated'])
        df['Posição'] = df.index + 1
        df_display = df[['Posição', 'Nickname', 'Level', 'ELO']]
        
        # Top 3 Players
        col1, col2, col3 = st.columns(3)
        with col2:
            if len(df) >= 1:
                st.markdown("### 🥇 " + df.iloc[0]['Nickname'])
                st.metric("ELO", df.iloc[0]['ELO'])
        with col1:
            if len(df) >= 2:
                st.markdown("### 🥈 " + df.iloc[1]['Nickname'])
                st.metric("ELO", df.iloc[1]['ELO'])
        with col3:
            if len(df) >= 3:
                st.markdown("### 🥉 " + df.iloc[2]['Nickname'])
                st.metric("ELO", df.iloc[2]['ELO'])
        
        st.markdown("---")
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        if st.button("🚀 Atualizar Ranking", use_container_width=True):
            with st.spinner("Atualizando ranking..."):
                for player in players:
                    nickname, faceit_id = player[0], player[1]
                    matches = faceit_api.get_player_matches(faceit_id)
                    if matches:
                        stats = data_processor.process_player_matches(matches, nickname)
                        db_manager.update_player_stats(nickname)
                st.success("Ranking atualizado com sucesso!")
                st.experimental_rerun()

elif menu == "👥 Perfis":
    st.title("👥 Perfis dos Jogadores")
    players = db_manager.get_all_players()
    
    if players:
        selected_player = st.selectbox("Selecione um jogador", [p[0] for p in players])
        if selected_player:
            player_data = next((p for p in players if p[0] == selected_player), None)
            if player_data:
                col1, col2 = st.columns([1, 2])
                with col1:
                    avatar_url = player_data[4] if player_data[4] else "https://assets.faceit.com/avatars/default_avatar.jpg"
                    st.image(avatar_url, width=200)
                    st.metric("Nível FACEIT", player_data[3])
                    st.metric("ELO", player_data[2])
                
                with col2:
                    st.subheader("Estatísticas Recentes")
                    matches = faceit_api.get_player_matches(player_data[1])
                    if matches:
                        stats = data_processor.process_player_matches(matches, selected_player)
                        
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("Win Rate", f"{stats['win_rate']:.1f}%")
                        with col_b:
                            st.metric("K/D Ratio", f"{stats['avg_kd']:.2f}")
                        with col_c:
                            st.metric("HS %", f"{stats['avg_hs']:.1f}%")
                        
                        st.subheader("Últimas Partidas")
                        match_data = []
                        for match in matches[:5]:
                            match_data.append({
                                "Data": pd.to_datetime(match['date']).strftime("%d/%m %H:%M"),
                                "Mapa": match['map'],
                                "Resultado": match['result'].title(),
                                "K/D": match['stats'].get('K/D', '0'),
                                "HS%": match['stats'].get('Headshots %', '0')
                            })
                        st.dataframe(pd.DataFrame(match_data), use_container_width=True)

elif menu == "📊 Estatísticas":
    st.title("📊 Estatísticas Gerais")
    players = db_manager.get_all_players()
    if players:
        chart_type = st.selectbox(
            "Tipo de Visualização", 
            ["ELO por Jogador", "Nível por Jogador", "Distribuição de ELO"]
        )
        
        df = pd.DataFrame(players, columns=['Nickname', 'ID FACEIT', 'ELO', 'Level', 'Avatar', 'Last Updated'])
        
        if chart_type == "ELO por Jogador":
            # Sort by ELO descending
            df_sorted = df.sort_values('ELO', ascending=False)
            st.bar_chart(df_sorted.set_index('Nickname')['ELO'])
            
        elif chart_type == "Nível por Jogador":
            # Sort by Level descending
            df_sorted = df.sort_values('Level', ascending=False)
            st.bar_chart(df_sorted.set_index('Nickname')['Level'])
            
        elif chart_type == "Distribuição de ELO":
            # Create ELO ranges for histogram
            elo_min = df['ELO'].min()
            elo_max = df['ELO'].max()
            bins = 10
            elo_ranges = pd.cut(df['ELO'], bins=bins)
            elo_dist = pd.DataFrame(elo_ranges.value_counts()).sort_index()
            elo_dist.columns = ['Jogadores']
            st.bar_chart(elo_dist)

elif menu == "➕ Gerenciar Jogadores":
    st.title("➕ Gerenciar Jogadores")
    
    # Create columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Adicionar Jogador")
        with st.form("add_player_form", clear_on_submit=True):
            nickname = st.text_input("Nickname FACEIT", placeholder="Ex: leoleo")
            submitted = st.form_submit_button("Adicionar Jogador", use_container_width=True)
            if submitted and nickname:
                with st.spinner(f"Buscando jogador {nickname}..."):
                    player_data = faceit_api.get_player_id(nickname)
                    if player_data:
                        db_manager.add_player(
                            nickname=player_data["nickname"],
                            faceit_id=player_data["player_id"],
                            elo=player_data["elo"],
                            level=player_data["level"],
                            avatar_url=player_data.get("avatar_url")
                        )
                        st.success(f"Jogador {nickname} adicionado com sucesso!")
                        st.write("**Detalhes do Jogador:**")
                        st.write(f"- Nível FACEIT: {player_data['level']}")
                        st.write(f"- ELO: {player_data['elo']}")
                    else:
                        st.error(f"Jogador '{nickname}' não encontrado. Verifique se o nickname está correto.")
    
    with col2:
        st.header("Remover Jogador")
        players = db_manager.get_all_players()
        if players:
            player_to_remove = st.selectbox(
                "Selecione o jogador para remover", 
                [p[0] for p in players]
            )
            if st.button("🗑️ Remover Jogador Selecionado", use_container_width=True):
                if st.session_state.get('confirm_delete', False):
                    db_manager.delete_player(player_to_remove)
                    st.success(f"Jogador {player_to_remove} removido com sucesso!")
                    st.session_state.confirm_delete = False
                    st.experimental_rerun()
                else:
                    st.warning(f"Tem certeza que deseja remover {player_to_remove}?")
                    col_y, col_n = st.columns(2)
                    with col_y:
                        if st.button("✓ Sim", use_container_width=True):
                            st.session_state.confirm_delete = True
                            st.experimental_rerun()
                    with col_n:
                        if st.button("✗ Não", use_container_width=True):
                            st.session_state.confirm_delete = False
        else:
            st.info("Nenhum jogador cadastrado para remover.")
    
elif menu == "📈 Análise de Desempenho":
    st.title("📈 Análise de Desempenho")
    players = db_manager.get_all_players()
    if players:
        selected_player = st.selectbox("Selecione um jogador", [p[0] for p in players])
        if selected_player:
            player_data = next((p for p in players if p[0] == selected_player), None)
            if player_data:
                matches = faceit_api.get_player_matches(player_data[1])
                if matches:
                    st.subheader("Últimas 20 Partidas")
                    performance_data = data_processor.process_player_matches(matches, selected_player)
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Vitórias", performance_data['wins'])
                    with col2:
                        st.metric("K/D Ratio", f"{performance_data['avg_kd']:.2f}")
                    with col3:
                        st.metric("HS %", f"{performance_data['avg_hs']:.1f}%")
                    with col4:
                        st.metric("Win Rate", f"{performance_data['win_rate']:.1f}%")
                    
                    st.subheader("Histórico de Partidas")
                    match_history = []
                    for match in matches:
                        match_history.append({
                            "Data": pd.to_datetime(match['date']).strftime("%d/%m %H:%M"),
                            "Mapa": match['map'],
                            "Resultado": match['result'].title(),
                            "K/D": match['stats'].get('K/D', '0'),
                            "HS%": match['stats'].get('Headshots %', '0'),
                            "Kills": match['stats'].get('Kills', '0'),
                            "Assists": match['stats'].get('Assists', '0'),
                            "Deaths": match['stats'].get('Deaths', '0')
                        })
                    
                    df_history = pd.DataFrame(match_history)
                    st.dataframe(df_history, use_container_width=True)
                    
                    st.subheader("Tendências de Desempenho")
                    tab1, tab2 = st.tabs(["K/D Ratio", "Headshots"])
                    
                    with tab1:
                        kd_data = pd.to_numeric(df_history['K/D'], errors='coerce')
                        st.line_chart(kd_data)
                    
                    with tab2:
                        hs_data = pd.to_numeric(df_history['HS%'].str.rstrip('%'), errors='coerce')
                        st.line_chart(hs_data)