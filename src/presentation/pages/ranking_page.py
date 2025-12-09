import streamlit as st
import pandas as pd
from ...business.services.ranking_service import RankingService

def render_ranking_page(ranking_service: RankingService):
    st.title("🏆 Ranking LeleoTV CS2")
    st.caption("Baseado na performance dos jogadores nas últimas 20 partidas")
    
    players = ranking_service.get_ranking()
    
    if players:
        df = pd.DataFrame(players, columns=['Nickname', 'ID FACEIT', 'ELO', 'Level', 'Avatar', 'Last Updated'])
        df['Posição'] = df.index + 1
        df_display = df[['Posição', 'Nickname', 'Level', 'ELO']]
        
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
                result = ranking_service.update_all_players()
                if result['success']:
                    st.success(f"Ranking atualizado com sucesso! {result['updated_count']} jogador(es) atualizado(s).")
                else:
                    st.warning(f"Nenhum jogador foi atualizado. {result['failed_count']} falha(s).")
                st.rerun()
    else:
        st.info("Nenhum jogador cadastrado. Adicione jogadores na seção 'Gerenciar Jogadores'.")

