import flet as ft  # type:ignore[import-untyped]

from env.classes.router import AppRouter
from env.config import config


class TopBar:
    def __init__(self, router: AppRouter) -> None:
        self._router: AppRouter = router

        # Initialize labels
        # TODO: Clear session data when clicking the text
        self._label: ft.Text = ft.Text(
            value=config.APP_TITLE,
            weight=ft.FontWeight.BOLD,
            size=config.TOP_BAR_LABEL_HEIGHT,
        )

        # Initialize buttons
        self._home_button: ft.IconButton = ft.IconButton(
            icon=ft.Icons.PERSON_OUTLINE,
            height=config.TOP_BAR_HEIGHT,
            icon_size=config.TOP_BAR_HEIGHT - 15,
            on_click=lambda _: self._router.go(route=config.ROUTE_PROFILE),
        )
        self._settings_button: ft.IconButton = ft.IconButton(
            icon=ft.CupertinoIcons.LINE_HORIZONTAL_3,
            height=config.TOP_BAR_HEIGHT,
            icon_size=config.TOP_BAR_HEIGHT - 15,
            on_click=lambda _: self._router.go(route=config.ROUTE_SETTINGS),
        )

        # Initialize containers
        self._home_button_row: ft.Row = ft.Row(
            controls=[self._home_button],
            alignment=ft.MainAxisAlignment.START,
            expand=True,
        )
        self._label_row: ft.Row = ft.Row(
            controls=[self._label],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )
        self._settings_button_row: ft.Row = ft.Row(
            controls=[self._settings_button],
            alignment=ft.MainAxisAlignment.END,
            expand=True,
        )

    def build(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            self._home_button_row,
                            self._label_row,
                            self._settings_button_row,
                        ],
                    ),
                    ft.Divider(height=1, thickness=1),
                ],
            ),
        )
