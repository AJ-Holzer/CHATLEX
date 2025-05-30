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
        key: Optional[bytes] = None,
    ) -> None:
        # Initialize hasher
        self._argon_hasher: ArgonHasher = ArgonHasher()

        # Define salt, iv and key
        self._password: str = password
        self._salt: Optional[bytes] = salt
        self._iv: Optional[bytes] = iv
        self._key: Optional[bytes] = key

    def generate_iv(self) -> None:
        self._iv = token_bytes(16)

    def generate_salt(self) -> None:
        self._salt = token_bytes(config.SALT_LENGTH)

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
