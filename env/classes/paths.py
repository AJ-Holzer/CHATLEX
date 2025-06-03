import os
import platform
import sys

from env.config import config

if platform.system() == "Android":
    from android_storage import app_storage_path  # type:ignore


class Paths:
    def __init__(self) -> None:
        # Define paths
        self._app_storage_path: str

        # Get app storage path
        if sys.platform == "win32":
            self._app_storage_path = os.path.join(
                os.environ.get("APPDATA", os.path.expanduser("~")),
                config.APP_TITLE.upper(),
            )
        elif sys.platform == "linux":
            self._app_storage_path = os.path.join(
                os.path.expanduser("~"), f".{config.APP_TITLE.lower()}"
            )
        elif platform.system() == "Android":
            self._app_storage_path = app_storage_path()
        else:
            self._app_storage_path = os.path.expanduser("~")

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
        if not hasattr(sys, "_MEIPASS"):
            return os.path.abspath("./")

        return sys._MEIPASS  # type:ignore

    @property
    def app_storage_path(self) -> str:
        return self._app_storage_path


paths = Paths()
