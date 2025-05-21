import re
from base64 import b64decode, b64encode
from secrets import token_bytes
from typing import Any

from argon2 import PasswordHasher
from argon2.low_level import Type, hash_secret_raw
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Config
from env.config import config

ARGON2_HASH_PATTERN: re.Pattern[Any] = re.compile(
    r"^\$argon2(id|i)\$v=\d+\$m=\d+,t=\d+,p=\d+\$.+"
)


def is_valid_argon2_hash(hash_str: str) -> bool:
    """Check if a given string matches the Argon2 hash pattern.

    Args:
        hash_str(str): The string to check against the Argon2 hash pattern.

    Returns:
        bool: True if the string matches the Argon2 hash pattern, False otherwise.

    Raises:
        re.error: If the provided hash_str is not a valid regular expression.
    """
    return bool(ARGON2_HASH_PATTERN.match(hash_str))


def byte_to_str(data: bytes) -> str:
    """Convert bytes to string using base64 encoding.

    Args:
        data(bytes): Bytes data to be converted.

    Returns:
        str: Base64 encoded string.

    Raises:
        binascii.Error: If the bytes data is not valid base64 encoded data.
        UnicodeDecodeError: If the base64 encoded data cannot be decoded using UTF-8.
    """
    return b64encode(data).decode("UTF-8")


def str_to_byte(data: str) -> bytes:
    """Convert a string to bytes using base64 decoding.

    Args:
        data(str): String to be converted to bytes.

    Returns:
        bytes: Bytes representation of the input string.

    Raises:
        binascii.Error: Raised if the input string is not a valid base64 encoded string.
        UnicodeEncodeError: Raised if the input string cannot be encoded using UTF-8.
    """
    return b64decode(data.encode("UTF-8"))


def generate_iv() -> bytes:
    """Generates a 16-byte Initialization Vector (IV).

    Args:
        None(None): No parameters are needed.

    Returns:
        bytes: A 16-byte Initialization Vector (IV).

    Raises:
        Exception: If token_bytes function fails unexpectedly.
    """
    return token_bytes(16)


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a 256-bit key from a password using Argon2id."""
    key: bytes = hash_secret_raw(
        secret=password.encode(),
        salt=salt,
        time_cost=config.ARGON2_TIME_COST,
        memory_cost=config.ARGON2_MEMORY_COST,
        parallelism=config.ARGON2_PARALLELISM,
        hash_len=config.ARGON2_HASH_LEN,
        type=Type.ID,
    )
    return key


def aes_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    """Encrypt data using AES in CBC mode.

    Args:
        plaintext(bytes): Data to be encrypted.
        key(bytes): Encryption key.
        iv(bytes): Initialization vector.

    Returns:
        bytes: Ciphertext.

    Raises:
        ValueError: If the key or IV is not the correct length.
        TypeError: If input data is not bytes.
    """
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return ciphertext


def aes_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    """Decrypts ciphertext using AES in CBC mode with PKCS7 padding.

    Args:
        ciphertext(bytes): Ciphertext to decrypt.
        key(bytes): Secret key for AES decryption.
        iv(bytes): Initialization vector (IV) for CBC mode.

    Returns:
        bytes: Decrypted plaintext.

    Raises:
        ValueError: If the key or IV length is invalid.
        cryptography.exceptions.InvalidTag: If the ciphertext is tampered with or the key is incorrect.
    """
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    return plaintext


def hash_password(password: str) -> str:
    """Hashes a given password using Argon2.

    Args:
        password(str): The password to hash.

    Returns:
        str: The Argon2 hash of the password.

    Raises:
        ValueError: Raised if no password is provided.
    """
    if not password:
        raise ValueError("No password provided!")

    ph: PasswordHasher = PasswordHasher(
        time_cost=config.ARGON2_TIME_COST,
        memory_cost=config.ARGON2_MEMORY_COST,
        parallelism=config.ARGON2_PARALLELISM,
        hash_len=config.ARGON2_HASH_LEN,
    )
    return ph.hash(password)


def verify_password(hash: str, password: str) -> bool:
    """Verifies if a given password matches a given Argon2 hash.

    Args:
        hash(str): The Argon2 hash to verify.
        password(str): The password to verify against the hash.

    Returns:
        bool: True if the password matches the hash, False otherwise.

    Raises:
        Exception: Generic exception during hash verification.
    """
    if not is_valid_argon2_hash(hash):
        print("Hash format invalid or potentially unsafe.")
        return False

    ph: PasswordHasher = PasswordHasher(
        time_cost=config.ARGON2_TIME_COST,
        memory_cost=config.ARGON2_MEMORY_COST,
        parallelism=config.ARGON2_PARALLELISM,
        hash_len=config.ARGON2_HASH_LEN,
    )
    try:
        return ph.verify(hash, password)
    except Exception:
        return False
