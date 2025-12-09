import os
from dotenv import load_dotenv

load_dotenv()

FACEIT_API_KEY = os.environ.get("FACEIT_API_KEY")
DATABASE_NAME = "leotv_players.db"

CACHE_DEFAULT_TTL = 3600
CACHE_PLAYER_ID_TTL = 3600
CACHE_MATCH_HISTORY_TTL = 1800
CACHE_MATCH_STATS_TTL = 86400
CACHE_PLAYER_STATS_TTL = 3600

APP_TITLE = "LeleoTV CS2 Stats"
APP_ICON = "static/leleo.png"
APP_LAYOUT = "wide"

def validate_api_key():
    if not FACEIT_API_KEY or FACEIT_API_KEY == "CHAVE_DE_API_DO_PROJETO_LEOTV":
        return False
    return True

