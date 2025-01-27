from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

# Config
from env_03.config import config

# ChatFile
from env_03.func.chatfile import chatfile

#ToDo: Store the salt in a file or database for later use
#ToDo: Add a function that asks the user for a password and then generates the key from that password

class AES:
    def __init__(self, key: bytes) -> None:
        self.key = key
        self.salt = chatfile.aes_salt

        if len(self.salt) != 16:
            raise ValueError(f"Salt must be 16 bytes long! Not {len(self.salt)}.")

    def _derive_key(self) -> bytes:
        """
        Derive a key from the provided key and salt using PBKDF2HMAC.
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(self.key))

    def encrypt(self, message: str) -> bytes:
        """
        Encrypt a message using the derived key.
        """
        derived_key = self._derive_key()
        fernet = Fernet(derived_key)
        return fernet.encrypt(message.encode(config.encoding))

    def decrypt(self, encrypted_message: bytes) -> str:
        """
        Decrypt an encrypted message using the derived key.
        """
        derived_key = self._derive_key()
        fernet = Fernet(derived_key)
        return fernet.decrypt(encrypted_message).decode(config.encoding)
