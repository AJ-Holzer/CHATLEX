import sqlite3

from env.classes.paths import paths
from env.config import config


class SQLiteDatabase:
    def __init__(self) -> None:
        self._conn: sqlite3.Connection = sqlite3.connect(
            database=paths.format(path=config.DATABASE_FILE)
        )
        self._cur: sqlite3.Cursor = self._conn.cursor()

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
            ip TEXT NOT NULL
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
            ip TEXT PRIMARY KEY,
            name TEXT NOT NULL
            )
        """
        )

        self.commit()

    def insert_contact(
        self, contact_uuid: str, username: str, description: str, onion_address: str
    ) -> None:
        try:
            # TODO: Encrypt data!
            self._cur.execute(
                "INSERT INTO contacts (contact_uuid, username, description, ip) VALUES (?, ?, ?, ?)",
                (contact_uuid, username, description, onion_address),
            )
        except Exception as e:
            print(
                f"Exception has occurred while inserting contact with uuid={contact_uuid}: {e}"
            )

    def insert_message(self, contact_uuid: str, message: str, timestamp: float) -> None:
        # TODO: Add missing code!
        raise NotImplementedError("This function is not implemented yet!")

    def commit(self) -> None:
        self._conn.commit()
