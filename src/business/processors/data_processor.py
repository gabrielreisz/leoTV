import pandas as pd

def process_player_matches(matches, player_nickname):
    if not matches:
        return None
        
    total_kills = 0
    total_deaths = 0
    total_assists = 0
    total_headshots = 0
    total_mvps = 0
    wins = 0
    matches_played = len(matches)
    
    for match in matches:
        stats = match.get("stats", {})
        total_kills += int(stats.get("Kills", 0))
        total_deaths += int(stats.get("Deaths", 1))
        total_assists += int(stats.get("Assists", 0))
        total_headshots += int(stats.get("Headshots", 0))
        total_mvps += int(stats.get("MVPs", 0))
        if match.get("result") == "victory":
            wins += 1
            
    return {
        "player": player_nickname,
        "matches_played": matches_played,
        "wins": wins,
        "losses": matches_played - wins,
        "win_rate": (wins / matches_played) * 100 if matches_played > 0 else 0,
        "total_kills": total_kills,
        "total_deaths": total_deaths,
        "total_assists": total_assists,
        "avg_kd": total_kills / total_deaths if total_deaths > 0 else 0,
        "avg_hs": (total_headshots / total_kills * 100) if total_kills > 0 else 0,
        "total_mvp": total_mvps
    }

def calculate_rws_leotv(player_id, match_stats_list):
    total_score = 0
    total_matches = 0

    for match_rounds_data in match_stats_list:
        if not match_rounds_data or not match_rounds_data[0].get("teams"):
            continue

        match_round_summary = match_rounds_data[0]
        player_info = None
        player_stats = None

        for team in match_round_summary.get("teams", []):
            for player in team.get("players", []):
                if player["player_id"] == player_id:
                    player_info = player
                    player_stats = player["player_stats"]
                    break
            if player_info:
                break
        
        if not player_stats:
            continue
            
        total_matches += 1

        kills = int(player_stats.get("Kills", 0))
        assists = int(player_stats.get("Assists", 0))
        damage = int(player_stats.get("Damage", 0))
        
        base_points = (kills * 5) + (assists * 3) + (damage * 0.01)

        match_result = player_info.get("match_result", "0")
        if match_result == "1":
             base_points *= 1.5

        total_score += base_points

    if total_matches > 0:
        return total_score / total_matches
    else:
        return 0

def aggregate_player_stats(rws_data):
    df = pd.DataFrame(rws_data.items(), columns=['Nickname', 'RWS-leoTV Médio'])
    df = df.sort_values(by='RWS-leoTV Médio', ascending=False).reset_index(drop=True)
    df['RWS-leoTV Médio'] = df['RWS-leoTV Médio'].round(2)
    return df