from typing import Any

import flet as ft  # type:ignore[import-untyped]
from flet.core.client_storage import ClientStorage  # type:ignore[import-untyped]
from flet.core.session_storage import SessionStorage  # type:ignore[import-untyped]


class StorageManager:
    def __init__(self, storage: SessionStorage | ClientStorage) -> None:
        """Initialize a new SessionManager instance.

        Args:
            self(SessionManager): The SessionManager instance.
            storage(SessionStorage | ClientStorage): The storage backend to use.

        Returns:
            None: No return value.

        Raises:
            TypeError: Raised if the storage argument is not a SessionStorage or ClientStorage instance.
        """
        self._storage: SessionStorage | ClientStorage = storage

        # Create storage cache for faster access
        self._storage_cache: dict[str, Any] = {}

        # Load saved storage into cache for faster access
        self._load_all()

        print(f"Storage (type='{type(self._storage)}'): cache={self._storage_cache}")

    def _load_all(self) -> None:
        """Loads all key-value pairs from storage into the cache."""
        if isinstance(self._storage, ClientStorage):
            for key in self._storage.get_keys(key_prefix=""):
                self._storage_cache[key] = self._storage.get(key)

        else:
            for key in self._storage.get_keys():
                self._storage_cache[key] = self._storage.get(key=key)

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieves a value from the internal storage using the given key.

        Args:
            key(str): Key to retrieve the value for.

        Returns:
            Any: The value associated with the key, or None if the key is not found.

        Raises:
            KeyError: If the key is not found in the internal storage (though this is handled internally and returns None).
        """
        # Try to return value from storage cache
        if key in self._storage_cache:
            return self._storage_cache[key]

        # Try to return value from storage
        if not self._storage.contains_key(key=key):
            return default

        # Return default
        return self._storage.get(key=key)

    def set(self, key: str, value: Any) -> None:
        """Sets a key-value pair in the internal storage.

        Args:
            key(str): Key to set.
            value(Any): Value to associate with the key.

        Returns:
            None: No return value.

        Raises:
            Exception: If the underlying storage mechanism encounters an error.
        """
        # Set storage and storage cache
        self._storage.set(key=key, value=value)
        self._storage_cache[key] = value

    def clear(self) -> None:
        self._storage.clear()


class Storages:
    def __init__(self, page: ft.Page) -> None:
        """Initializes a new instance of the class.

        Args:
            self(Self): The instance of the class.
            page(ft.Page): The page object.

        Returns:
            None: No return value.

        Raises:
            Exception: Generic exception during initialization.
        """
        self._page: ft.Page = page
        self._session_storage: StorageManager = StorageManager(
            storage=self._page.session
        )
        self._client_storage: StorageManager = StorageManager(
            storage=self._page.client_storage
        )

    @property
    def session_storage(self) -> StorageManager:
        """Retrieves the current session storage manager.

        Args:
            self(Session): The session object.

        Returns:
            StorageManager: The session storage manager.

        Raises:
            Exception: If the session storage manager is not available.
        """
        return self._session_storage

    @property
    def client_storage(self) -> StorageManager:
        """Returns the client storage manager.

        Args:
            self(Client): The client object.

        Returns:
            StorageManager: The client storage manager.

        Raises:
            Exception: If the client storage manager is not available.
        """
        return self._client_storage
