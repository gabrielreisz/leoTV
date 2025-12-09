import requests
import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(root_dir))

from src.data.cache.cache_manager import get_cache
from config.settings import (
    CACHE_PLAYER_ID_TTL,
    CACHE_MATCH_HISTORY_TTL,
    CACHE_MATCH_STATS_TTL,
    CACHE_PLAYER_STATS_TTL
)

API_KEY = None
cache = get_cache(ttl_seconds=3600)

def set_api_key(api_key: str):
    global API_KEY
    API_KEY = api_key 

def get_player_id(nickname, use_cache=True):
    if not API_KEY:
        print("Erro de API: A chave não foi carregada.")
        return None
    
    if use_cache:
        cached_data = cache.get("player_id", nickname.lower())
        if cached_data is not None:
            return cached_data
        
    url = "https://open.faceit.com/data/v4/players"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {"nickname": nickname} 
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        cs2_data = data.get("games", {}).get("cs2", {})
        elo = cs2_data.get("faceit_elo", 0)
        level = cs2_data.get("skill_level", 0)
        
        result = {
            "nickname": nickname, 
            "player_id": data["player_id"],
            "elo": elo,
            "level": level,
            "avatar_url": data.get("avatar")
        }
        
        if use_cache:
            cache.set("player_id", nickname.lower(), result, ttl_seconds=CACHE_PLAYER_ID_TTL)
        
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error fetching player ID for {nickname}: {e}")
        return None

def get_match_history(player_id, limit=20, use_cache=True):
    if not API_KEY:
        return None
    
    cache_key = f"{player_id}_{limit}"
    if use_cache:
        cached_data = cache.get("match_history", cache_key)
        if cached_data is not None:
            return cached_data
        
    url = f"https://open.faceit.com/data/v4/players/{player_id}/history"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {
        "game": "cs2",
        "offset": "0",
        "limit": str(limit)
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json().get("items", [])
        
        if use_cache:
            cache.set("match_history", cache_key, data, ttl_seconds=CACHE_MATCH_HISTORY_TTL)
        
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching match history: {e}")
        return None

def get_player_matches(player_id, limit=20, use_cache=True):
    matches = get_match_history(player_id, limit, use_cache)
    if not matches:
        return None
        
    detailed_matches = []
    for match in matches:
        match_id = match.get("match_id")
        match_stats = get_match_stats(match_id, use_cache)
        
        if match_stats:
            player_stats = None
            for team in match_stats[0].get("teams", []):
                for player in team.get("players", []):
                    if player["player_id"] == player_id:
                        player_stats = player.get("player_stats", {})
                        break
                if player_stats:
                    break
            
            if player_stats:
                detailed_matches.append({
                    "match_id": match_id,
                    "map": match.get("map", {}).get("name", "Unknown"),
                    "date": match.get("started_at", "Unknown"),
                    "result": match.get("result", "Unknown"),
                    "score": match.get("score", "Unknown"),
                    "stats": player_stats,
                })
                
    return detailed_matches

def get_match_stats(match_id, use_cache=True):
    if not API_KEY:
        return None
    
    if use_cache:
        cached_data = cache.get("match_stats", match_id)
        if cached_data is not None:
            return cached_data
        
    url = f"https://open.faceit.com/data/v4/matches/{match_id}/stats"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        result = data.get("rounds", [])
        
        if use_cache:
            cache.set("match_stats", match_id, result, ttl_seconds=CACHE_MATCH_STATS_TTL)
        
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error fetching match stats for match {match_id}: {e}")
        return None

def get_player_stats(player_id, use_cache=True):
    if not API_KEY:
        return None
    
    if use_cache:
        cached_data = cache.get("player_stats", player_id)
        if cached_data is not None:
            return cached_data
        
    url = f"https://open.faceit.com/data/v4/players/{player_id}/stats/cs2"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if use_cache:
            cache.set("player_stats", player_id, data, ttl_seconds=CACHE_PLAYER_STATS_TTL)
        
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching player stats: {e}")
        return None