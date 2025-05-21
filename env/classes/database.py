import base64
import sqlite3

import flet as ft  # type:ignore[import-untyped]

# Config
from env.config import config

# Func
from env.func.get_session_key import get_key_or_default
from env.func.security import aes_decrypt, aes_encrypt


class SQL:
    """SQL database interaction class. Manages connection, table creation, and data manipulation for users, messages, and devices.

    Attributes:
        _page(ft.Page): Page object associated with the database.
        _db_path(str): Path to the SQLite database file.
        _conn(sqlite3.Connection): SQLite database connection object.
        _cur(sqlite3.Cursor): SQLite database cursor object.
    """

    def __init__(self, page: ft.Page, key: bytes, iv: bytes) -> None:
        self._page: ft.Page = page
        self._key: bytes = key
        self._iv: bytes = iv

        self._db_path: str = get_key_or_default(
            page=self._page, default=config.SQL_PATH, key_name=config.CS_SQL_PATH
        )

        self._conn: sqlite3.Connection = sqlite3.connect(str(config.SQL_PATH))
        self._cur: sqlite3.Cursor = self._conn.cursor()

        # Create tables if they do not exist
        self._cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
            user_uid TEXT PRIMARY KEY,
            username TEXT NOT NULL,
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
            timestamp REAL NOT NULL,
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

    def insert_user(self, user_uid: str, username: str, ip: str) -> None:
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
            "INSERT OR IGNORE INTO users (user_uid, username, ip) VALUES (?, ?, ?)",
            (user_uid, username, ip),
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
            (user_uid, message, timestamp),
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
            (ip, name),
        )
        self._conn.commit()

    def retrieve_users(self, user_uid: str) -> list[dict[str, str]]:
        """Retrieves user information from the database based on the provided user UID.

        Args:
            self(Database): Instance of the Database class.
            user_uid(str): The unique identifier of the user to retrieve.

        Returns:
            list[dict[str, str]]: A list of dictionaries, where each dictionary contains user information (user_uid, username, ip). Returns an empty list if no user is found.

        Raises:
            sqlite3.OperationalError: Raised if there is an error while executing the SQL query.
            TypeError: Raised if the input user_uid is not a string.
        """
        data: list[tuple[str, str, str]] = self._cur.execute(
            "SELECT * FROM users WHERE user_uid = ?", (user_uid,)
        ).fetchall()

        return [
            {
                "user_uid": str(user[0]),
                "username": str(user[1]),
                "ip": str(user[2]),
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
        data: list[tuple[int, str, str, float]] = self._cur.execute(
            "SELECT * FROM messages WHERE user_uid = ?", (user_uid,)
        ).fetchall()

        return [
            {
                "id": str(msg[0]),
                "user_uid": str(msg[1]),
                "message": str(msg[2]),
                "timestamp": str(msg[3]),
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
                "ip": str(device[0]),
                "name": str(device[1]),
            }
            for device in data
        ]

    def encrypt_data(self, data: str) -> str:
        encrypted: bytes = aes_encrypt(
            plaintext=data,
            key=self._key,
            iv=self._iv,
        )
        return base64.b64encode(encrypted).decode("UTF-8")

    def decrypt_data(self, data: str) -> str:
        decrypted: bytes = aes_decrypt(
            ciphertext=base64.b64decode(data),
            key=self._key,
            iv=self._iv,
        )
        return decrypted.decode("UTF-8")
