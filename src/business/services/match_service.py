from typing import List, Optional, Dict
from ...data.api.faceit_api import get_player_matches

class MatchService:
    @staticmethod
    def get_player_matches(faceit_id: str, limit: int = 20, use_cache: bool = True) -> Optional[List[Dict]]:
        return get_player_matches(faceit_id, limit=limit, use_cache=use_cache)
    
    @staticmethod
    def format_match_data_for_display(matches: List[Dict], limit: int = 5) -> List[Dict]:
        import pandas as pd
        
        match_data = []
        for match in matches[:limit]:
            match_data.append({
                "Data": pd.to_datetime(match['date']).strftime("%d/%m %H:%M"),
                "Mapa": match['map'],
                "Resultado": match['result'].title(),
                "K/D": match['stats'].get('K/D', '0'),
                "HS%": match['stats'].get('Headshots %', '0')
            })
        return match_data
    
    @staticmethod
    def format_match_history_for_display(matches: List[Dict]) -> List[Dict]:
        import pandas as pd
        
        match_history = []
        for match in matches:
            match_history.append({
                "Data": pd.to_datetime(match['date']).strftime("%d/%m %H:%M"),
                "Mapa": match['map'],
                "Resultado": match['result'].title(),
                "K/D": match['stats'].get('K/D', '0'),
                "HS%": match['stats'].get('Headshots %', '0'),
                "Kills": match['stats'].get('Kills', '0'),
                "Assists": match['stats'].get('Assists', '0'),
                "Deaths": match['stats'].get('Deaths', '0')
            })
        return match_history

