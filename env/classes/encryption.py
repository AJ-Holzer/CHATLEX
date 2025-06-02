import base64
from secrets import token_bytes
from typing import Optional

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import (
    Cipher,
    CipherContext,
    algorithms,
    modes,
)

from env.classes.hashing import ArgonHasher

# Config
from env.config import config


class AES:
    def __init__(
        self,
        password: str,
        salt: Optional[bytes] = None,
        iv: Optional[bytes] = None,
    ) -> None:
        """Initializes an instance of the class.

        Args:
            self(Self): The instance of the class.
            password(str): The password to be stored.
            salt(Optional[bytes]): The salt to be used for password hashing. If None, a new salt will be generated.
            iv(Optional[bytes]): The initialization vector (IV) to be used for encryption. If None, a new IV will be generated.

        Returns:
            None: No return value.

        Raises:
            ValueError: If the password is empty or None.
        """
        # Initialize hasher
        self._argon_hasher: ArgonHasher = ArgonHasher()

        # Define salt, iv and key
        self._password: str = password
        self._salt: bytes = salt or self.generate_salt()
        self._iv: bytes = iv or self.generate_iv()
        self._key: Optional[bytes] = self._argon_hasher.derive_key(
            password=self._password, salt=self._salt
        )

    def generate_iv(self) -> bytes:
        iv: bytes = token_bytes(16)
        self._iv = iv

        return iv

    def generate_salt(self) -> bytes:
        salt: bytes = token_bytes(config.SALT_LENGTH)
        self._salt = salt

        return salt

    def encrypt(self, plaintext: str) -> bytes:
        padder: padding.PaddingContext = padding.PKCS7(128).padder()
        byte_data: bytes = base64.b64encode(s=plaintext.encode(config.ENCODING))
        padded_data: bytes = padder.update(byte_data) + padder.finalize()

        cipher: Cipher[modes.CBC] = Cipher(
            algorithm=algorithms.AES256(key=self.key),
            mode=modes.CBC(self.iv),
            backend=default_backend(),
        )
        encryptor: CipherContext = cipher.encryptor()
        cipher_text: bytes = encryptor.update(padded_data) + encryptor.finalize()

        return cipher_text

    def decrypt(self, ciphertext: bytes) -> str:
        cipher: Cipher[modes.CBC] = Cipher(
            algorithm=algorithms.AES256(key=self.key),
            mode=modes.CBC(self.iv),
            backend=default_backend(),
        )
        decryptor: CipherContext = cipher.encryptor()
        padded_data: bytes = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder: padding.PaddingContext = padding.PKCS7(128).unpadder()
        cipher_text: bytes = unpadder.update(padded_data) + unpadder.finalize()

        return base64.b64decode(cipher_text).decode(config.ENCODING)

    @property
    def salt(self) -> bytes:
        if not self._salt:
            raise TypeError("No salt provided. Generate salt first!")

        return self._salt

    @salt.setter
    def salt(self, salt: bytes) -> None:
        if not salt:
            raise ValueError("No salt provided!")

        self._salt = salt

    @property
    def iv(self) -> bytes:
        if not self._iv:
            raise TypeError("No salt provided. Generate salt first!")

        return self._iv

    @iv.setter
    def iv(self, iv: bytes) -> None:
        if not iv:
            raise ValueError("No iv provided!")

        self._iv = iv

    @property
    def key(self) -> bytes:
        if not self._key:
            raise TypeError("No key provided. Generate key first!")

        return self._key

    @key.setter
    def key(self, key: bytes) -> None:
        if not key:
            raise ValueError("No key provided!")

        self._key = key
