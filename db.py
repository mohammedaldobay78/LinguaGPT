# db.py
import sqlite3
import time
from contextlib import closing

DB_NAME = "bot.db"

def init_db():
    with closing(sqlite3.connect(DB_NAME)) as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            level TEXT DEFAULT 'A1',
            unit INTEGER DEFAULT 1,
            lessons_completed INTEGER DEFAULT 0,
            coins INTEGER DEFAULT 0,
            vip_pronunciation INTEGER DEFAULT 0,
            upgrade_a INTEGER DEFAULT 0,
            upgrade_b INTEGER DEFAULT 0,
            boost_quizzes INTEGER DEFAULT 0,
            learning_24h_until INTEGER DEFAULT 0,
            last_daily_gift_date TEXT DEFAULT ''
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS lesson_sessions (
            user_id INTEGER PRIMARY KEY,
            start_ts INTEGER DEFAULT 0
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS quiz_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            level TEXT,
            unit INTEGER,
            score INTEGER,
            ts INTEGER
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            item TEXT,
            ts INTEGER
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS pronunciation_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            transcript TEXT,
            score REAL,
            feedback TEXT,
            ts INTEGER
        )
        """)
        conn.commit()

# user helpers
def create_user_if_not_exists(user_id, username):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        c = conn.cursor()
        c.execute("SELECT 1 FROM users WHERE user_id=?", (user_id,))
        if not c.fetchone():
            c.execute("INSERT INTO users(user_id, username) VALUES(?,?)", (user_id, username or ""))
            conn.commit()

def get_user(user_id):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        row = c.fetchone()
        return dict(row) if row else None

def update_user_field(user_id, field, value):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        c = conn.cursor()
        c.execute(f"UPDATE users SET {field}=? WHERE user_id=?", (value, user_id))
        conn.commit()

def add_coins(user_id, amount):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        c = conn.cursor()
        c.execute("UPDATE users SET coins = coins + ? WHERE user_id=?", (amount, user_id))
        conn.commit()

def spend_coins(user_id, amount):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        c = conn.cursor()
        c.execute("SELECT coins FROM users WHERE user_id=?", (user_id,))
        row = c.fetchone()
        if not row: return False
        if row[0] < amount: return False
        c.execute("UPDATE users SET coins = coins - ? WHERE user_id=?", (amount, user_id))
        conn.commit()
        return True

def record_purchase(user_id, item):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO purchases(user_id,item,ts) VALUES(?,?,?)", (user_id, item, int(time.time())))
        conn.commit()

# lesson session
def start_lesson_session(user_id):
    now = int(time.time())
    with closing(sqlite3.connect(DB_NAME)) as conn:
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO lesson_sessions(user_id, start_ts) VALUES(?,?)", (user_id, now))
        conn.commit()

def get_lesson_session_start(user_id):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        c = conn.cursor()
        c.execute("SELECT start_ts FROM lesson_sessions WHERE user_id=?", (user_id,))
        row = c.fetchone()
        return row[0] if row else 0

def end_lesson_session(user_id):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM lesson_sessions WHERE user_id=?", (user_id,))
        conn.commit()

# quizzes
def save_quiz_result(user_id, level, unit, score):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO quiz_history(user_id,level,unit,score,ts) VALUES(?,?,?,?,?)", (user_id, level, unit, score, int(time.time())))
        conn.commit()
    # reward coin
    add_coins(user_id, 1)

# pronunciation
def save_pronunciation(user_id, transcript, score, feedback):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO pronunciation_scores(user_id,transcript,score,feedback,ts) VALUES(?,?,?,?,?)",
                  (user_id, transcript, score, feedback, int(time.time())))
        conn.commit()

# daily gift
def give_daily_gift(user_id):
    import datetime
    today = datetime.date.today().isoformat()
    u = get_user(user_id)
    if not u:
        return False
    if u['last_daily_gift_date'] == today:
        return False
    add_coins(user_id, 5)
    update_user_field(user_id, 'last_daily_gift_date', today)
    return True