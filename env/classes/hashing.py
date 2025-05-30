import re

from argon2 import PasswordHasher
from argon2.low_level import Type, hash_secret_raw

from env.config import config


class ArgonHasher:
    def __init__(self) -> None:
        self.ARGON2_HASH_PATTERN: re.Pattern[str] = re.compile(
            r"^\$argon2(id|i)\$v=\d+\$m=\d+,t=\d+,p=\d+\$.+"
        )

    def _validate_hash(self, hash: str) -> bool:
        return bool(self.ARGON2_HASH_PATTERN.match(string=hash))

    def hash_password(self, password: str) -> str:
        # Check if password exists
        if not password:
            raise ValueError("No password provided!")

        # Initialize hasher
        ph: PasswordHasher = PasswordHasher(
            time_cost=config.ARGON2_TIME_COST,
            memory_cost=config.ARGON2_MEMORY_COST,
            parallelism=config.ARGON2_PARALLELISM,
            hash_len=config.ARGON2_HASH_LEN,
        )
        return ph.hash(password)

    def verify_password(self, hash: str, password: str) -> bool:
        # Check if hash is valid
        if not self._validate_hash(hash=hash):
            print("Hash format invalid or potentially unsafe.")
            return False

        # Initialize hasher
        ph: PasswordHasher = PasswordHasher(
            time_cost=config.ARGON2_TIME_COST,
            memory_cost=config.ARGON2_MEMORY_COST,
            parallelism=config.ARGON2_PARALLELISM,
            hash_len=config.ARGON2_HASH_LEN,
        )

        try:
            return ph.verify(hash=hash, password=password)
        except Exception:
            return False

    def derive_key(self, password: str, salt: bytes) -> bytes:
        return hash_secret_raw(
            secret=password.encode(config.ENCODING),
            salt=salt,
            time_cost=config.ARGON2_TIME_COST,
            memory_cost=config.ARGON2_MEMORY_COST,
            parallelism=config.ARGON2_PARALLELISM,
            hash_len=config.ARGON2_HASH_LEN,
            type=Type.ID,
        )
