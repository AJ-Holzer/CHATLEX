from typing import Optional

import flet as ft  # type:ignore[import-untyped]

from env.app.widgets.buttons_and_toggles import SectionButton


class InfoButtonAlert:
    def __init__(
        self,
        page: ft.Page,
        label: str,
        content: str,
        icon: Optional[ft.IconValue] = None,
    ) -> None:
        self._page: ft.Page = page
        self._label: str = label
        self._content: str = content
        self._icon: Optional[ft.IconValue] = icon

        # Create info alert
        self._info_alert: ft.AlertDialog = ft.AlertDialog(
            title=self._label,
            scrollable=True,
            content=ft.Markdown(value=self._content),
        )

        # Create button to open alert
        self._info_button: SectionButton = SectionButton(
            text=self._label,
            icon=self._icon,
            func=self._page.open,
            func_args=(self._info_alert,),
        )

    def build(self) -> ft.Container:
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            self._info_button.build(),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        expand=True,
                    ),
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            expand=True,
        )
