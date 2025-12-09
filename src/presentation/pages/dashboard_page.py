import streamlit as st
import pandas as pd
from ...business.services.player_service import PlayerService
from ...business.services.ranking_service import RankingService
from ...business.services.match_service import MatchService
from ...business.processors.data_processor import calculate_rws

def render_dashboard_page(player_service: PlayerService, ranking_service: RankingService, match_service: MatchService):
    st.title("🏠 Dashboard")
    
    players = player_service.get_all_players()
    
    if not players:
        st.info("Nenhum jogador cadastrado. Adicione jogadores na seção 'Gerenciar'.")
        return
    
    df = pd.DataFrame(players, columns=['Nickname', 'ID FACEIT', 'ELO', 'Level', 'Avatar', 'Last Updated'])
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Jogadores", len(df))
    with col2:
        st.metric("ELO Médio", f"{df['ELO'].mean():.0f}")
    with col3:
        st.metric("ELO Máximo", int(df['ELO'].max()))
    with col4:
        st.metric("ELO Mínimo", int(df['ELO'].min()))
    
    st.markdown("---")
    
    st.subheader("🏆 Top 5 Ranking")
    top5 = df.head(5)[['Nickname', 'ELO', 'Level']].copy()
    top5.index = range(1, len(top5) + 1)
    top5.index.name = "Posição"
    st.dataframe(top5, width='stretch', hide_index=False)
    
    st.markdown("---")
    
    st.subheader("📊 Visão Geral")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Distribuição de ELO")
        if len(df) > 1:
            elo_chart = df[['Nickname', 'ELO']].set_index('Nickname')
            st.bar_chart(elo_chart, height=300)
        else:
            st.info("Adicione mais jogadores para ver a distribuição")
    
    with col2:
        st.markdown("#### Distribuição de Níveis")
        level_chart = df[['Nickname', 'Level']].set_index('Nickname')
        st.bar_chart(level_chart, height=300)
    
    st.markdown("---")
    
    st.subheader("📈 Análise Rápida")
    selected_player = st.selectbox("Selecione um jogador para análise rápida", [p[0] for p in players], key="dashboard_player")
    
    if selected_player:
        player_data = next((p for p in players if p[0] == selected_player), None)
        if player_data:
            matches = match_service.get_player_matches(player_data[1], limit=20)
            if matches:
                stats = player_service.get_player_stats(player_data[1], selected_player)
                rws_score = calculate_rws(matches, player_data[1])
                
                if stats:
                    col1, col2, col3, col4, col5 = st.columns(5)
                    with col1:
                        st.metric("Win Rate", f"{stats['win_rate']:.1f}%")
                    with col2:
                        st.metric("K/D", f"{stats['avg_kd']:.2f}")
                    with col3:
                        st.metric("HS %", f"{stats['avg_hs']:.1f}%")
                    with col4:
                        st.metric("RWS", f"{rws_score:.2f}")
                    with col5:
                        st.metric("Partidas", stats['matches_played'])
                    
                    with st.expander("ℹ️ Sobre RWS (Round Win Share)", expanded=False):
                        st.markdown("""
                        **RWS (Round Win Share)** é uma métrica que mede o impacto do jogador nas vitórias da equipe.
                        
                        **Fórmula:**
                        - Base: `(Kills × 2.0) + (Assists × 1.0) + (Damage × 0.01)`
                        - Bônus: Multiplicado por 1.5 se a partida foi vencida
                        
                        **Interpretação:**
                        - **RWS > 20**: Desempenho excepcional
                        - **RWS 15-20**: Desempenho muito bom
                        - **RWS 10-15**: Desempenho bom
                        - **RWS < 10**: Desempenho abaixo da média
                        
                        Quanto maior o RWS, maior o impacto do jogador nas vitórias da equipe.
                        """)
                else:
                    st.info("Estatísticas não disponíveis para este jogador.")
            else:
                st.info("Nenhuma partida encontrada para este jogador.")


