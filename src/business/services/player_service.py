from typing import Optional, Dict, List
from ...data.repositories.player_repository import PlayerRepository
from ...data.api.faceit_api import get_player_id, get_player_matches
from ..processors.data_processor import process_player_matches

class PlayerService:
    def __init__(self, player_repository: PlayerRepository):
        self.repository = player_repository
    
    def add_player(self, nickname: str) -> Dict:
        player_data = get_player_id(nickname, use_cache=True)
        
        if not player_data:
            return {
                'success': False,
                'message': f"Jogador '{nickname}' não encontrado. Verifique se o nickname está correto.",
                'player_data': None
            }
        
        success = self.repository.add_player(
            nickname=player_data["nickname"],
            faceit_id=player_data["player_id"],
            elo=player_data["elo"],
            level=player_data["level"],
            avatar_url=player_data.get("avatar_url")
        )
        
        if success:
            return {
                'success': True,
                'message': f"Jogador {nickname} adicionado com sucesso!",
                'player_data': player_data
            }
        else:
            return {
                'success': False,
                'message': f"Erro ao adicionar jogador {nickname}.",
                'player_data': None
            }
    
    def get_all_players(self) -> List[tuple]:
        return self.repository.get_all_players()
    
    def get_player_by_nickname(self, nickname: str) -> Optional[tuple]:
        return self.repository.get_player_by_nickname(nickname)
    
    def get_player_stats(self, faceit_id: str, nickname: str, limit: int = 20) -> Optional[Dict]:
        matches = get_player_matches(faceit_id, limit=limit, use_cache=True)
        
        if not matches:
            return None
        
        return process_player_matches(matches, nickname)
    
    def update_player_stats(self, nickname: str) -> bool:
        player_data = get_player_id(nickname, use_cache=False)
        
        if not player_data:
            return False
        
        return self.repository.update_player_stats(
            nickname=nickname,
            elo=player_data.get("elo"),
            level=player_data.get("level"),
            avatar_url=player_data.get("avatar_url")
        )
    
    def delete_player(self, nickname: str) -> bool:
        return self.repository.delete_player(nickname)

