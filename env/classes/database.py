import sqlite3

from env.classes.paths import paths
from env.config import config


class SQLiteDatabase:
    def __init__(self) -> None:
        self._conn: sqlite3.Connection = sqlite3.connect(
            database=paths.format(path=config.DATABASE_FILE)
        )
        self._cur: sqlite3.Cursor = self._conn.cursor()

    def insert_user(
        self, user_uuid: str, username: str, description: str, onion_address: str
    ) -> None:
        # TODO: Add missing code!
        raise NotImplementedError("This function is not implemented yet!")

    def commit(self) -> None:
        self._conn.commit()
