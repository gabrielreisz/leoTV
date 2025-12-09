from typing import List, Optional, Dict
from ...data.api.faceit_api import get_player_matches

class MatchService:
    @staticmethod
    def get_player_matches(faceit_id: str, limit: int = 20, use_cache: bool = True) -> Optional[List[Dict]]:
        return get_player_matches(faceit_id, limit=limit, use_cache=use_cache)
    
    @staticmethod
    def format_match_data_for_display(matches: List[Dict], limit: int = 5) -> List[Dict]:
        import pandas as pd
        from datetime import datetime
        
        match_data = []
        for match in matches[:limit]:
            stats = match.get('stats', {})
            kills = int(stats.get('Kills', 0) or stats.get('kills', 0))
            deaths = int(stats.get('Deaths', 0) or stats.get('deaths', 0))
            kd_ratio = round(kills / deaths, 2) if deaths > 0 else (kills if kills > 0 else 0.0)
            
            headshots = int(stats.get('Headshots', 0) or stats.get('headshots', 0))
            hs_percentage = round((headshots / kills * 100), 1) if kills > 0 else 0.0
            
            date_str = match.get('date', '')
            formatted_date = "N/A"
            if date_str:
                try:
                    date_obj = pd.to_datetime(date_str, errors='coerce')
                    if pd.notna(date_obj):
                        formatted_date = date_obj.strftime("%d/%m %H:%M")
                except:
                    try:
                        from dateutil import parser
                        date_obj = parser.parse(date_str)
                        formatted_date = date_obj.strftime("%d/%m %H:%M")
                    except:
                        formatted_date = "N/A"
            
            result = match.get('result', 'Unknown')
            if isinstance(result, str):
                result_lower = result.lower()
                if result == '1' or result_lower in ['victory', 'win', 'won']:
                    result_display = "Vitória"
                elif result == '0' or result_lower in ['defeat', 'loss', 'lost']:
                    result_display = "Derrota"
                else:
                    result_display = result.title()
            else:
                result_display = "Unknown"
            
            map_name = match.get('map', 'Unknown')
            if map_name == 'Unknown' or not map_name:
                map_name = "N/A"
            
            match_data.append({
                "Data": formatted_date,
                "Mapa": map_name,
                "Resultado": result_display,
                "K/D": f"{kd_ratio:.2f}",
                "HS%": f"{hs_percentage:.1f}%"
            })
        return match_data
    
    @staticmethod
    def format_match_history_for_display(matches: List[Dict]) -> List[Dict]:
        import pandas as pd
        from datetime import datetime
        
        match_history = []
        for match in matches:
            stats = match.get('stats', {})
            kills = int(stats.get('Kills', 0) or stats.get('kills', 0))
            deaths = int(stats.get('Deaths', 0) or stats.get('deaths', 0))
            assists = int(stats.get('Assists', 0) or stats.get('assists', 0))
            kd_ratio = round(kills / deaths, 2) if deaths > 0 else (kills if kills > 0 else 0.0)
            
            headshots = int(stats.get('Headshots', 0) or stats.get('headshots', 0))
            hs_percentage = round((headshots / kills * 100), 1) if kills > 0 else 0.0
            
            date_str = match.get('date', '')
            formatted_date = "N/A"
            if date_str:
                try:
                    date_obj = pd.to_datetime(date_str, errors='coerce')
                    if pd.notna(date_obj):
                        formatted_date = date_obj.strftime("%d/%m %H:%M")
                except:
                    try:
                        from dateutil import parser
                        date_obj = parser.parse(date_str)
                        formatted_date = date_obj.strftime("%d/%m %H:%M")
                    except:
                        formatted_date = "N/A"
            
            result = match.get('result', 'Unknown')
            if isinstance(result, str):
                result_lower = result.lower()
                if result == '1' or result_lower in ['victory', 'win', 'won']:
                    result_display = "Vitória"
                elif result == '0' or result_lower in ['defeat', 'loss', 'lost']:
                    result_display = "Derrota"
                else:
                    result_display = result.title()
            else:
                result_display = "Unknown"
            
            map_name = match.get('map', 'Unknown')
            if map_name == 'Unknown' or not map_name:
                map_name = "N/A"
            
            match_history.append({
                "Data": formatted_date,
                "Mapa": map_name,
                "Resultado": result_display,
                "K/D": kd_ratio,
                "HS%": hs_percentage,
                "Kills": kills,
                "Assists": assists,
                "Deaths": deaths
            })
        return match_history

