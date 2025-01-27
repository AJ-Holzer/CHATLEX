import socket
from typing import Optional, Any

# Config
from env_03.config import config

# Encryption
from env_03.func.Encryption import AES

# Exeptions
from env_03.func.Exeptions import NoSocketObject

class User:
    def __init__(self, aes: AES, address: str) -> None:
        self.address: str = address
        self.port: int = config.port
        self.username: Optional[str] = None
        self.sock_obj: Optional[socket.socket] = None
        self.aes: AES = aes

    def update_connection(self, address: str, port: int) -> None: self.address, self.port = address, port
    def update_username(self, username: str) -> None: self.username = username
    def connect(self) -> None:
        try:
            self.sock_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock_obj.connect((self.address, self.port))
            received_data = self.sock_obj.recv(config.buf_size)
            if received_data:
                try:
                    self.username = self.aes.decrypt(received_data)
                except Exception as e:
                    print(f"Error: {e}")
                    self.sock_obj.close()
            else:
                print("No data received from the user.")
                return
        except Exception as e:
            print(f"Error while connecting to user! Error: {e}")
            return
    
    def send(self, message: str) -> None:
        if not self.sock_obj: raise NoSocketObject("No socket object defined! Maybe the user is offline?")
        
        try:                   self.sock_obj.sendall(self.aes.encrypt(str(message)))
        except Exception as e: print(f"Error while sending message! Error: {e}")

class Message:
    def __init__(self) -> None:
        self.content: Optional[str] = None
        self.timestamp: Optional[str] = None
        self.sent: bool = False
        self.read: bool = False
        self.sender: Optional[User] = None

    def update_content(self, content: str) -> None: self.content = content
    def update_timestamp(self, timestamp: str) -> None: self.timestamp = timestamp
    def mark_as_sent(self) -> None: self.sent = True
    def mark_as_read(self) -> None: self.read = True

class Chat:
    def __init__(self, friend: User) -> None:
        self.friend: User = friend
        self.messages: list[Message] = []
        self.message_queue: list[Message] = []
    
    def add_message(self, message: Message) -> None: self.messages.append(message)
    def send_messages(self) -> None:
        for message in self.message_queue:
            if not message.content: continue
            self.friend.send(message.content)

class Client():
    def __init__(self) -> None:
        self.username: Optional[str] = None
        self.chats: list[Chat] = []
        self.friends: list[User] = []

        # Init connection
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("0.0.0.0", config.port))

    def connect_to_friends(self) -> None:
        # Add chats
        self.chats  += [Chat(user) for user in self.friends]
        # Connect to friends
        for chat in self.chats:
            chat.friend.connect()

    def add_friend(self, friend: User) -> None:    self.friends.append(friend)
    def remove_friend(self, friend: User) -> None: self.friends.remove(friend)
