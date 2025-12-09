import streamlit as st
import pandas as pd
from ...business.services.player_service import PlayerService
from ...business.services.match_service import MatchService
from ...business.processors.data_processor import calculate_rws

def render_profiles_page(player_service: PlayerService, match_service: MatchService):
    st.title("👥 Perfis dos Jogadores")
    players = player_service.get_all_players()
    
    if players:
        selected_player = st.selectbox("Selecione um jogador", [p[0] for p in players], key="profile_select")
        if selected_player:
            player_data = next((p for p in players if p[0] == selected_player), None)
            if player_data:
                col1, col2 = st.columns([1, 2])
                with col1:
                    avatar_url = player_data[4] if player_data[4] else "https://assets.faceit.com/avatars/default_avatar.jpg"
                    st.image(avatar_url, width=200)
                    st.markdown("---")
                    st.metric("Nível FACEIT", player_data[3])
                    st.metric("ELO", player_data[2])
                
                with col2:
                    st.subheader("📊 Estatísticas Recentes")
                    matches = match_service.get_player_matches(player_data[1], limit=20)
                    if matches:
                        stats = player_service.get_player_stats(player_data[1], selected_player)
                        rws_score = calculate_rws(matches, player_data[1])
                        
                        if stats:
                            col_a, col_b, col_c, col_d = st.columns(4)
                            with col_a:
                                st.metric("Win Rate", f"{stats['win_rate']:.1f}%")
                            with col_b:
                                st.metric("K/D Ratio", f"{stats['avg_kd']:.2f}")
                            with col_c:
                                st.metric("HS %", f"{stats['avg_hs']:.1f}%")
                            with col_d:
                                st.metric("RWS", f"{rws_score:.2f}")
                            
                            st.markdown("---")
                            st.subheader("🎮 Últimas Partidas")
                            match_data = match_service.format_match_data_for_display(matches, limit=10)
                            st.dataframe(pd.DataFrame(match_data), width='stretch', hide_index=True)
                    else:
                        st.info("Nenhuma partida encontrada para este jogador.")
    else:
        st.info("Nenhum jogador cadastrado. Adicione jogadores na seção 'Gerenciar'.")

