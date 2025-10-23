import sqlite3
import os

DATABASE_NAME = "leotv_players.db"


def init_db():
    """Initializes the database by creating necessary tables."""
    # First remove existing database if it exists
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)
        
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        # Players table with additional fields
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nickname TEXT UNIQUE,
                faceit_id TEXT UNIQUE,
                elo INTEGER,
                level INTEGER,
                avatar_url TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Match history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS match_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER,
                match_id TEXT,
                map_name TEXT,
                result TEXT,
                kills INTEGER,
                deaths INTEGER,
                assists INTEGER,
                kd_ratio REAL,
                hs_percentage REAL,
                mvps INTEGER,
                match_date TIMESTAMP,
                FOREIGN KEY(player_id) REFERENCES players(id)
            )
        """)
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


def add_player(nickname, faceit_id, elo, level, avatar_url=None):
    """
    Adds a new player to the database or updates existing player information.
    
    Args:
        nickname: The player's nickname
        faceit_id: The player's FACEIT ID
        elo: Current FACEIT ELO
        level: Current FACEIT Level
        avatar_url: URL to player's avatar image
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO players (nickname, faceit_id, elo, level, avatar_url, last_updated) 
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (nickname, faceit_id, elo, level, avatar_url))
        conn.commit()
    except sqlite3.IntegrityError:
        cursor.execute("""
            UPDATE players 
            SET elo = ?, level = ?, avatar_url = ?, last_updated = CURRENT_TIMESTAMP 
            WHERE nickname = ?
        """, 
            (elo, level, nickname)
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


def get_all_players():
    """Retrieves all players from the 'players' table.

    Returns:
        list: A list of tuples: (nickname, faceit_id, elo, level).
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        # ⚠️ LINHA A SER CORRIGIDA ⚠️
        cursor.execute("SELECT nickname, faceit_id, elo, level FROM players")
        players = cursor.fetchall()
        return players
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        conn.close()

def delete_player(nickname):
    """Deletes a player from the 'players' table based on their nickname."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM players WHERE nickname=?", (nickname,))
    conn.commit()
    conn.close()