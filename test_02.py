import base64
import json

with open("chatfile.dat", "rb") as f:
    print(base64.b64decode(json.loads(f.read().decode())["AES-Salt"]))