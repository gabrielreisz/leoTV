import streamlit as st
import pandas as pd
from ...business.services.ranking_service import RankingService

def render_ranking_page(ranking_service: RankingService):
    st.title("🏆 Ranking LeleoTV CS2")
    st.caption("Classificação baseada no ELO dos jogadores")
    
    players = ranking_service.get_ranking()
    
    if players:
        df = pd.DataFrame(players, columns=['Nickname', 'ID FACEIT', 'ELO', 'Level', 'Avatar', 'Last Updated'])
        df['Posição'] = df.index + 1
        df_display = df[['Posição', 'Nickname', 'Level', 'ELO']].copy()
        
        if len(df) >= 3:
            col1, col2, col3 = st.columns([1, 1.2, 1])
            with col1:
                st.markdown(f"""
                <div style='text-align: center; padding: 1.5rem; background: rgba(139, 92, 246, 0.15); 
                border-radius: 16px; border: 2px solid rgba(139, 92, 246, 0.3);'>
                    <h3 style='color: #C4B5FD; margin: 0.5rem 0;'>🥈</h3>
                    <h4 style='color: #F3E8FF; margin: 0.5rem 0;'>{df.iloc[1]['Nickname']}</h4>
                    <p style='color: #A78BFA; font-size: 1.2rem; font-weight: 700; margin: 0;'>{df.iloc[1]['ELO']}</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(139, 92, 246, 0.3), rgba(102, 126, 234, 0.3)); 
                border-radius: 20px; border: 3px solid rgba(139, 92, 246, 0.5);'>
                    <h2 style='color: #F3E8FF; margin: 0.5rem 0; font-size: 3rem;'>🥇</h2>
                    <h3 style='color: #F3E8FF; margin: 0.5rem 0;'>{df.iloc[0]['Nickname']}</h3>
                    <p style='color: #F3E8FF; font-size: 1.5rem; font-weight: 700; margin: 0;'>{df.iloc[0]['ELO']}</p>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div style='text-align: center; padding: 1.5rem; background: rgba(139, 92, 246, 0.15); 
                border-radius: 16px; border: 2px solid rgba(139, 92, 246, 0.3);'>
                    <h3 style='color: #C4B5FD; margin: 0.5rem 0;'>🥉</h3>
                    <h4 style='color: #F3E8FF; margin: 0.5rem 0;'>{df.iloc[2]['Nickname']}</h4>
                    <p style='color: #A78BFA; font-size: 1.2rem; font-weight: 700; margin: 0;'>{df.iloc[2]['ELO']}</p>
                </div>
                """, unsafe_allow_html=True)
        elif len(df) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 🥇 " + df.iloc[0]['Nickname'])
                st.metric("ELO", df.iloc[0]['ELO'])
            with col2:
                st.markdown("### 🥈 " + df.iloc[1]['Nickname'])
                st.metric("ELO", df.iloc[1]['ELO'])
        elif len(df) >= 1:
            st.markdown("### 🥇 " + df.iloc[0]['Nickname'])
            st.metric("ELO", df.iloc[0]['ELO'])
        
        st.markdown("---")
        st.subheader("📋 Classificação Completa")
        st.dataframe(df_display, width='stretch', hide_index=True)
        
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            if st.button("🔄 Atualizar Ranking", width='stretch'):
                with st.spinner("Atualizando ranking..."):
                    result = ranking_service.update_all_players()
                    if result['success']:
                        st.success(f"✅ {result['updated_count']} jogador(es) atualizado(s)")
                    else:
                        st.warning(f"⚠️ {result['failed_count']} falha(s)")
                    st.rerun()
    else:
        st.info("Nenhum jogador cadastrado. Adicione jogadores na seção 'Gerenciar'.")

