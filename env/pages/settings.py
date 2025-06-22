import flet as ft  # type:ignore[import-untyped]

from env.app.widgets.buttons_and_toggles import SectionButton, SectionToggle
from env.app.widgets.color_picker import ColorPicker
from env.app.widgets.container import MasterContainer
from env.app.widgets.sections import Section
from env.app.widgets.sliders import DescriptiveSlider
from env.app.widgets.top_bars import SubPageTopBar
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
        themes: Themes,
    ) -> None:
        self._page: ft.Page = page
        self._router: AppRouter = router
        self._storages: Storages = storages
        self._themes: Themes = themes

        " === Controls Appearance Section === "
        # Theme color picker
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
        self._font_size_slider: DescriptiveSlider = DescriptiveSlider(
            page=self._page,
            description="Font Size",
            slider_value=self._themes.font_size,
            slider_min=config.FONT_SIZE_MIN,
            slider_max=config.FONT_SIZE_MAX,
            on_change_end=self._change_font_size,
            slider_label="Font Size: {value}",
            slider_divisions=abs(config.FONT_SIZE_MAX - config.FONT_SIZE_MIN),
            slider_default_value=config.APPEARANCE_FONT_SIZE_DEFAULT,
        )

        " === Controls Security Section === "

        # Create sections
        self._appearance_section: Section = Section(
            title="Appearance",
            content=[
                SectionButton(
                    text="Change Color",
                    icon=ft.Icons.COLOR_LENS_OUTLINED,
                    func=lambda: self._page.open(self._theme_color_picker.build()),
                ).build(),
                ft.Row(
                    controls=[self._font_family_chooser],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                self._font_size_slider.build(),
            ],
        )

        self._security_section: Section = Section(
            title="Security",
            content=[
                # Logout on lost focus
                SectionToggle(
                    text="Logout on Lost Focus",
                    toggle_value=self._storages.client_storage.get(
                        key=config.CS_LOGOUT_ON_LOST_FOCUS,
                        default=config.LOGOUT_ON_LOST_FOCUS_DEFAULT,
                    ),
                    on_click=self._toggle_logout_lost_focus,
                ).build(),
                # Logout on on shake detection
                SectionToggle(
                    text="Logout on Shake Detection",
                    toggle_value=self._storages.client_storage.get(
                        key=config.CS_SHAKE_DETECTION_ENABLED,
                        default=config.SHAKE_DETECTION_ENABLED_DEFAULT,
                    ),
                    on_click=self._toggle_logout_shake_detection,
                ).build(),
            ],
        )

        # TODO: Add 'Support' section (--> donation, about)
        # TODO: Add delete data button
        # TODO: Add update button
        # TODO: Add change password button

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

    def _toggle_logout_lost_focus(self, e: ft.ControlEvent) -> None:
        value: bool = True if e.data == "true" else False

        self._storages.client_storage.set(
            key=config.CS_LOGOUT_ON_LOST_FOCUS,
            value=value,
        )

    def _toggle_logout_shake_detection(self, e: ft.ControlEvent) -> None:
        value: bool = True if e.data == "true" else False

        self._storages.client_storage.set(
            key=config.CS_SHAKE_DETECTION_ENABLED,
            value=value,
        )

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
                                    self._security_section.build(),
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
