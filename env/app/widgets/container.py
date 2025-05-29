from typing import Any

import flet as ft  # type:ignore[import-untyped]

from env.config import config


class MasterContainer(ft.Container):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)  # type:ignore

        # Set default values
        self.padding = ft.padding.only(top=config.APP_PADDING_TOP)
        self.expand = True
