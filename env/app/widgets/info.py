from typing import Optional

import flet as ft  # type: ignore[import-untyped]

from env.func.text_parser import parse_custom_markdown


class InfoAlert:
    def __init__(
        self,
        title: Optional[str],
        content: Optional[str],
    ) -> None:
        self._title: Optional[str] = title
        self._content: Optional[str] = content

    def build(self) -> ft.AlertDialog:
        return ft.AlertDialog(
            title=ft.Text(value=self._title, text_align=ft.TextAlign.CENTER),
            scrollable=True,
            content=ft.Container(
                content=(
                    ft.Column(
                        controls=[
                            parse_custom_markdown(input_str=self._content),
                        ],
                        scroll=ft.ScrollMode.AUTO,
                    )
                    if self._content is not None
                    else None
                ),
            ),
        )
