import os
import platform
import sys

if platform.system() == "Android":
    from android_storage import app_storage_path  # type:ignore


class Paths:
    def __init__(self) -> None:
        # Define types
        self._app_storage_path: str

        # Get app storage path
        if sys.platform == "win32":
            self._app_storage_path = os.path.join(
                os.environ.get("APPDATA", os.path.expanduser("~")), "ChatLex"
            )
        elif sys.platform == "linux":
            self._app_storage_path = os.path.join(os.path.expanduser("~"), ".chatlex")
        elif platform.system() == "Android":
            self._app_storage_path = app_storage_path()
        else:
            self._app_storage_path = os.path.expanduser("~")

    @property
    def app_storage(self) -> str:
        return self._app_storage_path


paths = Paths()
