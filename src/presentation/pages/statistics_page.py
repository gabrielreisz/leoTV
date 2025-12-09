import streamlit as st
import pandas as pd
from ...business.services.player_service import PlayerService

def render_statistics_page(player_service: PlayerService):
    st.title("📊 Estatísticas Gerais")
    players = player_service.get_all_players()
    
    if players:
        chart_type = st.selectbox(
            "Tipo de Visualização", 
            ["ELO por Jogador", "Nível por Jogador", "Distribuição de ELO"]
        )
        
        df = pd.DataFrame(players, columns=['Nickname', 'ID FACEIT', 'ELO', 'Level', 'Avatar', 'Last Updated'])
        
        if chart_type == "ELO por Jogador":
            df_sorted = df.sort_values('ELO', ascending=False)
            st.bar_chart(df_sorted.set_index('Nickname')['ELO'])
            
        elif chart_type == "Nível por Jogador":
            df_sorted = df.sort_values('Level', ascending=False)
            st.bar_chart(df_sorted.set_index('Nickname')['Level'])
            
        elif chart_type == "Distribuição de ELO":
            elo_min = df['ELO'].min()
            elo_max = df['ELO'].max()
            bins = 10
            elo_ranges = pd.cut(df['ELO'], bins=bins)
            elo_dist = pd.DataFrame(elo_ranges.value_counts()).sort_index()
            elo_dist.columns = ['Jogadores']
            st.bar_chart(elo_dist)
    else:
        st.info("Nenhum jogador cadastrado. Adicione jogadores na seção 'Gerenciar Jogadores'.")

