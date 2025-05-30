import base64
import json
from pathlib import Path
from typing import Literal, Optional

from nacl.signing import SigningKey, VerifyKey

from env.config import config
from env.typing.encryption import MasterKeys, SignedOnionData


class OnionEncryption:
    def __init__(self) -> None:
        """Initializes an instance of the class.

        Args:
            self(Self): The instance of the class.

        Returns:
            None: No value is returned.

        Raises:
            Exception: Any exception during initialization.
        """
        self._keys: MasterKeys = {
            "private_key": None,
            "public_key": None,
        }

    def _load_key(self, key: Literal["private_key", "public_key"]) -> None:
        file_path: str = (
            config.ENCRYPTION_PRIVATE_KEY_FILE
            if key == "private_key"
            else config.ENCRYPTION_PUBLIC_KEY_FILE
        )
        
        # Check if the file exists
        if not Path(file_path).exists():
            raise FileNotFoundError(f"File '{file_path}' does not exist!")

        # Load the data
        with open(file_path,"r") as file:
            # Load key
            data = base64.b64decode(file.read())
            if key == "private_key":
                self._keys[key] = SigningKey(data)
            else:
                self._keys[key] = VerifyKey(data)

    def _save_key(self, key: Literal["private_key", "public_key"]) -> None:
        # Create a local variable to ensure mypy isn't yelling at me
        actual_key: Optional[SigningKey | VerifyKey] = self._keys[key]

        # Check if key exists
        if actual_key is None:
            raise TypeError(
                f"Key '{key}' does not contain a value. Expected a value; got '{key}' instead. Generate the key first!"
            )

        # Write to file
        with open(
            (
                config.ENCRYPTION_PRIVATE_KEY_FILE
                if key == "private_key"
                else config.ENCRYPTION_PUBLIC_KEY_FILE
            ),
            "w",
        ) as file:
            file.write(base64.b64encode(actual_key.encode()).decode(config.ENCODING))

    def _load_signed_data(self) -> Optional[SignedOnionData]:
        if not Path(config.ENCRYPTION_SINGED_ONION_DATA_FILE).exists():
            return None
        
        with open(config.ENCRYPTION_SINGED_ONION_DATA_FILE, "r") as file:
            return json.load(file)

    def _save_signed_data(self, data: SignedOnionData) -> None:
        with open(config.ENCRYPTION_SINGED_ONION_DATA_FILE, "w") as file:
            json.dump(data, file, indent=2)

    def generate_master_keys(self) -> None:
        # Create a new key
        key: SigningKey = SigningKey.generate()

        # Derive private and public key
        self._keys["private_key"] = key
        self._keys["public_key"] = key.verify_key

        # Save keys
        self.save_master_keys()

    def load_master_keys(self) -> None:
        self._load_key(key="private_key")
        self._load_key(key="public_key")

    def save_master_keys(self) -> None:
        # Check if keys exist
        if self._keys["private_key"] is None:
            raise TypeError("Private key is of type 'None'. Create key first!")
        if self._keys["public_key"] is None:
            raise TypeError("Private key is of type 'None'. Create key first!")

        # Save keys
        self._save_key(key="private_key")
        self._save_key(key="public_key")

    def sign_onion(self, onion_address: str, expiry_days: int) ->

    @property
    def private_key(self) -> SigningKey:
        # Check if private key exists
        if self._keys["private_key"] is None:
            raise TypeError("Private key is of type 'None'. Create key first!")

        return self._keys["private_key"]

    @property
    def public_key(self) -> VerifyKey:
        # Check if public key
        if self._keys["public_key"] is None:
            raise TypeError("Public key is of type 'None'. Create key first!")

        return self._keys["public_key"]
