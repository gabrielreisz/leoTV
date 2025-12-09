import streamlit as st
import pandas as pd
from ...business.services.player_service import PlayerService

def render_statistics_page(player_service: PlayerService):
    st.title("📊 Estatísticas Gerais")
    players = player_service.get_all_players()
    
    if players:
        df = pd.DataFrame(players, columns=['Nickname', 'ID FACEIT', 'ELO', 'Level', 'Avatar', 'Last Updated'])
        
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
        
        tab1, tab2, tab3 = st.tabs(["📈 Gráficos", "📋 Tabela Completa", "📊 Análise"])
        
        with tab1:
            chart_type = st.selectbox(
                "Tipo de Visualização", 
                ["ELO por Jogador", "Nível por Jogador", "Distribuição de ELO", "Comparação ELO vs Nível"],
                key="chart_type"
            )
            
            if chart_type == "ELO por Jogador":
                df_sorted = df.sort_values('ELO', ascending=False)
                st.bar_chart(df_sorted.set_index('Nickname')['ELO'], height=400)
                
            elif chart_type == "Nível por Jogador":
                df_sorted = df.sort_values('Level', ascending=False)
                st.bar_chart(df_sorted.set_index('Nickname')['Level'], height=400)
                
            elif chart_type == "Distribuição de ELO":
                if len(df) > 1:
                    elo_min = int(df['ELO'].min())
                    elo_max = int(df['ELO'].max())
                    bins = min(10, len(df))
                    
                    if elo_max > elo_min:
                        elo_ranges = pd.cut(df['ELO'], bins=bins)
                        elo_dist = pd.DataFrame(elo_ranges.value_counts()).sort_index()
                        elo_dist.index = [str(interval) for interval in elo_dist.index]
                        elo_dist.columns = ['Jogadores']
                        st.bar_chart(elo_dist, height=400)
                    else:
                        st.info("Todos os jogadores têm o mesmo ELO.")
                else:
                    st.info("É necessário pelo menos 2 jogadores para visualizar a distribuição.")
            
            elif chart_type == "Comparação ELO vs Nível":
                comparison_df = df[['Nickname', 'ELO', 'Level']].set_index('Nickname')
                st.line_chart(comparison_df, height=400)
        
        with tab2:
            st.dataframe(df[['Nickname', 'ELO', 'Level']].sort_values('ELO', ascending=False), width='stretch', hide_index=True)
        
        with tab3:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 📊 Estatísticas Descritivas - ELO")
                st.dataframe(df['ELO'].describe(), width='stretch')
            with col2:
                st.markdown("#### 📊 Estatísticas Descritivas - Nível")
                st.dataframe(df['Level'].describe(), width='stretch')
    else:
        st.info("Nenhum jogador cadastrado. Adicione jogadores na seção 'Gerenciar'.")

