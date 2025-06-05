import sqlite3
from typing import Optional

from env.classes.encryption import AES
from env.classes.paths import paths
from env.config import config
from env.func.converter import byte_to_str, str_to_byte
from env.typing.dicts import ContactData, DeviceData, MessageData
from env.typing.hashing import HKDFInfoKey


class SQLiteDatabase:
    def __init__(self, aes_encryptor: AES) -> None:
        self._db_path: str = paths.join_with_app_storage(path=config.DATABASE_FILE)

        # Initialize sql connection and cursor
        self._conn: sqlite3.Connection = sqlite3.connect(database=self._db_path)
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

    def _encrypt(self, data: str, encryption_key_info: HKDFInfoKey) -> str:
        if not data:
            return ""

        return byte_to_str(
            data=self._encryptor.encrypt(
                plaintext=data,
                encryption_key_info=encryption_key_info,
            )
        )

    def _decrypt(self, data: str, encryption_key_info: HKDFInfoKey) -> str:
        if not data:
            return ""

        return self._encryptor.decrypt(
            encrypted_data=str_to_byte(data=data),
            encryption_key_info=encryption_key_info,
        )

    def insert_contact(self, contact_data: ContactData) -> None:
        # Insert data (encrypted)
        self._cur.execute(
            "INSERT INTO contacts (contact_uuid, username, description, onion_address) VALUES (?, ?, ?, ?)",
            (
                contact_data[
                    "contact_uuid"
                ],  # Leave uuid decrypted to be able to find it
                self._encrypt(
                    data=contact_data["username"],
                    encryption_key_info=config.HKDF_INFO_CONTACT,
                ),
                self._encrypt(
                    data=contact_data["description"],
                    encryption_key_info=config.HKDF_INFO_CONTACT,
                ),
                self._encrypt(
                    data=contact_data["onion_address"],
                    encryption_key_info=config.HKDF_INFO_CONTACT,
                ),
            ),
        )

        self.commit()

    def insert_message(self, contact_uuid: str, message: str, timestamp: float) -> None:
        try:
            self._cur.execute(
                "INSERT INTO messages (contact_uuid, message, timestamp) VALUES (?, ?, ?)",
                (
                    contact_uuid,  # Leave uuid decrypted to be able to find it
                    self._encrypt(
                        data=message,
                        encryption_key_info=config.HKDF_INFO_MESSAGE,
                    ),
                    self._encrypt(
                        data=str(timestamp),
                        encryption_key_info=config.HKDF_INFO_MESSAGE,
                    ),
                ),
            )
            self.commit()
        except Exception as e:
            print(
                f"Exception has occurred while inserting message for contact_uuid={contact_uuid}: {e}"
            )

    def insert_device(self, device_uuid: str, onion_address: str, name: str) -> None:
        try:
            self._cur.execute(
                "INSERT INTO devices (device_uuid, onion_address, name) VALUES (?, ?, ?)",
                (
                    device_uuid,  # Leave uuid decrypted to be able to find it
                    self._encrypt(
                        data=onion_address,
                        encryption_key_info=config.HKDF_INFO_DEVICE,
                    ),
                    self._encrypt(
                        data=name,
                        encryption_key_info=config.HKDF_INFO_DEVICE,
                    ),
                ),
            )

            self.commit()
        except Exception as e:
            print(
                f"Exception has occurred while inserting message for contact_uuid={device_uuid}: {e}"
            )

    def retrieve_contacts(self) -> Optional[list[ContactData]]:
        # Select contacts
        rows: list[tuple[str, str, str, str]] = self._cur.execute(
            "SELECT contact_uuid, username, description, onion_address FROM contacts"
        ).fetchall()

        contacts: list[ContactData] = []

        for (
            uuid,
            encrypted_username,
            encrypted_description,
            encrypted_onion_address,
        ) in rows:
            contacts.append(
                {
                    "contact_uuid": uuid,
                    "username": self._decrypt(
                        data=encrypted_username,
                        encryption_key_info=config.HKDF_INFO_CONTACT,
                    ),
                    "description": self._decrypt(
                        data=encrypted_description,
                        encryption_key_info=config.HKDF_INFO_CONTACT,
                    ),
                    "onion_address": self._decrypt(
                        data=encrypted_onion_address,
                        encryption_key_info=config.HKDF_INFO_CONTACT,
                    ),
                }
            )
        return contacts

    def retrieve_messages(self, contact_uuid: str) -> Optional[list[MessageData]]:
        try:
            # Select messages
            rows: list[tuple[str, str, str]] = self._cur.execute(
                "SELECT id, message, timestamp FROM messages WHERE contact_uuid = ? ORDER BY timestamp ASC",
                (contact_uuid,),
            ).fetchall()

            messages: list[MessageData] = []
            for message_id, encrypted_message, encrypted_timestamp in rows:
                messages.append(
                    {
                        "id": message_id,
                        "contact_uuid": contact_uuid,
                        "message": self._decrypt(
                            data=encrypted_message,
                            encryption_key_info=config.HKDF_INFO_MESSAGE,
                        ),
                        "timestamp": float(
                            self._decrypt(
                                data=encrypted_timestamp,
                                encryption_key_info=config.HKDF_INFO_MESSAGE,
                            )
                        ),
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

            for device_uuid, encrypted_onion_address, encrypted_name in rows:
                devices.append(
                    {
                        "uuid": device_uuid,
                        "onion_address": self._decrypt(
                            data=encrypted_onion_address,
                            encryption_key_info=config.HKDF_INFO_DEVICE,
                        ),
                        "name": self._decrypt(
                            data=encrypted_name,
                            encryption_key_info=config.HKDF_INFO_DEVICE,
                        ),
                    },
                )

            return devices
        except Exception as e:
            print(f"Could not retrieve devices. Error: {e}")
            return None

    def update_contact(self, contact_uuid: str, contact_data: ContactData) -> None:
        """
        Update an existing contact's information.
        """
        self._cur.execute(
            """
            UPDATE contacts
            SET username = ?, description = ?, onion_address = ?
            WHERE contact_uuid = ?
            """,
            (
                self._encrypt(
                    data=contact_data["username"],
                    encryption_key_info=config.HKDF_INFO_CONTACT,
                ),
                self._encrypt(
                    data=contact_data["description"],
                    encryption_key_info=config.HKDF_INFO_CONTACT,
                ),
                self._encrypt(
                    data=contact_data["onion_address"],
                    encryption_key_info=config.HKDF_INFO_CONTACT,
                ),
                contact_uuid,
            ),
        )
        self.commit()

    def update_device(self, device_uuid: str, device_data: DeviceData) -> None:
        """
        Update an existing contact's information.
        """
        self._cur.execute(
            """
            UPDATE devices
            SET name = ?, onion_address = ?
            WHERE device_uuid = ?
            """,
            (
                self._encrypt(
                    data=device_data["name"],
                    encryption_key_info=config.HKDF_INFO_CONTACT,
                ),
                self._encrypt(
                    data=device_data["onion_address"],
                    encryption_key_info=config.HKDF_INFO_CONTACT,
                ),
                device_uuid,
            ),
        )
        self.commit()

    def delete_contact(self, contact_uuid: str) -> None:
        """
        Delete a contact and all associated messages from the database.
        """
        # Delete messages associated with the contact
        self._cur.execute(
            "DELETE FROM messages WHERE contact_uuid = ?", (contact_uuid,)
        )
        # Delete the contact itself
        self._cur.execute(
            "DELETE FROM contacts WHERE contact_uuid = ?", (contact_uuid,)
        )
        self.commit()

    def delete_message(self, message_id: str) -> None:
        self._cur.execute("DELETE FROM messages WHERE id = ?", (message_id,))
        self.commit()

    def delete_device(self, device_uuid: str) -> None:
        self._cur.execute("DELETE FROM devices WHERE device_uuid = ?", (device_uuid,))
        self.commit()

    def commit(self) -> None:
        self._conn.commit()
