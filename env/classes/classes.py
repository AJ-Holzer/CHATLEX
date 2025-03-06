import re
from typing import Optional
from datetime import datetime

class User:
    def __init__(self, user_id: Optional[int], username: str, ip: str) -> None:
        self.user_id: Optional[int] = user_id
        self.username: str = username
        self.ip: str = ip
        self.online: bool = False
    
    def update_id(self, new_id: int) -> None: assert isinstance(new_id, int), f"Expected int, got {type(new_id)}"; self.user_id = new_id

    def __str__(self) -> str: return f"User(user_id={self.user_id}, username='{self.username}', ip='{self.ip}', online={self.online})"
    def __repr__(self) -> str: return f"user_id={self.user_id}, username='{self.username}', ip='{self.ip}', online={self.online}"

class Message:
    def __init__(self, user: User, content: str, sent_timestamp: Optional[datetime], received_timestamp: Optional[datetime]) -> None:
        if not user.user_id: raise ValueError("User ID is not set!")

        self.user_id: int = user.user_id
        self.content: str = content.translate(str.maketrans({"\\": r"\\", "\n": r"\n", "\r": r"\r"}))  #type:ignore[arg-type]
        self.sent_timestamp: Optional[datetime] = sent_timestamp
        self.received_timestamp: Optional[datetime] = received_timestamp

    def __str__(self) -> str: return f"message='{self.content}'"
    def __repr__(self) -> str: return f"Message(user_id={self.user_id}, content='{self.content}', sent_timestamp={self.sent_timestamp}, received_timestamp={self.received_timestamp})"
