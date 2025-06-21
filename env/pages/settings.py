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
            on_color_click=self._themes.change_seed_color,
        )

        # Create font family chooser
        if self._page.fonts:
            font_options = [
                ft.dropdown.Option(key=font_family, text=font_family)
                for font_family in self._page.fonts.keys()
            ]
        else:
            font_options = [
                ft.dropdown.Option(
                    key=self._themes.font_family,
                    text=self._themes.font_family,
                )
            ]
        self._font_family_chooser: ft.Dropdown = ft.Dropdown(
            value=self._themes.font_family,
            options=font_options,
            label="Font Family",
            on_change=self._change_font_family,
        )

        # Crate font size slider
        # TODO: Create a 'DescriptiveSlider' class instead!
        self._font_size_label: ft.Container = ft.Container(
            content=ft.Text(
                value="Font Size",
                expand=True,
                text_align=ft.TextAlign.CENTER,
                theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
            ),
            padding=ft.padding.only(top=10),
        )
        self._font_size_slider: ft.Slider = ft.Slider(
            value=self._themes.font_size,
            min=config.FONT_SIZE_MIN,
            max=config.FONT_SIZE_MAX,
            on_change_end=self._change_font_size,
            label="Font Size: {value}",
            divisions=abs(config.FONT_SIZE_MAX - config.FONT_SIZE_MIN),
            expand=True,
        )

        # Create sections
        self._appearance_section: Section = Section(
            title="Appearance",
            content=[
                SectionButton(
                    text="Change Color",
                    icon=ft.Icons.COLOR_LENS_OUTLINED,
                    func=lambda: self._page.open(self._theme_color_picker.build()),
                ).build(),
                self._font_family_chooser,
                self._font_size_label,
                self._font_size_slider,
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
        # TODO: Add password changing

    def _change_font_family(self, e: ft.ControlEvent) -> None:
        if not e.data:
            raise ValueError(
                f"There is no drop down option when changing font family. Got '{e}'!"
            )
        self._themes.change_font_family(new_font_family=str(e.data))

    def _change_font_size(self, e: ft.ControlEvent) -> None:
        if e.data is None:
            raise ValueError("No font size provided!")
        if float(e.data) < 0.0:
            raise ValueError("Font size is not allowed to be negative!")

        self._themes.change_font_size(new_font_size=int(float(e.data)))

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
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    ),
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
        )
