import sqlite3
from typing import Any, Optional

# Config
from env.config import config

class CCursor:
    def __init__(self) -> None:
        self.conn: sqlite3.Connection = sqlite3.connect(config.db_name)
        self.cur: sqlite3.Cursor = self.conn.cursor()

        # Create tables if not exist
        self.write(config.create_messages, ())
        self.write(config.create_users, ())

    def write(self, task: str, values: tuple[Any, ...]) -> None:
        if values: self.cur.execute(task, values)
        else:      self.cur.execute(task)
        self.conn.commit()

class User(CCursor):
    def __init__(self, uid: str | None) -> None:
        super().__init__()
        if not uid: raise ValueError("Provide an uid!")
        self.uid: str = uid
        self.username: str
        self.address: str
        self.port: int
        self.messages: list[Message]
    
    def retrieve_messages(self) -> None:
        messages_tmp: list[tuple[Any]] = self.cur.execute("SELECT content FROM messages WHERE user_id = ?", (self.uid,)).fetchall()
        if messages_tmp: self.messages = [Message(user_id, timestamp, content) for i in messages_tmp for user_id, timestamp, content in i]
        else:            print("No messages found!")

class Message(CCursor):
    def __init__(self, user_id: str, timestamp: float, content: str) -> None:
        self.message_id: int
        self.user_uid: str = user_id
        self.content: str = content
        self.timestamp: float = timestamp
        self.sent: bool

    def mark_as_sent(self) -> None: self.sent = True
    def mark_as_unsent(self) -> None: self.sent = False

    #ToDo: Implement this function correctly
    # def add(self, user_id: str, content: str, timestamp: float) -> None:
    #     self.write("INSERT INTO messages (user_id, timestamp, content, sent) VALUES (?, ?, ?, ?)", (user_id, timestamp, content, False))
