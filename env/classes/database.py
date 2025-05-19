import sqlite3

import flet as ft  # type:ignore[import-untyped]

# Class
from env.classes.widgets import CText

# Config
from env.config import config

# Func
from env.func.get_session_key import get_key_or_default


class SQL:
    def __init__(self, page: ft.Page, sql_path: str) -> None:
        self._page: ft.Page = page

        # Check if sql path exists, otherwise show push message to lead to the settings page
        if not get_key_or_default(
            page=self._page, default=None, key_name=config.CS_SQL_PATH
        ):
            self._page.open(
                ft.SnackBar(
                    CText(
                        page=self._page,
                        value="Consider to create a database to store your messages.",
                    ),
                    duration=3000,
                )
            )
            return

        self._conn: sqlite3.Connection = sqlite3.connect(str(config.SQL_PATH))
        self._cur: sqlite3.Cursor = self._conn.cursor()
