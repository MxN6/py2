import os
import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

DB_AVAILABLE = True

try:
    def get_connection():
        return psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )

    def ensure_tables():
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS players (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL
                    );
                    CREATE TABLE IF NOT EXISTS game_sessions (
                        id SERIAL PRIMARY KEY,
                        player_id INTEGER REFERENCES players(id),
                        score INTEGER NOT NULL,
                        level_reached INTEGER NOT NULL,
                        played_at TIMESTAMP DEFAULT NOW()
                    );
                    """
                )
                conn.commit()

    def get_player_id(username):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO UPDATE SET username = EXCLUDED.username RETURNING id;",
                    (username,),
                )
                player_id = cur.fetchone()[0]
                conn.commit()
                return player_id

    def save_game_session(username, score, level):
        player_id = get_player_id(username)
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s);",
                    (player_id, score, level),
                )
                conn.commit()

    def fetch_leaderboard(limit=10):
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT p.username, gs.score, gs.level_reached, gs.played_at FROM game_sessions gs "
                    "JOIN players p ON p.id = gs.player_id "
                    "ORDER BY gs.score DESC, gs.played_at DESC LIMIT %s;",
                    (limit,),
                )
                return cur.fetchall()

    def fetch_personal_best(username):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT MAX(gs.score) FROM game_sessions gs "
                    "JOIN players p ON p.id = gs.player_id "
                    "WHERE p.username = %s;",
                    (username,),
                )
                result = cur.fetchone()[0]
                return result if result is not None else 0

    ensure_tables()
except Exception:
    DB_AVAILABLE = False
