import os
import sys


class Paths:
    def __init__(self) -> None:
        # Define paths
        self._app_storage_path: str = str(os.getenv("FLET_APP_STORAGE_DATA"))
        self._base_path: str = (
            sys._MEIPASS  # type: ignore
            if hasattr(sys, "_MEIPASS")
            else os.path.abspath("./")
        )

    def _normalize_join_path(self, *paths: str) -> str:
        converted_paths: list[str] = [os.path.normpath(path) for path in paths]
        return os.path.normpath(os.path.join(*converted_paths))

    def join_with_app_storage(self, path: str) -> str:
        """Normalize and join the given path with the application storage path.

        Args:
            path (str): The path to normalize and join.

        Returns:
            str: The normalized and joined path.

        Raises:
            ValueError: If the path is invalid.
            TypeError: If the path is not a string.
        """
        return self._normalize_join_path(self.app_storage_path, path)

    def join_with_base_path(self, path: str) -> str:
        return self._normalize_join_path(self.base_path, path)

    @property
    def base_path(self) -> str:
        return self._base_path

    @property
    def app_storage_path(self) -> str:
        return self._app_storage_path


paths = Paths()
