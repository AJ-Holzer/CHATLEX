from typing import Any

import i18n  # type: ignore[import-untyped]

from env.classes.storages import Storages
from env.config import config


class Translator:
    def __init__(self, storages: Storages) -> None:
        self._storages: Storages = storages

        # Set up i18n
        i18n.load_path.append(config.FOLDER_LANGUAGES)  # type: ignore
        i18n.set(key="filename_format", value="{namespace}.{format}")  # type: ignore
        i18n.set(  # type: ignore
            key="locale",
            value=self._storages.client_storage.get(
                key=config.CS_LANGUAGE, default=config.LANGUAGE_DEFAULT
            ),
        )
        i18n.set(key="available_locales", value=config.LANGUAGE_AVAILABLE_LOCALES)  # type: ignore

    def change_language(self, new_language: str) -> None:
        self._storages.client_storage.set(
            key=config.CS_LANGUAGE,
            value=new_language,
        )

    def t(self, key: str, **kwargs: Any) -> str:
        return i18n.t(key, **kwargs)  # type: ignore

    @property
    def available_locales(self) -> list[str]:
        return i18n.get(key="available_locales")  # type: ignore
