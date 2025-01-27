import socket

# Func
from env_01.func.db import init_db

# class DB:
#     def __init__(self) -> None:
#         self.conn, self.cur = init_db()

#     def write(self, task: str, values: tuple[str]) -> None:
#         self.cur.execute(task, values)
#         self.conn.commit()
    
#     def update_values(self, entity: str, uid: str, values: list[tuple[str, str]]) -> None:
#         task: str = "UPDATE ? SET ? = ? WHERE uid = ?"
#         for column, value in values:
#             self.cur.execute(task, (entity, column, value, uid))
#         self.conn.commit()

#     def __del__(self) -> None:
#         self.conn.commit()
#         self.conn.close()
#         print("DB saved!")

class Message:
    def __init__(self, header: str, body: str, timestamp: float) -> None:
        self.header: str = header
        self.body: str = body
        self.timestamp: float = timestamp
        self.sent: bool
        self.uid: str

class User:
    def __init__(self, uid: str, name: str, ip: str, port: int, messages: list[Message]) -> None:
        self.uid: str = uid
        self.username: str = name
        self.ip: str = ip
        self.port: int = port
        self.messages: list[Message] = []

    # def upate_user(self) -> None:
    #     raise NotImplementedError("This code is not implemented yet!")

    # def update_messages(self, message: Message) -> None:
    #     if message in self.messages:
    #         raise ValueError("Message already exists in the user's messages!")
    #     self.messages.append(message)
    #     self.write("INSERT INTO messages (header, body, timestamp, uid) VALUES (?, ?, ?, ?)", (message.header, message.body, message.timestamp, message.uid))

class DB:
    def __init__(self) -> None:
        self.message_insert: str = "INSERT INTO messages (header, body, timestamp, uid) VALUES (?, ?, ?, ?)"
        self.user_insert: str = "INSERT INTO users (uid, username, ip, port) VALUES (?, ?, ?, ?)"
        self.conn, self.cur = init_db()
        self.existing_users: list[User]

    def insert_message(self, message: Message) -> None:
        self.cur.execute(self.message_insert, (message.header, message.body, message.timestamp))
        self.conn.commit()

    def insert_user(self, uid: str, username: str, ip: str, port: int) -> None:
        self.cur.execute(self.user_insert, (uid, username, ip, port))
        self.conn.commit()
    
    def _retrieve_message_by_user(self, user_id: str) -> tuple[tuple[int, str, str, str, int], list[Message]]:
        users: list[tuple[int, str, str, str, int]] = self.cur.execute("SELECT * FROM users WHERE uid = ?", (user_id)).fetchall()
        if len(users) > 1: raise ValueError(f"Multiple users with the same uid! --> {users}")
        elif len(users) < 1: raise ValueError(f"No user with the uid {user_id}!")
        return users[0], [Message(header, body, timestamp) for _, header, body, timestamp in self.cur.execute("SELECT * FROM messages WHERE uid = ?", (user_id,)).fetchall()]

    def retrieve_user(self, user_id: str) -> User:
        user, messages = self._retrieve_message_by_user(user_id)
        return User(user[1], user[2], user[3], user[4], messages)

    def __del__(self) -> None:
        self.conn.commit()
        self.conn.close()
        print("DB saved!")
