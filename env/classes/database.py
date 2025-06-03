import sqlite3
from typing import Optional

from env.classes.encryption import AES
from env.classes.paths import paths
from env.config import config
from env.func.converter import byte_to_str, str_to_byte
from env.typing.dicts import ContactData, DeviceData, MessageData


class SQLiteDatabase:
    def __init__(self, aes_encryptor: AES) -> None:
        # Initialize sql connection and cursor
        self._conn: sqlite3.Connection = sqlite3.connect(
            database=paths.join_with_app_storage(path=config.DATABASE_FILE)
        )
        self._cur: sqlite3.Cursor = self._conn.cursor()

        # Initialize AES encryptor
        self._encryptor: AES = aes_encryptor

        # Create tables if they don't exist
        self._crate_tables()

    def _crate_tables(self) -> None:
        # Contact table
        self._cur.execute(
            """
            CREATE TABLE IF NOT EXISTS contacts (
            contact_uuid TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            description TEXT,
            onion_address TEXT NOT NULL
            )
        """
        )
        # Message table
        self._cur.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contact_uuid TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY(contact_uuid) REFERENCES contacts(contact_uuid)
            )
        """
        )
        # Device table
        self._cur.execute(
            """
            CREATE TABLE IF NOT EXISTS devices (
                device_uuid TEXT PRIMARY KEY,
                onion_address TEXT NOT NULL,
                name TEXT NOT NULL
            )
        """
        )

        self.commit()

    def _encrypt(self, data: str) -> str:
        if not data:
            raise ValueError(f"Data has to contain a value, got '{data}' instead!")

        # TODO: Use random IVs for every entry and store the IV along the encrypted data to be able to decrypt it again. ChatGPT said I should use AES-GCM or AES-CBC with random IVs
        return byte_to_str(data=self._encryptor.encrypt(plaintext=data))

    def _decrypt(self, data: str) -> str:
        if not data:
            raise ValueError(f"Data has to contain a value, got '{data}' instead!")

        # TODO: Update the function accordingly to the encrypt function
        return self._encryptor.decrypt(ciphertext=str_to_byte(data=data))

    def insert_contact(
        self, contact_uuid: str, username: str, description: str, onion_address: str
    ) -> None:
        try:
            # Insert data (encrypted)
            self._cur.execute(
                "INSERT INTO contacts (contact_uuid, username, description, ip) VALUES (?, ?, ?, ?)",
                (
                    self._encrypt(data=contact_uuid),
                    self._encrypt(data=username),
                    self._encrypt(data=description),
                    self._encrypt(data=onion_address),
                ),
            )
        except Exception as e:
            print(
                f"Exception has occurred while inserting contact with uuid={contact_uuid}: {e}"
            )

    def insert_message(self, contact_uuid: str, message: str, timestamp: float) -> None:
        try:
            self._cur.execute(
                "INSERT INTO messages (contact_uuid, message, timestamp) VALUES (?, ?, ?)",
                (
                    self._encrypt(data=contact_uuid),  # TODO: Don't encrypt primary key
                    self._encrypt(data=message),
                    self._encrypt(data=str(timestamp)),
                ),
            )
        except Exception as e:
            print(
                f"Exception has occurred while inserting message for contact_uuid={contact_uuid}: {e}"
            )

    def insert_device(self, device_uuid: str, onion_address: str, name: str) -> None:
        try:
            self._cur.execute(
                "INSERT INTO devices (device_uuid, onion_address, name) VALUES (?, ?, ?)",
                (
                    self._encrypt(data=device_uuid),  # TODO: Don't encrypt primary key
                    self._encrypt(data=onion_address),
                    self._encrypt(data=name),
                ),
            )
        except Exception as e:
            print(
                f"Exception has occurred while inserting message for contact_uuid={device_uuid}: {e}"
            )

    def retrieve_contact(self, contact_uuid: str) -> Optional[ContactData]:
        try:
            # Encrypt uuid to find it in the database
            encrypted_uuid: str = self._encrypt(data=contact_uuid)

            # Select contact
            encrypted_username, encrypted_description, encrypted_onion_address = (
                self._cur.execute(
                    "SELECT username, description, onion_address FROM contacts WHERE contact_uuid = ?",
                    (encrypted_uuid,),  # TODO: Don't encrypt primary key
                ).fetchone()
            )

            return {
                "contact_uuid": contact_uuid,
                "username": self._decrypt(data=encrypted_username),
                "description": self._decrypt(data=encrypted_description),
                "onion_address": self._decrypt(data=encrypted_onion_address),
            }
        except Exception as e:
            print(f"Could not retrieve contact with uuid='{contact_uuid}'. Error: {e}")
            return None

    def retrieve_messages(self, contact_uuid: str) -> Optional[list[MessageData]]:
        try:
            # Encrypt uuid to find it in the database
            encrypted_uuid: str = self._encrypt(data=contact_uuid)

            # Select messages
            rows: list[tuple[str, str, str]] = self._cur.execute(
                "SELECT id, message, timestamp FROM messages WHERE contact_uuid = ? ORDER BY timestamp ASC",
                (encrypted_uuid,),
            ).fetchall()

            messages: list[MessageData] = []
            for message_id, encrypted_message, encrypted_timestamp in rows:
                messages.append(
                    {
                        "id": message_id,  # TODO: Don't encrypt primary key
                        "contact_uuid": contact_uuid,  # TODO: Don't encrypt uuid key
                        "message": self._decrypt(data=encrypted_message),
                        "timestamp": float(self._decrypt(data=encrypted_timestamp)),
                    }
                )

            return messages
        except Exception as e:
            print(f"Could not retrieve messages with uuid='{contact_uuid}'. Error: {e}")
            return None

    def retrieve_devices(self) -> Optional[list[DeviceData]]:
        try:
            rows: list[tuple[str, str, str]] = self._cur.execute(
                "SELECT device_uuid, onion_address, name FROM devices"
            ).fetchall()

            devices: list[DeviceData] = []

            for encrypted_device_uuid, encrypted_onion_address, encrypted_name in rows:
                devices.append(
                    {
                        "uuid": self._decrypt(
                            data=encrypted_device_uuid
                        ),  # TODO: Don't encrypt primary key
                        "onion_address": self._decrypt(data=encrypted_onion_address),
                        "name": self._decrypt(data=encrypted_name),
                    },
                )

            return devices
        except Exception as e:
            print(f"Could not retrieve devices. Error: {e}")
            return None

    # TODO: Add functions to update users and devices

    def commit(self) -> None:
        self._conn.commit()
