import sqlite3

# Classes
from env_01.func.Classes import Message, User

# Config
from env_01.config import config


def init_db() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    message_init: str = """CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        header TEXT,
        body TEXT,
        timestamp FLOAT,
        uid TEXT
    )"""
    user_init: str = """CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uid TEXT,
        username TEXT,
        ip TEXT,
        port INTEGER
    )"""
    conn = sqlite3.connect(config.db_name)
    cur = conn.cursor()
    # Create tables
    for i in [message_init, user_init]: cur.execute(i)
    conn.commit()
    return conn, cur
