"""
Módulo de integração com a API FACEIT.
"""
from .faceit_api import (
    get_player_id,
    get_match_history,
    get_player_matches,
    get_match_stats,
    get_player_stats,
    set_api_key
)

__all__ = [
    'get_player_id',
    'get_match_history',
    'get_player_matches',
    'get_match_stats',
    'get_player_stats',
    'set_api_key'
]

