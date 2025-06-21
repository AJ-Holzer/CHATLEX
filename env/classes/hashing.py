import re
from typing import Optional

from argon2 import PasswordHasher
from argon2.low_level import Type, hash_secret_raw
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from env.classes.storages import Storages
from env.config import config
from env.func.generations import generate_salt
from env.typing.hashing import HKDFInfoKey


class ArgonHasher:
    def __init__(self, storages: Storages) -> None:
        self._storages: Storages = storages

        # Get time cost
        self._storage_time_cost: Optional[int] = self._storages.client_storage.get(
            key=config.CS_PASSWORD_HASH_TIME_COST, default=None
        )

        # Check if time cost is defined
        if self._storage_time_cost is None:
            raise ValueError("No time cost provided!")

        # Define time cost
        self._time_cost: int = self._storage_time_cost

        # Create Argon2 hash pattern
        self._ARGON2_HASH_PATTERN: re.Pattern[str] = re.compile(
            r"^\$argon2(id|i)\$v=\d+\$m=\d+,t=\d+,p=\d+\$.+"
        )

    def _validate_hash(self, hash: str) -> bool:
        return bool(self._ARGON2_HASH_PATTERN.match(string=hash))

    def hash_password(self, password: str) -> str:
        # Check if password exists
        if not password:
            raise ValueError("No password provided!")

        # Initialize hasher
        ph: PasswordHasher = PasswordHasher(
            time_cost=self._time_cost,
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
            time_cost=self._time_cost,
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
            time_cost=self._time_cost,
            memory_cost=config.ARGON2_MEMORY_COST,
            parallelism=config.ARGON2_PARALLELISM,
            hash_len=config.ARGON2_HASH_LEN,
            type=Type.ID,
        )


class HKDFHasher:
    def __init__(self, derived_key: bytes) -> None:
        self.derived_key: bytes = derived_key

    def _derive_key(self, info: HKDFInfoKey, salt: Optional[bytes] = None) -> bytes:
        # Generate a new salt if nothing provided
        new_salt: bytes = salt or generate_salt(salt_length=config.SALT_LENGTH)

        hkdf: HKDF = HKDF(
            algorithm=hashes.SHA256(),
            length=config.HKDF_LENGTH,
            salt=new_salt,
            info=info,
        )

        return hkdf.derive(self.derived_key)

    def derive_random_key(self, info: HKDFInfoKey) -> bytes:
        return self._derive_key(
            info=info,
        )

    def derive_key(self, info: HKDFInfoKey, salt: bytes) -> bytes:
        return self._derive_key(info=info, salt=salt)
