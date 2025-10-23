import requests
import os

# A API_KEY será carregada pelo app.py e atribuída a esta variável
API_KEY = None 

def get_player_id(nickname):
    """Fetches a player's FACEIT ID, ELO, and Level given their nickname.
    
    CORREÇÃO: O parâmetro 'game=cs2' foi removido para evitar o erro 400.
    
    Args:
        nickname (str): The nickname of the player.

    Returns:
        dict: Contendo nickname, player_id, elo e level, ou None.
    """
    if not API_KEY:
        print("Erro de API: A chave não foi carregada.")
        return None
        
    url = "https://open.faceit.com/data/v4/players"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    # Parâmetro corrigido: SÓ o nickname
    params = {"nickname": nickname} 
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extrai Level e ELO de CS2 (pode falhar se o jogador nunca jogou CS2)
        cs2_data = data.get("games", {}).get("cs2", {})
        elo = cs2_data.get("faceit_elo", 0)
        level = cs2_data.get("skill_level", 0)
        
        return {
            "nickname": nickname, 
            "player_id": data["player_id"],
            "elo": elo,
            "level": level,
            "avatar_url": data.get("avatar") # Novo dado para o resumo visual
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching player ID for {nickname}: {e}")
        return None


def get_match_history(player_id, limit=20):
    """
    Fetches match history for a player.
    """
    if not API_KEY:
        return None
        
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
        return response.json().get("items", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching match history: {e}")
        return None

def get_player_matches(player_id, limit=20):
    """
    Fetches detailed match information for a player.
    """
    matches = get_match_history(player_id, limit)
    if not matches:
        return None
        
    detailed_matches = []
    for match in matches:
        match_id = match.get("match_id")
        match_stats = get_match_stats(match_id)
        
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

def get_match_stats(match_id):
    """
    Fetches detailed statistics for a specific match.
    """
    if not API_KEY:
        return None
        
    url = f"https://open.faceit.com/data/v4/matches/{match_id}/stats"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("rounds", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching match stats: {e}")
        return None

def get_player_stats(player_id):
    """
    Fetches lifetime statistics for a player in CS2.
    """
    if not API_KEY:
        return None
        
    url = f"https://open.faceit.com/data/v4/players/{player_id}/stats/cs2"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching player stats: {e}")
        return None
    """Retrieves the most recent CS2 matches for a given player ID."""
    if not API_KEY: return None
    url = f"https://open.faceit.com/data/v4/players/{player_id}/history?game=cs2&offset=0&limit={limit}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["items"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching match history for player {player_id}: {e}")
        return None


def get_match_stats(match_id):
    """Retrieves detailed statistics for a specific match (resumo da partida)."""
    if not API_KEY: return None
    url = f"https://open.faceit.com/data/v4/matches/{match_id}/stats"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        # Retorna o resumo da partida (que está no índice [0] da lista 'rounds')
        return data.get("rounds")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching match stats for match {match_id}: {e}")
        return None