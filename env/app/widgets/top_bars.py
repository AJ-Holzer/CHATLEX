import flet as ft  # type: ignore[import-untyped]

from env.classes.router import AppRouter
from env.classes.storages import Storages
from env.classes.translate import Translator
from env.config import config
from env.func.logout import logout_on_lost_focus


# Define function for logging out when clicking the label of the top bar
def top_bar_logout_action(storages: Storages, router: AppRouter) -> None:
    if not storages.client_storage.get(
        key=config.CS_LOGOUT_ON_TOP_BAR_LABEL_CLICK,
        default=config.TOP_BAR_LOGOUT_ON_LABEL_CLICK_DEFAULT,
    ):
        return

    logout_on_lost_focus(
        e=None,
        router=router,
        storages=storages,
        force=True,
    )


class TopBar:
    def __init__(
        self,
        page: ft.Page,
        translator: Translator,
        router: AppRouter,
        storages: Storages,
        title: str,
    ) -> None:
        self._page: ft.Page = page
        self._translator: Translator = translator
        self._router: AppRouter = router
        self._storages: Storages = storages
        self._title: str = title

        # Initialize labels
        self._label: ft.Text = ft.Text(
            value=title,
            weight=ft.FontWeight.BOLD,
            theme_style=ft.TextThemeStyle.TITLE_LARGE,
            color=ft.Colors.PRIMARY,
        )

        # Initialize buttons
        self._home_button: ft.IconButton = ft.IconButton(
            icon=ft.Icons.PERSON_OUTLINE,
            tooltip=self._translator.t(key="top_bars.profile_button"),
            height=config.TOP_BAR_HEIGHT,
            icon_size=config.TOP_BAR_HEIGHT - 15,
            on_click=lambda _: self._router.go(route=config.ROUTE_PROFILE),
        )
        self._settings_button: ft.IconButton = ft.IconButton(
            icon=ft.Icons.SETTINGS_OUTLINED,
            tooltip=self._translator.t(key="top_bars.settings_button"),
            height=config.TOP_BAR_HEIGHT,
            icon_size=config.TOP_BAR_HEIGHT - 15,
            on_click=lambda _: self._router.go(route=config.ROUTE_SETTINGS),
        )

        # Initialize containers
        self._home_button_row: ft.Row = ft.Row(
            controls=[self._home_button],
            alignment=ft.MainAxisAlignment.START,
        )
        self._label_row: ft.Row = ft.Row(
            controls=[
                ft.Container(
                    content=self._label,
                    on_click=lambda _: top_bar_logout_action(
                        storages=self._storages,
                        router=self._router,
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )
        self._settings_button_row: ft.Row = ft.Row(
            controls=[self._settings_button],
            alignment=ft.MainAxisAlignment.END,
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
        self,
        page: ft.Page,
        translator: Translator,
        router: AppRouter,
        storages: Storages,
        title: str,
    ) -> None:
        self._page: ft.Page = page
        self._translator: Translator = translator
        self._router: AppRouter = router
        self._storages: Storages = storages
        self._title: str = title

        # Initialize labels
        self._label: ft.Text = ft.Text(
            value=self._title,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.START,
            # expand=True,
            theme_style=ft.TextThemeStyle.TITLE_LARGE,
            color=ft.Colors.PRIMARY,
        )

        # Initialize buttons
        self._back_button: ft.IconButton = ft.IconButton(
            icon=ft.Icons.ARROW_BACK_IOS_ROUNDED,
            tooltip=self._translator.t(key="top_bars.back_button"),
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
                    on_click=lambda _: top_bar_logout_action(
                        storages=self._storages,
                        router=self._router,
                    ),
                    expand=True,
                    padding=ft.padding.only(right=30),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def build(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            self._back_button_row,
                            self._label_row,
                        ],
                    ),
                    ft.Divider(height=1, thickness=1),
                ],
            ),
        )
