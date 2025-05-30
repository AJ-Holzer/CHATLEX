import base64
import json
import time
from pathlib import Path
from typing import Literal, Optional

from nacl.signing import SigningKey, VerifyKey

from env.config import config
from env.typing.encryption import MasterKeys, SignedOnionData


class AES:
    def __init__(self) -> None:
        pass

    def encrypt(self) -> None:...

    def decrypt(self) -> None:...

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
        self._signed_onion_data: Optional[SignedOnionData] = None

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
        with open(file_path, "r") as file:
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
        if not Path(config.ENCRYPTION_SIGNED_ONION_DATA_FILE).exists():
            return None

        with open(config.ENCRYPTION_SIGNED_ONION_DATA_FILE, "r") as file:
            return json.load(file)

    def _save_signed_data(self) -> None:
        with open(config.ENCRYPTION_SIGNED_ONION_DATA_FILE, "w") as file:
            json.dump(self._signed_onion_data, file, indent=2)

    def _save_master_keys(self) -> None:
        # Check if keys exist
        if self._keys["private_key"] is None:
            raise TypeError("Private key is of type 'None'. Create key first!")
        if self._keys["public_key"] is None:
            raise TypeError("Private key is of type 'None'. Create key first!")

        # Save keys
        self._save_key(key="private_key")
        self._save_key(key="public_key")

    def generate_master_keys(self) -> None:
        # Create a new key
        key: SigningKey = SigningKey.generate()

        # Derive private and public key
        self._keys["private_key"] = key
        self._keys["public_key"] = key.verify_key

        # Save keys
        self._save_master_keys()

    def load_master_keys(self) -> None:
        self._load_key(key="private_key")
        self._load_key(key="public_key")

    def sign_onion(self, onion_address: str, expiry_days: int) -> None:
        # Check if key exists
        actual_key: Optional[SigningKey] = self._keys["private_key"]
        if actual_key is None:
            raise TypeError(
                "No private key exists. Run 'generate_master_keys()' to generate it!"
            )

        # Define data
        timestamp: float = time.time()
        expires: float = timestamp + expiry_days * 86400
        message: str = f"{onion_address}{timestamp}{expires}"
        sig = actual_key.sign(message=message.encode(config.ENCODING)).signature

        self._signed_onion_data = {
            "onion": onion_address,
            "timestamp": timestamp,
            "expires": expires,
            "signed_by": base64.b64encode(actual_key.encode()).decode(config.ENCODING),
            "signature": base64.b64encode(sig).decode(config.ENCODING),
        }

        # Save signed data
        self._save_signed_data()

    def id_is_valid(self, json_path: str) -> bool:
        with open(json_path, "r") as file:
            data: SignedOnionData = json.load(file)

        # Check if time expired
        if time.time() > data["expires"]:
            print("❌ ID has expired!")
            return False

        # Get data
        message: bytes = f"{data["onion"]}{data["timestamp"]}{data["expires"]}".encode(config.ENCODING)
        signature: bytes = base64.b64decode(data["signature"])
        pubkey: bytes = base64.b64decode(data["signed_by"])

        # Check if valid
        try:
            verify_key: VerifyKey = VerifyKey(pubkey)
            verify_key.verify(smessage=message, signature=signature)
            print("✅ Signature is valid!")
            return True
        except Exception as _:
            print("❌ Signature is invalid!")
            return False

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

    @property
    def signed_onion_data(self) -> SignedOnionData:
        if self._signed_onion_data is None:
            raise TypeError(
                "No signed onion data found. Run the 'sign_onion()' function to sign!"
            )

        return self._signed_onion_data
