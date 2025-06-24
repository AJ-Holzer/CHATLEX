from typing import Optional

import flet as ft  # type:ignore[import-untyped]

from env.app.widgets.buttons_and_toggles import ActionButton


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
            title=ft.Text(value=self._label, text_align=ft.TextAlign.CENTER),
            scrollable=True,
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Markdown(value=self._content),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
            ),
        )

        # Create button to open alert
        self._info_button: ActionButton = ActionButton(
            page=self._page,
            text=self._label,
            icon=self._icon,
            on_click=lambda _: self._page.open(self._info_alert),
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
