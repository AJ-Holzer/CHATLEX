import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import (
    Cipher,
    CipherContext,
    algorithms,
    modes,
)

from env.classes.hashing import HKDFHasher
from env.config import config
from env.func.generations import generate_iv, generate_salt
from env.typing.hashing import HKDFInfoKey


class AES:
    def __init__(self, derived_key: bytes, salt: bytes) -> None:
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
        self._salt: bytes = salt
        self._derived_key: bytes = derived_key
        self._hkdf_hasher: HKDFHasher = HKDFHasher(derived_key=self._derived_key)

    def encrypt(self, plaintext: str, encryption_key_info: HKDFInfoKey) -> bytes:
        # Generate a new IV, salt and key
        iv: bytes = generate_iv()
        salt: bytes = generate_salt(config.SALT_LENGTH)
        encryption_key: bytes = self._hkdf_hasher.derive_random_key(
            info=encryption_key_info
        )

        padder: padding.PaddingContext = padding.PKCS7(128).padder()
        byte_data: bytes = base64.b64encode(s=plaintext.encode(config.ENCODING))
        padded_data: bytes = padder.update(byte_data) + padder.finalize()

        cipher: Cipher[modes.CBC] = Cipher(
            algorithm=algorithms.AES256(key=encryption_key),
            mode=modes.CBC(iv),
            backend=default_backend(),
        )
        encryptor: CipherContext = cipher.encryptor()
        cipher_text: bytes = encryptor.update(padded_data) + encryptor.finalize()

        return salt + iv + cipher_text

    def decrypt(self, encrypted_data: bytes, encryption_key_info: HKDFInfoKey) -> str:
        # Retrieve salt, IV and ciphertext
        salt = encrypted_data[: config.SALT_LENGTH :]
        iv = encrypted_data[config.SALT_LENGTH : config.SALT_LENGTH + 16 :]
        decryption_key: bytes = self._hkdf_hasher.derive_key(
            info=encryption_key_info, salt=salt
        )

        ciphertext = encrypted_data[config.SALT_LENGTH + 16 : :]

        cipher: Cipher[modes.CBC] = Cipher(
            algorithm=algorithms.AES256(key=decryption_key),
            mode=modes.CBC(iv),
            backend=default_backend(),
        )
        decryptor: CipherContext = cipher.decryptor()
        padded_data: bytes = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder: padding.PaddingContext = padding.PKCS7(128).unpadder()
        cipher_text: bytes = unpadder.update(padded_data) + unpadder.finalize()

        return base64.b64decode(cipher_text).decode(config.ENCODING)
