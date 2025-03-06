import sqlite3
from typing import Optional
from functools import lru_cache
from datetime import datetime

# Classes
from env.classes.classes import User, Message

# Config
from env.config import config

sql_users: str = """
CREATE TABLE IF NOT EXISTS users (
    user_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    username    TEXT UNIQUE NOT NULL,
    ip          TEXT UNIQUE NOT NULL,

    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""
sql_messages: str = """
CREATE TABLE IF NOT EXISTS messages (
    message_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id             INTEGER NOT NULL,
    content             TEXT NOT NULL,

    sent_timestamp      DATETIME DEFAULT CURRENT_TIMESTAMP,
    received_timestamp  DATETIME DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
);
"""

class Database:
    def __init__(self) -> None:
        self.db_path: str = config.db_path
        self.conn: sqlite3.Connection = sqlite3.connect(database=self.db_path)
        self.cur: sqlite3.Cursor = self.conn.cursor()

        # Create tables if not exist
        self.cur.executescript(sql_users + sql_messages)

    def get_users(self) -> list[User]:
        return [User(user_id=user[0], username=user[1], ip=user[2], created_at=user[3]) for user in self.cur.execute("SELECT user_id, username, ip, created_at from users").fetchall()]
    #! Fix this
    @lru_cache(maxsize=50)
    def _get_user(self, user_id: int) -> User:
        user: tuple[Optional[int], str, str] = self.cur.execute("SELECT user_id, username, ip FROM users WHERE user_id = ?", (user_id,)).fetchone()
        if not user: raise ValueError(f"User with id {user_id} does not exist!")
        return User(user_id=user[0], username=user[1], ip=user[2])

    def get_messages(self, user_id: int) -> list[Message]:
        messages: list[tuple[int, str, str, str]] = self.cur.execute("SELECT user_id, content, sent_timestamp, received_timestamp from messages WHERE user_id = ?", (user_id,)).fetchall()
        return [
            Message(
                    user=self._get_user(msg[0]),
                    content=msg[1],
                    sent_timestamp=(datetime.strptime(msg[2],config.datetime_format) if msg[2] else None),
                    received_timestamp=(datetime.strptime(msg[3], config.datetime_format) if msg[3] else None)
            ) for msg in messages
        ]

    def insert_user(self, user: User) -> None:
        self.cur.execute("INSERT OR IGNORE INTO users (username, ip) VALUES (?, ?)", (user.username, user.ip))
        user.update_id(self.cur.lastrowid or self.cur.execute("SELECT user_id FROM users WHERE username = ? AND ip = ?", (user.username, user.ip)).fetchone()[0])  # Set the new user_id to the User instance
        self.conn.commit()

    def insert_message(self, message: Message) -> None:
        self.cur.execute("INSERT OR IGNORE INTO messages (user_id, content) VALUES (?, ?)", (message.user_id, message.content))
        self.conn.commit()
