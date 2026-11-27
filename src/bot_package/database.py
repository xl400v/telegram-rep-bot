import os, sqlite3
from bot_package import config as ENV  # Импорт из __init__.py

# Гарантируем, что директория для БД существует
db_dir = os.path.dirname(ENV.database_url)
if db_dir:
    os.makedirs(db_dir, exist_ok=True)

conn = sqlite3.connect(ENV.database_url, check_same_thread=False)
cur = conn.cursor()

def init():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        balance INTEGER DEFAULT 0
    )
    """)
    conn.commit()

def get_user_balance(user_id: int):
    cur.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    return cur.fetchone()

def set_user_balance(user_id: int, amount: int):
    cur.execute("UPDATE users SET balance = balance + ? WHERE user_id=?", (amount, user_id,))
    conn.commit()

def add_user(user_id: int):
    cur.execute("INSERT INTO users (user_id, balance) VALUES (?, 10)", (user_id,))
    conn.commit()