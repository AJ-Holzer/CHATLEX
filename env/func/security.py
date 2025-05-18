from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from argon2 import PasswordHasher
from argon2.low_level import Type, hash_secret_raw
from secrets import token_bytes
from base64 import b64encode, b64decode
import re

ARGON2_HASH_PATTERN = re.compile(r"^\$argon2(id|i)\$v=\d+\$m=\d+,t=\d+,p=\d+\$.+")

# Config
from env.config import config


def is_valid_argon2_hash(hash_str: str) -> bool:
    return bool(ARGON2_HASH_PATTERN.match(hash_str))

def byte_to_str(data: bytes) -> str:
    """Convert bytes to a base64-encoded UTF-8 string."""
    return b64encode(data).decode('UTF-8')

def str_to_byte(data: str) -> bytes:
    """Convert a base64-encoded UTF-8 string to bytes."""
    return b64decode(data.encode('UTF-8'))

def generate_iv() -> bytes:
    """Securely generate a 16-byte IV for AES-CBC."""
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
        type=Type.ID
    )
    return key

def aes_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    """Encrypt plaintext using AES-256-CBC with PKCS7 padding."""
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return ciphertext

def aes_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    """Decrypt ciphertext using AES-256-CBC with PKCS7 padding."""
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    return plaintext

def hash_password(password: str) -> str:
    """Hash a password using Argon2id (for storing securely)."""
    if not password:
        raise ValueError("No password provided!")
    
    ph: PasswordHasher = PasswordHasher(
        time_cost=config.ARGON2_TIME_COST,
        memory_cost=config.ARGON2_MEMORY_COST,
        parallelism=config.ARGON2_PARALLELISM,
        hash_len=config.ARGON2_HASH_LEN
    )
    return ph.hash(password)

def verify_password(hash: str, password: str) -> bool:
    """Verify an Argon2id password hash."""
    if not is_valid_argon2_hash(hash):
        print("Hash format invalid or potentially unsafe.")
        return False
    
    ph: PasswordHasher = PasswordHasher(
        time_cost=config.ARGON2_TIME_COST,
        memory_cost=config.ARGON2_MEMORY_COST,
        parallelism=config.ARGON2_PARALLELISM,
        hash_len=config.ARGON2_HASH_LEN
    )
    try:
        print(hash, password)
        return ph.verify(hash, password)
    except Exception:
        return False
