import streamlit as st
import pandas as pd
from ...business.services.player_service import PlayerService
from ...business.services.match_service import MatchService
from ...business.processors.data_processor import calculate_rws

def render_performance_page(player_service: PlayerService, match_service: MatchService):
    st.title("📈 Análise de Desempenho")
    players = player_service.get_all_players()
    
    if players:
        selected_player = st.selectbox("Selecione um jogador", [p[0] for p in players], key="performance_select")
        if selected_player:
            player_data = next((p for p in players if p[0] == selected_player), None)
            if player_data:
                matches = match_service.get_player_matches(player_data[1], limit=20)
                if matches:
                    performance_data = player_service.get_player_stats(player_data[1], selected_player)
                    rws_score = calculate_rws(matches, player_data[1])
                    
                    if performance_data:
                        st.markdown("---")
                        
                        col1, col2, col3, col4, col5 = st.columns(5)
                        with col1:
                            st.metric("Vitórias", performance_data['wins'], delta=f"{performance_data['losses']} derrotas", delta_color="inverse")
                        with col2:
                            st.metric("K/D Ratio", f"{performance_data['avg_kd']:.2f}")
                        with col3:
                            st.metric("HS %", f"{performance_data['avg_hs']:.1f}%")
                        with col4:
                            st.metric("Win Rate", f"{performance_data['win_rate']:.1f}%")
                        with col5:
                            st.metric("RWS", f"{rws_score:.2f}", help="Round Win Share")
                        
                        with st.expander("ℹ️ Sobre RWS (Round Win Share)", expanded=False):
                            st.markdown("""
                            **RWS (Round Win Share)** mede o impacto do jogador nas vitórias da equipe.
                            
                            **Fórmula de Cálculo:**
                            ```
                            Base Score = (Kills × 2.0) + (Assists × 1.0) + (Damage × 0.01)
                            RWS = Base Score × 1.5 (se vitória) ou Base Score (se derrota)
                            ```
                            
                            **Interpretação:**
                            - **RWS > 20**: Desempenho excepcional, alto impacto nas vitórias
                            - **RWS 15-20**: Desempenho muito bom, contribuição significativa
                            - **RWS 10-15**: Desempenho bom, contribuição adequada
                            - **RWS < 10**: Desempenho abaixo da média, baixo impacto
                            
                            A métrica valoriza não apenas kills, mas também assists e damage, dando bônus para vitórias.
                            """)
                        
                        st.markdown("---")
                        
                        tab1, tab2, tab3 = st.tabs(["📋 Histórico de Partidas", "📊 Estatísticas Detalhadas", "📈 Tendências"])
                        
                        with tab1:
                            match_history = match_service.format_match_history_for_display(matches)
                            df_history = pd.DataFrame(match_history)
                            
                            if not df_history.empty:
                                st.dataframe(df_history, width='stretch', hide_index=True)
                                
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.markdown("#### 📍 Performance por Mapa")
                                    map_stats = df_history.groupby('Mapa').agg({
                                        'K/D': 'mean',
                                        'HS%': 'mean',
                                        'Resultado': lambda x: (x == 'Vitória').sum()
                                    }).round(2)
                                    map_stats.columns = ['K/D Médio', 'HS% Médio', 'Vitórias']
                                    st.dataframe(map_stats, width='stretch')
                                
                                with col2:
                                    st.markdown("#### 🎯 Resumo de Estatísticas")
                                    total_kills = df_history['Kills'].sum()
                                    total_deaths = df_history['Deaths'].sum()
                                    total_assists = df_history['Assists'].sum()
                                    victories = (df_history['Resultado'] == 'Vitória').sum()
                                    
                                    st.metric("Total de Kills", total_kills)
                                    st.metric("Total de Deaths", total_deaths)
                                    st.metric("Total de Assists", total_assists)
                                    st.metric("Vitórias", victories, delta=f"{victories}/{len(df_history)} partidas")
                            else:
                                st.info("Nenhum dado disponível")
                        
                        with tab2:
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown("#### 📊 Métricas Gerais")
                                st.metric("Partidas Jogadas", performance_data['matches_played'])
                                st.metric("Total de Kills", performance_data['total_kills'])
                                st.metric("Total de Deaths", performance_data['total_deaths'])
                                st.metric("Total de Assists", performance_data['total_assists'])
                                st.metric("Total de MVPs", performance_data.get('total_mvp', 0))
                            
                            with col2:
                                st.markdown("#### 🎯 Eficiência")
                                kd_efficiency = "Excelente" if performance_data['avg_kd'] > 1.2 else "Bom" if performance_data['avg_kd'] > 1.0 else "Regular"
                                hs_efficiency = "Excelente" if performance_data['avg_hs'] > 50 else "Bom" if performance_data['avg_hs'] > 40 else "Regular"
                                winrate_efficiency = "Excelente" if performance_data['win_rate'] > 60 else "Bom" if performance_data['win_rate'] > 50 else "Regular"
                                
                                st.metric("Eficiência K/D", kd_efficiency)
                                st.metric("Eficiência HS", hs_efficiency)
                                st.metric("Eficiência Win Rate", winrate_efficiency)
                                st.metric("RWS Médio", f"{rws_score:.2f}")
                        
                        with tab3:
                            st.markdown("#### 📈 Tendências de Desempenho")
                            
                            if not df_history.empty and len(df_history) > 1:
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.markdown("##### K/D Ratio ao Longo do Tempo")
                                    kd_values = df_history['K/D'].tolist()
                                    kd_df = pd.DataFrame({
                                        'Partida': range(1, len(kd_values) + 1),
                                        'K/D Ratio': kd_values
                                    })
                                    st.line_chart(kd_df.set_index('Partida'), height=300)
                                
                                with col2:
                                    st.markdown("##### Headshots % ao Longo do Tempo")
                                    hs_values = df_history['HS%'].tolist()
                                    hs_df = pd.DataFrame({
                                        'Partida': range(1, len(hs_values) + 1),
                                        'HS %': hs_values
                                    })
                                    st.line_chart(hs_df.set_index('Partida'), height=300)
                                
                                st.markdown("##### RWS por Partida")
                                rws_per_match = []
                                for match in matches:
                                    rws = calculate_rws([match], player_data[1])
                                    rws_per_match.append(rws)
                                
                                rws_df = pd.DataFrame({
                                    'Partida': range(1, len(rws_per_match) + 1),
                                    'RWS': rws_per_match
                                })
                                st.line_chart(rws_df.set_index('Partida'), height=300)
                                
                                st.markdown("##### Comparação de Métricas")
                                comparison_df = pd.DataFrame({
                                    'K/D': kd_values,
                                    'HS%': hs_values,
                                    'RWS': rws_per_match
                                })
                                st.line_chart(comparison_df, height=300)
                            else:
                                st.info("É necessário pelo menos 2 partidas para visualizar tendências")
                else:
                    st.info("Nenhuma partida encontrada para este jogador.")
    else:
        st.info("Nenhum jogador cadastrado. Adicione jogadores na seção 'Gerenciar'.")

