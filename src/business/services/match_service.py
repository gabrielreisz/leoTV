from typing import List, Optional, Dict
from ...data.api.faceit_api import get_player_matches

class MatchService:
    @staticmethod
    def get_player_matches(faceit_id: str, limit: int = 20, use_cache: bool = True) -> Optional[List[Dict]]:
        return get_player_matches(faceit_id, limit=limit, use_cache=use_cache)
    
    @staticmethod
    def format_match_data_for_display(matches: List[Dict], limit: int = 5, player_id: str = None) -> List[Dict]:
        import pandas as pd
        from datetime import datetime
        from ...business.processors.data_processor import calculate_rws
        
        match_data = []
        for match in matches[:limit]:
            stats = match.get('stats', {})
            kills = int(stats.get('Kills', 0) or stats.get('kills', 0))
            deaths = int(stats.get('Deaths', 0) or stats.get('deaths', 0))
            kd_ratio = round(kills / deaths, 2) if deaths > 0 else (kills if kills > 0 else 0.0)
            
            headshots = int(stats.get('Headshots', 0) or stats.get('headshots', 0))
            hs_percentage = round((headshots / kills * 100), 1) if kills > 0 else 0.0
            
            date_value = match.get('date', '') or match.get('started_at', '') or match.get('finished_at', '')
            formatted_date = "N/A"
            
            if date_value:
                try:
                    if isinstance(date_value, (int, float)):
                        date_obj = datetime.fromtimestamp(date_value)
                        formatted_date = date_obj.strftime("%d/%m %H:%M")
                    elif isinstance(date_value, str) and date_value.strip():
                        date_str = date_value.strip()
                        date_obj = pd.to_datetime(date_str, errors='coerce', utc=True)
                        if pd.notna(date_obj):
                            if date_obj.tz is not None:
                                date_obj = date_obj.tz_convert(None)
                            formatted_date = date_obj.strftime("%d/%m %H:%M")
                        else:
                            try:
                                from dateutil import parser
                                date_obj = parser.parse(date_str)
                                if date_obj.tzinfo is not None:
                                    date_obj = date_obj.replace(tzinfo=None)
                                formatted_date = date_obj.strftime("%d/%m %H:%M")
                            except:
                                try:
                                    if 'T' in date_str:
                                        date_part = date_str.split('T')[0]
                                        time_part = date_str.split('T')[1].split('.')[0].split('Z')[0].split('+')[0]
                                        if len(time_part) == 8:
                                            date_obj = datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M:%S")
                                        elif len(time_part) == 5:
                                            date_obj = datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M")
                                        else:
                                            date_obj = datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M:%S")
                                        formatted_date = date_obj.strftime("%d/%m %H:%M")
                                except:
                                    formatted_date = "N/A"
                except Exception as e:
                    try:
                        if isinstance(date_value, str) and 'T' in date_value:
                            date_str = date_value.strip()
                            date_part = date_str.split('T')[0]
                            time_part = date_str.split('T')[1].split('.')[0].split('Z')[0].split('+')[0]
                            if len(time_part) == 8:
                                date_obj = datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M:%S")
                            elif len(time_part) == 5:
                                date_obj = datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M")
                            else:
                                date_obj = datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M:%S")
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
            if map_name == 'Unknown' or not map_name or map_name == 'N/A':
                map_name = "N/A"
            
            rws_value = 0.0
            if player_id:
                try:
                    rws_value = calculate_rws([match], player_id)
                except:
                    rws_value = 0.0
            
            match_data.append({
                "Data": formatted_date,
                "Mapa": map_name,
                "Resultado": result_display,
                "K/D": f"{kd_ratio:.2f}",
                "HS%": f"{hs_percentage:.1f}%",
                "RWS": f"{rws_value:.2f}"
            })
        return match_data
    
    @staticmethod
    def format_match_history_for_display(matches: List[Dict], player_id: str = None) -> List[Dict]:
        import pandas as pd
        from datetime import datetime
        from ...business.processors.data_processor import calculate_rws
        
        match_history = []
        for match in matches:
            stats = match.get('stats', {})
            kills = int(stats.get('Kills', 0) or stats.get('kills', 0))
            deaths = int(stats.get('Deaths', 0) or stats.get('deaths', 0))
            assists = int(stats.get('Assists', 0) or stats.get('assists', 0))
            kd_ratio = round(kills / deaths, 2) if deaths > 0 else (kills if kills > 0 else 0.0)
            
            headshots = int(stats.get('Headshots', 0) or stats.get('headshots', 0))
            hs_percentage = round((headshots / kills * 100), 1) if kills > 0 else 0.0
            
            date_value = match.get('date', '') or match.get('started_at', '') or match.get('finished_at', '')
            formatted_date = "N/A"
            
            if date_value:
                try:
                    if isinstance(date_value, (int, float)):
                        date_obj = datetime.fromtimestamp(date_value)
                        formatted_date = date_obj.strftime("%d/%m %H:%M")
                    elif isinstance(date_value, str) and date_value.strip():
                        date_str = date_value.strip()
                        date_obj = pd.to_datetime(date_str, errors='coerce', utc=True)
                        if pd.notna(date_obj):
                            if date_obj.tz is not None:
                                date_obj = date_obj.tz_convert(None)
                            formatted_date = date_obj.strftime("%d/%m %H:%M")
                        else:
                            try:
                                from dateutil import parser
                                date_obj = parser.parse(date_str)
                                if date_obj.tzinfo is not None:
                                    date_obj = date_obj.replace(tzinfo=None)
                                formatted_date = date_obj.strftime("%d/%m %H:%M")
                            except:
                                try:
                                    if 'T' in date_str:
                                        date_part = date_str.split('T')[0]
                                        time_part = date_str.split('T')[1].split('.')[0].split('Z')[0].split('+')[0]
                                        if len(time_part) == 8:
                                            date_obj = datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M:%S")
                                        elif len(time_part) == 5:
                                            date_obj = datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M")
                                        else:
                                            date_obj = datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M:%S")
                                        formatted_date = date_obj.strftime("%d/%m %H:%M")
                                except:
                                    formatted_date = "N/A"
                except Exception as e:
                    try:
                        if isinstance(date_value, str) and 'T' in date_value:
                            date_str = date_value.strip()
                            date_part = date_str.split('T')[0]
                            time_part = date_str.split('T')[1].split('.')[0].split('Z')[0].split('+')[0]
                            if len(time_part) == 8:
                                date_obj = datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M:%S")
                            elif len(time_part) == 5:
                                date_obj = datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M")
                            else:
                                date_obj = datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M:%S")
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
            if map_name == 'Unknown' or not map_name or map_name == 'N/A':
                map_name = "N/A"
            
            rws_value = 0.0
            if player_id:
                try:
                    rws_value = calculate_rws([match], player_id)
                except:
                    rws_value = 0.0
            
            match_history.append({
                "Data": formatted_date,
                "Mapa": map_name,
                "Resultado": result_display,
                "K/D": kd_ratio,
                "HS%": hs_percentage,
                "RWS": round(rws_value, 2),
                "Kills": kills,
                "Assists": assists,
                "Deaths": deaths
            })
        return match_history

