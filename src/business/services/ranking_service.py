from typing import List, Dict
from ...data.repositories.player_repository import PlayerRepository
from ...data.api.faceit_api import get_player_id
from ...data.cache.cache_manager import get_cache

class RankingService:
    def __init__(self, player_repository: PlayerRepository):
        self.repository = player_repository
    
    def get_ranking(self) -> List[tuple]:
        return self.repository.get_all_players()
    
    def update_all_players(self) -> Dict:
        players = self.repository.get_all_players()
        updated_count = 0
        failed_count = 0
        cache = get_cache()
        
        for player in players:
            nickname, faceit_id = player[0], player[1]
            player_data = get_player_id(nickname, use_cache=False)
            
            if player_data:
                success = self.repository.update_player_stats(
                    nickname=nickname,
                    elo=player_data.get("elo"),
                    level=player_data.get("level"),
                    avatar_url=player_data.get("avatar_url")
                )
                
                if success:
                    updated_count += 1
                    cache.invalidate("match_history", f"{faceit_id}_20")
                else:
                    failed_count += 1
            else:
                failed_count += 1
        
        return {
            'success': updated_count > 0,
            'updated_count': updated_count,
            'failed_count': failed_count
        }

