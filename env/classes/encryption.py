from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import (AEADDecryptionContext,
                                                    AEADEncryptionContext,
                                                    Cipher, algorithms, modes)

from env.classes.hashing import HKDFHasher
from env.config import config
from env.func.generations import generate_iv, generate_salt
from env.typing.hashing import HKDFInfoKey


class AES_256_GCM:
    def __init__(self, derived_key: bytes) -> None:
        self._derived_key: bytes = derived_key
        self._hkdf_hasher: HKDFHasher = HKDFHasher(derived_key=self._derived_key)

    def encrypt(self, plaintext: str, encryption_key_info: HKDFInfoKey) -> bytes:
        iv: bytes = generate_iv(length=config.AES_256_GCM_IV_LENGTH)
        salt: bytes = generate_salt(length=config.SALT_LENGTH)
        encryption_key: bytes = self._hkdf_hasher.derive_key(
            info=encryption_key_info,
            salt=salt,
        )

        # Create cipher text
        cipher: Cipher[modes.GCM] = Cipher(
            algorithm=algorithms.AES256(encryption_key),
            mode=modes.GCM(iv),
            backend=default_backend(),
        )
        encryptor: AEADEncryptionContext = cipher.encryptor()
        ciphertext: bytes = (
            encryptor.update(plaintext.encode(config.ENCODING)) + encryptor.finalize()
        )

        return salt + iv + ciphertext + encryptor.tag

    def decrypt(self, encrypted_data: bytes, encryption_key_info: HKDFInfoKey) -> str:
        salt: bytes = encrypted_data[: config.SALT_LENGTH :]
        iv: bytes = encrypted_data[
            config.SALT_LENGTH : config.SALT_LENGTH + config.AES_256_GCM_IV_LENGTH :
        ]
        tag: bytes = encrypted_data[-16::]
        ciphertext: bytes = encrypted_data[
            config.SALT_LENGTH + config.AES_256_GCM_IV_LENGTH : -16 :
        ]

        # Retrieve decryption key
        decryption_key: bytes = self._hkdf_hasher.derive_key(
            info=encryption_key_info,
            salt=salt,
        )

        # Decrypt cipher text
        cipher: Cipher[modes.GCM] = Cipher(
            algorithm=algorithms.AES256(decryption_key),
            mode=modes.GCM(iv, tag),
            backend=default_backend(),
        )
        decryptor: AEADDecryptionContext = cipher.decryptor()
        plaintext_bytes: bytes = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext_bytes.decode(config.ENCODING)
