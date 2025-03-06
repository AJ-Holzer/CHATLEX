import time
from pprint import pprint
from env.classes.db import Database
from env.classes.classes import User, Message
from datetime import datetime

db = Database()

user1: User = User(user_id=None, username="AJ", ip="198.168.8.110")
db.insert_user(user=user1)

msg1: Message = Message(user=user1, content="Hello!\nDear friend...", sent_timestamp=datetime.now(), received_timestamp=None)
# db.insert_message(message=msg1)

# print(str(msg1))

users: list[User] = db.get_users()
messages: list[tuple[int, list[Message]]] = [(user.user_id, db.get_messages(user_id=user.user_id)) for user in users if user.user_id]

# print()
print(f"Messages:\n{"\n".join(str(msg) for id, msgs in messages for msg in msgs)}")
