import flet as ft  # type:ignore[import-untyped]

from env.app.widgets.buttons_and_toggles import SectionButton
from env.app.widgets.color_picker import ColorPicker
from env.app.widgets.container import MasterContainer
from env.app.widgets.sections import Section
from env.app.widgets.top_bars import SubPageTopBar
from env.classes.phone_sensors import ShakeDetector
from env.classes.router import AppRouter
from env.classes.storages import Storages
from env.config import config
from env.func.update_themes import set_theme
from env.themes.themes import Themes


class SettingsPage:
    def __init__(
        self,
        page: ft.Page,
        router: AppRouter,
        storages: Storages,
        shake_detector: ShakeDetector,
        themes: Themes,
    ) -> None:
        self._page: ft.Page = page
        self._router: AppRouter = router
        self._storages: Storages = storages
        self._shake_detector: ShakeDetector = shake_detector
        self._themes: Themes = themes

        # Initialize color picker
        self._theme_color_picker: ColorPicker = ColorPicker(
            page=self._page,
            on_color_click=self._change_theme_color,
        )

        # Create sections
        # TODO: Add the ability to change color seed, font family and font size!
        self._appearance_section: Section = Section(
            title="Appearance",
            content=[
                SectionButton(
                    text="Change Color",
                    icon=ft.Icons.COLOR_LENS_OUTLINED,
                    func=lambda: self._page.open(self._theme_color_picker.build()),
                ).build(),
            ],
        )

        # TODO: Use sections (custom class for easier access and management
        # TODO: Add font settings (size, family, ...)
        # TODO: Add shake detection settings (threshold_gravity, minimum_shake) --> for logging out
        # TODO: Add auto logout on lost focus
        # TODO: Add donation button
        # TODO: Add about section
        # TODO: Add delete data button
        # TODO: Add color change settings (theme color)

    def _change_theme_color(self, color: ft.ColorValue) -> None:
        self._storages.client_storage.set(key=config.CS_COLOR_SEED, value=color)
        self._themes.change_seed_color(new_color=color)
        set_theme(page=self._page, themes=self._themes)

    def build(self) -> ft.Container:
        return MasterContainer(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            SubPageTopBar(
                                page=self._page,
                                router=self._router,
                                storages=self._storages,
                                title="Settings",
                            ).build(),
                            ft.ListView(
                                controls=[
                                    self._appearance_section.build(),
                                ],
                                expand=True,
                                spacing=20,
                            ),
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
        )
