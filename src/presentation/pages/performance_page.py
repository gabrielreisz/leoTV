import streamlit as st
import pandas as pd
from ...business.services.player_service import PlayerService
from ...business.services.match_service import MatchService

def render_performance_page(player_service: PlayerService, match_service: MatchService):
    st.title("📈 Análise de Desempenho")
    players = player_service.get_all_players()
    
    if players:
        selected_player = st.selectbox("Selecione um jogador", [p[0] for p in players])
        if selected_player:
            player_data = next((p for p in players if p[0] == selected_player), None)
            if player_data:
                matches = match_service.get_player_matches(player_data[1], limit=20)
                if matches:
                    st.subheader("Últimas 20 Partidas")
                    performance_data = player_service.get_player_stats(player_data[1], selected_player)
                    
                    if performance_data:
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
                        match_history = match_service.format_match_history_for_display(matches)
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
                else:
                    st.info("Nenhuma partida encontrada para este jogador.")
    else:
        st.info("Nenhum jogador cadastrado. Adicione jogadores na seção 'Gerenciar Jogadores'.")

