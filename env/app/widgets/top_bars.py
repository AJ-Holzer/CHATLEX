import flet as ft  # type:ignore[import-untyped]

from env.classes.router import AppRouter
from env.classes.storages import Storages
from env.config import config
from env.func.logout import logout_on_lost_focus


class TopBar:
    def __init__(self, page: ft.Page, router: AppRouter, storages: Storages) -> None:
        self._page: ft.Page = page
        self._router: AppRouter = router
        self._storages: Storages = storages

        # Initialize labels
        self._label: ft.Text = ft.Text(
            value=config.APP_TITLE,
            weight=ft.FontWeight.BOLD,
            size=config.TOP_BAR_LABEL_HEIGHT,
        )

        # Initialize buttons
        self._home_button: ft.IconButton = ft.IconButton(
            icon=ft.Icons.PERSON_OUTLINE,
            tooltip="Profile",
            height=config.TOP_BAR_HEIGHT,
            icon_size=config.TOP_BAR_HEIGHT - 15,
            on_click=lambda _: self._router.go(route=config.ROUTE_PROFILE),
        )
        self._settings_button: ft.IconButton = ft.IconButton(
            icon=ft.CupertinoIcons.LINE_HORIZONTAL_3,
            tooltip="Settings",
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
            controls=[
                ft.Container(
                    content=self._label,
                    on_click=lambda _: logout_on_lost_focus(
                        e=None,
                        router=self._router,
                        storages=self._storages,
                        force=True,
                    ),
                ),
            ],
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


class SubPageTopBar:
    def __init__(
        self, page: ft.Page, router: AppRouter, storages: Storages, title: str
    ) -> None:
        self._page: ft.Page = page
        self._router: AppRouter = router
        self._storages: Storages = storages
        self._title: str = title

        # Initialize labels
        self._label: ft.Text = ft.Text(
            value=self._title,
            weight=ft.FontWeight.BOLD,
            size=config.TOP_BAR_LABEL_HEIGHT,
            text_align=ft.TextAlign.CENTER,
            expand=True,
        )

        # Initialize buttons
        self._back_button: ft.IconButton = ft.IconButton(
            icon=ft.Icons.ARROW_BACK_IOS_ROUNDED,
            tooltip="Back",
            height=config.TOP_BAR_HEIGHT,
            icon_size=config.TOP_BAR_HEIGHT - 15,
            on_click=lambda _: self._router.pop(),
        )

        # Initialize containers
        self._back_button_row: ft.Row = ft.Row(
            controls=[self._back_button],
            alignment=ft.MainAxisAlignment.START,
            expand=True,
        )
        self._label_row: ft.Row = ft.Row(
            controls=[
                ft.Container(
                    content=self._label,
                    on_click=lambda _: logout_on_lost_focus(
                        e=None,
                        router=self._router,
                        storages=self._storages,
                        force=True,
                    ),
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )

        # ADD EMPTY RIGHT COLUMN to balance layout
        self._spacer_row: ft.Row = ft.Row(
            controls=[],  # intentionally empty
            alignment=ft.MainAxisAlignment.END,
            expand=True,
        )

    def build(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            self._back_button_row,
                            self._label_row,
                            self._spacer_row,
                        ],
                    ),
                    ft.Divider(height=1, thickness=1),
                ],
            ),
        )
