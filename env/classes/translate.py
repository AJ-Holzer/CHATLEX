from typing import Any

import i18n  # type: ignore[import-untyped]

from env.classes.storages import Storages
from env.config import config


class Translator:
    def __init__(self, storages: Storages) -> None:
        self._storages: Storages = storages

        # Set up i18n
        i18n.load_path.append(config.FOLDER_LANGUAGES)  # type: ignore
        i18n.set("filename_format", "{namespace}.{format}")  # type: ignore
        i18n.set(  # type: ignore
            "locale",
            self._storages.client_storage.get(
                key=config.CS_LANGUAGE, default=config.LANGUAGE_DEFAULT
            ),
        )

    def t(self, key: str, **kwargs: Any) -> None:
        return i18n.t(key, **kwargs)  # type: ignore
