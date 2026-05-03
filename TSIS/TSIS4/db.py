import psycopg2
from config import DB_CONFIG

def get_connection():
    """
    Подключение к базе данных PostgreSQL (с запасным планом на postgres).
    """
    try:
        return psycopg2.connect(**DB_CONFIG)
    except psycopg2.OperationalError:
        # Fallback to default postgres if phonebook fails
        fallback = DB_CONFIG.copy()
        fallback['database'] = 'postgres'
        return psycopg2.connect(**fallback)

def init_db():
    """
    Инициализация таблиц для игроков (players) и игровых сессий (game_sessions).
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_sessions (
            id SERIAL PRIMARY KEY,
            player_id INTEGER REFERENCES players(id),
            score INTEGER NOT NULL,
            level_reached INTEGER NOT NULL,
            played_at TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

def save_score(username, score, level):
    """
    Сохранение результата игры в базу данных. Если игрок новый, он добавляется.
    """
    if not username:
        username = "Guest"
    conn = get_connection()
    cursor = conn.cursor()
    
    # Insert or get player
    cursor.execute("SELECT id FROM players WHERE username = %s", (username,))
    row = cursor.fetchone()
    if row:
        player_id = row[0]
    else:
        cursor.execute("INSERT INTO players (username) VALUES (%s) RETURNING id", (username,))
        player_id = cursor.fetchone()[0]
    
    # Insert session
    cursor.execute("""
        INSERT INTO game_sessions (player_id, score, level_reached)
        VALUES (%s, %s, %s)
    """, (player_id, score, level))
    
    conn.commit()
    cursor.close()
    conn.close()

def get_top_10():
    """
    Получение 10 лучших результатов для таблицы рекордов (Leaderboard).
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.username, s.score, s.level_reached, s.played_at
            FROM game_sessions s
            JOIN players p ON p.id = s.player_id
            ORDER BY s.score DESC, s.played_at DESC
            LIMIT 10
        """)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except Exception:
        return []

def get_personal_best(username):
    """
    Получение личного рекорда (PB) для конкретного игрока по его имени.
    """
    if not username: 
        return 0
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT MAX(s.score)
            FROM game_sessions s
            JOIN players p ON p.id = s.player_id
            WHERE p.username = %s
        """, (username,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row[0] if row and row[0] else 0
    except Exception:
        return 0
