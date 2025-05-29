from typing import Any

import flet as ft  # type:ignore[import-untyped]

from env.config import config


class MasterContainer(ft.Container):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)  # type:ignore

        # Set default values
        self.padding = ft.Padding(
            top=config.APP_PADDING_TOP,
            right=config.APP_PADDING_RIGHT,
            bottom=config.APP_PADDING_BOTTOM,
            left=config.APP_PADDING_LEFT,
        )
        self.expand = True
