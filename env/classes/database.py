import sqlite3

import flet as ft  # type:ignore[import-untyped]

# Config
from env.config import config

# Func
from env.func.get_session_key import get_key_or_default
from env.func.security import aes_encrypt, aes_decrypt


class SQL:
    def __init__(self, page: ft.Page) -> None:
        self._page: ft.Page = page
        self._db_path: str = get_key_or_default(page=self._page, default=config.SQL_PATH, key_name=config.CS_SQL_PATH)

        self._conn: sqlite3.Connection = sqlite3.connect(str(config.SQL_PATH))
        self._cur: sqlite3.Cursor = self._conn.cursor()

    def insert_user(self, user_uid: str, username: str, ip: str) -> None:
        raise NotImplementedError("This function is not implemented yet!")

    def insert_message(self, user_uid: str, message: str, timestamp: float) -> None:
        raise NotImplementedError("This function is not implemented yet!")

    def insert_device(self, ip: str, name: str) -> None:  # TODO: Add the comment ;)
        raise NotImplementedError("This function is not implemented yet!")

    def retrieve_user(self, user_uid: str) -> None:
        raise NotImplementedError("This function is not implemented yet!")
