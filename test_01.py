from env_03.func.Encryption import AES
from env_03.func.Classes import Client, User

client = Client()
aes = AES(b"key")

# Create a test friend
friend = User(aes=aes, address="127.0.0.1")

# Add a test friend
client.add_friend(friend)

client.connect_to_friends()
