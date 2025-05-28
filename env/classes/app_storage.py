from typing import Any

import flet as ft  # type:ignore[import-untyped]
from flet.core.client_storage import ClientStorage  # type:ignore[import-untyped]
from flet.core.session_storage import SessionStorage  # type:ignore[import-untyped]


class StorageManager:
    def __init__(self, storage: SessionStorage | ClientStorage) -> None:
        self._storage: SessionStorage | ClientStorage = storage

    def get(self, key: str) -> Any:
        if not self._storage.contains_key(key=key):
            raise ValueError(f"Key '{key}' does not exist in the {"client" if isinstance(self._storage, ClientStorage) else "session"} storage")
        
        return self._storage.get(key=key)

    def set(self, key: str, value: Any) -> None:
        self._storage.set(key=key, value=value)


class Storages:
    def __init__(self, page: ft.Page) -> None:
        self._page: ft.Page = page
        self._session_storage: StorageManager = StorageManager(storage=self._page.session)
        self._client_storage: StorageManager = StorageManager(storage=self._page.client_storage)
        