import base64
import os
import sqlite3
from typing import Optional

import flet as ft  # type:ignore[import-untyped]

from env.config import config
from env.func.get_session_key import get_key_or_default
from env.func.security import aes_decrypt, aes_encrypt, str_to_byte
from env.typing.types import ContactType


class DatabaseHandler:
    """DatabaseHandler interaction class. Manages connection, table creation, and data manipulation for users, messages, and devices.

    Attributes:
        _page(ft.Page): Page object associated with the database.
        _db_path(str): Path to the SQLite database file.
        _conn(sqlite3.Connection): SQLite database connection object.
        _cur(sqlite3.Cursor): SQLite database cursor object.
    """

    def __init__(self, page: ft.Page) -> None:
        self._page: ft.Page = page
        self._key: Optional[bytes] = self._page.session.get(config.SS_SESSION_KEY)
        self._iv: bytes = str_to_byte(
            data=str(self._page.client_storage.get(config.CS_PASSWORD_IV))
        )

        # Check if key and iv exist
        if not self._key or not self._iv:
            raise ValueError("Key and IV must be provided for encryption/decryption.")

        self._db_path: str = get_key_or_default(
            page=self._page, default=config.SQL_PATH, key_name=config.CS_SQL_PATH
        )

        # # TODO: Remove this line. It is only for testing purposes.
        # path_alert: ft.AlertDialog = ft.AlertDialog(
        #     title=ft.Text("Database initialized!"),
        #     content=ft.Text(f"Path: {self._db_path}"),
        #     actions=[
        #         ft.TextButton("OK", on_click=lambda _: self._page.close(path_alert))
        #     ],
        # )
        # self._page.open(path_alert)

        # Create db path if it does not exist
        os.makedirs(os.path.dirname(self._db_path), exist_ok=True)

        print(f"Using database path: {self._db_path}")
        self._conn: sqlite3.Connection = sqlite3.connect(
            self._db_path,
            check_same_thread=False,  # TODO: Try to avoid using this in production
        )
        self._cur: sqlite3.Cursor = self._conn.cursor()

        # Create tables if they do not exist
        self._cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
            user_uid TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            description TEXT,
            ip TEXT NOT NULL
            )
        """
        )
        self._cur.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_uid TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY(user_uid) REFERENCES users(user_uid)
            )
        """
        )
        self._cur.execute(
            """
            CREATE TABLE IF NOT EXISTS devices (
            ip TEXT PRIMARY KEY,
            name TEXT NOT NULL
            )
        """
        )
        self._conn.commit()

        print(f"Created database at '{self._db_path}'.")

    def insert_user(
        self, user_uid: str, username: str, description: str, ip: str
    ) -> None:
        """Insert a new user into the database if one with the same user_uid does not already exist.

        Args:
            self(Database): Database instance.
            user_uid(str): Unique identifier for the user.
            username(str): Username of the user.
            ip(str): IP address of the user.

        Returns:
            None: No return value.

        Raises:
            sqlite3.IntegrityError: Raised if there is a constraint violation, such as trying to insert a duplicate user_uid.
            sqlite3.OperationalError: Raised if there is an error during database operation.
        """
        self._cur.execute(
            "INSERT OR IGNORE INTO users (user_uid, username, description, ip) VALUES (?, ?, ?, ?)",
            (
                self._encrypt_data(user_uid),
                self._encrypt_data(username),
                self._encrypt_data(description),
                self._encrypt_data(ip),
            ),
        )
        self._conn.commit()

    def insert_message(self, user_uid: str, message: str, timestamp: float) -> None:
        """Insert a new message into the database.  If a message with the same user_uid and timestamp already exists, it will be ignored.

        Args:
            self(Database): Database instance.
            user_uid(str): Unique identifier of the user sending the message.
            message(str): The message content.
            timestamp(float): Timestamp indicating when the message was sent.

        Returns:
            None: No return value.

        Raises:
            sqlite3.IntegrityError: Raised if there is a database integrity issue during insertion.
            sqlite3.OperationalError: Raised if there is an operational error during database interaction.
        """
        self._cur.execute(
            "INSERT OR IGNORE INTO messages (user_uid, message, timestamp) VALUES (?, ?, ?)",
            (
                self._encrypt_data(user_uid),
                self._encrypt_data(message),
                self._encrypt_data(str(timestamp)),
            ),
        )
        self._conn.commit()

    def insert_device(self, ip: str, name: str) -> None:
        """Insert a new device into the devices table. If a device with the same IP address already exists, it will be ignored.

        Args:
            self(Database): Database instance.
            ip(str): IP address of the device.
            name(str): Name of the device.

        Returns:
            None: No return value.

        Raises:
            sqlite3.IntegrityError: Raised if there is a problem committing the transaction to the database.
            sqlite3.OperationalError: Raised if there is a problem executing the SQL query.
        """
        self._cur.execute(
            "INSERT OR IGNORE INTO devices (ip, name) VALUES (?, ?)",
            (self._encrypt_data(data=ip), self._encrypt_data(name)),
        )
        self._conn.commit()

    def retrieve_contacts(self) -> list[ContactType]:
        """Retrieves all contact information from the database.

        Args:
            self(DatabaseConnector): Instance of the DatabaseConnector class.

        Returns:
            list[dict]: List of dictionaries, where each dictionary represents a contact with keys: "user_uid", "username", "description", and "ip".

        Raises:
            Exception: Generic exception during database interaction or data processing.
        """
        data: list[tuple[str, str, str, str]] = self._cur.execute(
            "SELECT user_uid, username, description, ip FROM users"
        ).fetchall()

        return [
            {
                "user_uid": self._decrypt_data(user[0]),
                "username": self._decrypt_data(user[1]),
                "description": self._decrypt_data(user[2]),
                "ip": self._decrypt_data(user[3]),
            }
            for user in data
        ]

    def retrieve_messages(self, user_uid: str) -> list[dict[str, str]]:
        """Retrieves messages for a given user UID.

        Args:
            self(Database): Instance of the Database class.
            user_uid(str): The UID of the user whose messages are to be retrieved.

        Returns:
            list[dict[str, str]]: A list of dictionaries, where each dictionary represents a message with its ID, user UID, message content, and timestamp.

        Raises:
            sqlite3.OperationalError: Raised if there is an error executing the SQL query.
            TypeError: Raised if the user_uid is not a string.
        """
        data: list[tuple[int, str, str, str]] = self._cur.execute(
            "SELECT * FROM messages WHERE user_uid = ?", (user_uid,)
        ).fetchall()

        return [
            {
                "id": self._decrypt_data(str(msg[0])),
                "user_uid": self._decrypt_data(msg[1]),
                "message": self._decrypt_data(msg[2]),
                "timestamp": self._decrypt_data(msg[3]),
            }
            for msg in data
        ]

    def retrieve_devices(self) -> list[dict[str, str]]:
        """Retrieves all devices from the database.

        Args:
            self(DatabaseConnector): Instance of the DatabaseConnector class.

        Returns:
            list[dict[str, str]]: List of dictionaries, where each dictionary represents a device with "ip" and "name" keys.

        Raises:
            sqlite3.Error: If an error occurs during database interaction.
            Exception: For any other unexpected error.
        """
        data: list[tuple[str, str]] = self._cur.execute(
            "SELECT * FROM devices"
        ).fetchall()

        return [
            {
                "ip": self._decrypt_data(device[0]),
                "name": self._decrypt_data(device[1]),
            }
            for device in data
        ]

    def remove_contact(self, user_uid: str) -> None:
        self._cur.execute(
            "DELETE FROM users WHERE user_uid = ?",
            (self._encrypt_data(user_uid),),
        )

    def _encrypt_data(self, data: str) -> str:
        if not self._key or not self._iv:
            raise ValueError("Key and IV must be provided for encryption.")

        encrypted: bytes = aes_encrypt(
            plaintext=data,
            key=self._key,
            iv=self._iv,  # TODO: Check if it really bytes! Raises error somehow
        )
        return base64.b64encode(encrypted).decode("UTF-8")

    def _decrypt_data(self, data: str) -> str:
        if not self._key or not self._iv:
            raise ValueError("Key and IV must be provided for encryption.")

        decrypted: bytes = aes_decrypt(
            ciphertext=base64.b64decode(data),
            key=self._key,
            iv=self._iv,
        )
        return decrypted.decode("UTF-8")

    def close(self) -> None:
        if not self._conn:
            return

        self._conn.close()

    def commit(self) -> None:
        """Commits the current transaction to the database."""
        if not self._conn:
            raise ValueError("Database connection is not established.")

        self._conn.commit()

    def __del__(self) -> None:
        self.close()
