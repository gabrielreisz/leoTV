import sqlite3
import sys
from pathlib import Path
from typing import List, Tuple, Optional

root_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(root_dir))

from config.settings import DATABASE_NAME

class PlayerRepository:
    def __init__(self, db_name: str = DATABASE_NAME):
        self.db_name = db_name
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
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
    
    def add_player(self, nickname: str, faceit_id: str, elo: int, level: int, avatar_url: Optional[str] = None) -> bool:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO players (nickname, faceit_id, elo, level, avatar_url, last_updated) 
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (nickname, faceit_id, elo, level, avatar_url))
            conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            existing_player = cursor.execute("""
                SELECT faceit_id FROM players WHERE nickname = ? OR faceit_id = ?
            """, (nickname, faceit_id)).fetchone()
            
            if existing_player:
                cursor.execute("""
                    UPDATE players 
                    SET elo = ?, level = ?, avatar_url = ?, last_updated = CURRENT_TIMESTAMP 
                    WHERE nickname = ? OR faceit_id = ?
                """, (elo, level, avatar_url, nickname, faceit_id))
                conn.commit()
                return True
            return False
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        finally:
            conn.close()
    
    def get_all_players(self) -> List[Tuple]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT nickname, faceit_id, elo, level, avatar_url, last_updated 
                FROM players 
                ORDER BY elo DESC
            """)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            conn.close()
    
    def get_player_by_nickname(self, nickname: str) -> Optional[Tuple]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT nickname, faceit_id, elo, level, avatar_url, last_updated 
                FROM players 
                WHERE nickname = ?
            """, (nickname,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            conn.close()
    
    def update_player_stats(self, nickname: str, elo: Optional[int] = None, 
                           level: Optional[int] = None, avatar_url: Optional[str] = None) -> bool:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            updates = []
            params = []
            
            if elo is not None:
                updates.append("elo = ?")
                params.append(elo)
            if level is not None:
                updates.append("level = ?")
                params.append(level)
            if avatar_url is not None:
                updates.append("avatar_url = ?")
                params.append(avatar_url)
            
            if updates:
                updates.append("last_updated = CURRENT_TIMESTAMP")
                params.append(nickname)
                
                query = f"UPDATE players SET {', '.join(updates)} WHERE nickname = ?"
                cursor.execute(query, params)
                conn.commit()
                return True
            return False
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        finally:
            conn.close()
    
    def delete_player(self, nickname: str) -> bool:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM players WHERE nickname=?", (nickname,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        finally:
            conn.close()

