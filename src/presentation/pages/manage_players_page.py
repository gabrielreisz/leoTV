import streamlit as st
from ...business.services.player_service import PlayerService

def render_manage_players_page(player_service: PlayerService):
    st.title("➕ Gerenciar Jogadores")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("➕ Adicionar Jogador")
        with st.form("add_player_form", clear_on_submit=True):
            nickname = st.text_input("Nickname FACEIT", placeholder="Ex: leoleo", key="add_nickname")
            submitted = st.form_submit_button("Adicionar Jogador", width='stretch')
            if submitted and nickname:
                with st.spinner(f"Buscando jogador {nickname}..."):
                    result = player_service.add_player(nickname.strip())
                    if result['success']:
                        st.success(result['message'])
                        st.markdown("**Detalhes do Jogador:**")
                        st.markdown(f"- **Nível FACEIT:** {result['player_data']['level']}")
                        st.markdown(f"- **ELO:** {result['player_data']['elo']}")
                        st.rerun()
                    else:
                        st.error(result['message'])
    
    with col2:
        st.header("🗑️ Remover Jogador")
        players = player_service.get_all_players()
        if players:
            player_to_remove = st.selectbox(
                "Selecione o jogador para remover", 
                [p[0] for p in players],
                key="remove_select"
            )
            if st.button("🗑️ Remover Jogador Selecionado", width='stretch'):
                if st.session_state.get('confirm_delete', False):
                    success = player_service.delete_player(player_to_remove)
                    if success:
                        st.success(f"✅ Jogador {player_to_remove} removido com sucesso!")
                        st.session_state.confirm_delete = False
                        st.rerun()
                    else:
                        st.error(f"❌ Erro ao remover jogador {player_to_remove}.")
                else:
                    st.warning(f"⚠️ Tem certeza que deseja remover **{player_to_remove}**?")
                    col_y, col_n = st.columns(2)
                    with col_y:
                        if st.button("✓ Sim", width='stretch', key="confirm_yes"):
                            st.session_state.confirm_delete = True
                            st.rerun()
                    with col_n:
                        if st.button("✗ Não", width='stretch', key="confirm_no"):
                            st.session_state.confirm_delete = False
        else:
            st.info("Nenhum jogador cadastrado para remover.")

