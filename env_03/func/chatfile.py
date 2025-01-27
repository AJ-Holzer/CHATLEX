import os
import json
import secrets
import base64
from typing import Any

# Config
from env_03.config import config

class ChatFile:
    def __init__(self, file_path: str) -> None:
        self.file_path: str = file_path
        self.file_data = self._load_data()
        self.aes_salt: bytes = base64.b64decode(self.file_data.get("AES-Salt") or self._generate_salt())

    def _load_data(self) -> dict[str, Any]:
        if not os.path.exists(self.file_path):
            return {}

        with open(self.file_path, "rb") as file:
            return json.loads(file.read().decode(config.encoding))

    def _generate_salt(self) -> str:
        """Generate a random salt."""
        salt = base64.b64encode(secrets.token_bytes(16)).decode(config.encoding)  # 16 bytes (128 bits) is a common size for AES salts
        self._save_data({"AES-Salt": salt})
        return salt

    def _save_data(self, data: dict[str, Any]) -> None:
        """Save data to the file, merging with existing data."""
        existing_data = self._load_data()
        updated_data = {**existing_data, **data}
        with open(self.file_path, "wb") as file:
            file.write(json.dumps(updated_data).encode(config.encoding))

chatfile = ChatFile(config.chatfile_path)
