import json
import os
from typing import Literal

import flet as ft  # type: ignore[import-untyped]

from env.app.widgets.buttons_and_toggles import (ActionButton, SectionToggle,
                                                 URLButton)
from env.app.widgets.color_picker import ColorPicker
from env.app.widgets.container import MasterContainer
from env.app.widgets.dropdown import SectionDropDown
from env.app.widgets.info import InfoButtonAlert
from env.app.widgets.sections import Section
from env.app.widgets.sliders import DescriptiveSlider
from env.app.widgets.top_bars import SubPageTopBar
from env.classes.router import AppRouter
from env.classes.shake_detector import ShakeDetector
from env.classes.storages import Storages
from env.classes.translate import Translator
from env.config import config
from env.themes.themes import Themes


class SettingsPage:
    def __init__(
        self,
        page: ft.Page,
        translator: Translator,
        router: AppRouter,
        storages: Storages,
        themes: Themes,
        shake_detector: ShakeDetector,
    ) -> None:
        self._page: ft.Page = page
        self._translator: Translator = translator
        self._router: AppRouter = router
        self._storages: Storages = storages
        self._themes: Themes = themes
        self._shake_detector: ShakeDetector = shake_detector

        " === CONTROLS APPEARANCE SECTION === "
        # Theme color picker
        self._theme_color_picker: ColorPicker = ColorPicker(
            page=self._page,
            translator=self._translator,
            title=self._translator.t(key="settings_page.color_picker"),
            default_color=self._themes.color_seed,
            on_color_click=lambda col: self._change_theme_color(new_color=col),
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
        self._font_family_chooser: SectionDropDown = SectionDropDown(
            value=self._themes.font_family,
            label=self._translator.t(key="settings_page.font_family_chooser"),
            options=font_options,
            on_change=self._change_font_family,
        )
        self._font_size_slider: DescriptiveSlider = DescriptiveSlider(
            page=self._page,
            description=self._translator.t(
                key="settings_page.font_size_slider.description"
            ),
            slider_value=self._themes.font_size,
            slider_min=config.FONT_SIZE_MIN,
            slider_max=config.FONT_SIZE_MAX,
            on_change_end=self._change_font_size,
            slider_label=self._translator.t(
                key="settings_page.font_size_slider.slider_label"
            ),
            slider_divisions=abs(config.FONT_SIZE_MAX - config.FONT_SIZE_MIN),
            slider_default_value=config.APPEARANCE_FONT_SIZE_DEFAULT,
        )

        " === CONTROLS SECURITY SECTION === "
        # TODO: Use locales yml instead ("infos.yml", "about.yml")
        for file_path in [
            config.FILE_INFOS,
            config.FILE_ABOUT,
        ]:
            if not os.path.exists(path=file_path):
                raise FileNotFoundError(f"File {file_path} not found!")
        # Load infos and their descriptions
        with open(
            file=config.FILE_INFOS,
            mode="r",
            encoding="UTF-8",
        ) as i, open(
            file=config.FILE_ABOUT,
            mode="r",
            encoding="UTF-8",
        ) as a:
            infos: dict[str, dict[Literal["content", "icon"], str]] = json.load(i)
            about: dict[str, dict[Literal["content", "icon"], str]] = json.load(a)
        # Logout on lost focus
        self._toggle_lolf: SectionToggle = SectionToggle(
            text=self._translator.t(key="settings_page.toggle_lolf"),
            toggle_value=self._storages.client_storage.get(
                key=config.CS_LOGOUT_ON_LOST_FOCUS,
                default=config.LOGOUT_ON_LOST_FOCUS_DEFAULT,
            ),
            on_click=self._toggle_logout_lost_focus,
        )
        # Logout on on shake detection
        self._toggle_shake_detection: SectionToggle = SectionToggle(
            text=self._translator.t(key="settings_page.toggle_shake_detection"),
            toggle_value=self._storages.client_storage.get(
                key=config.CS_SHAKE_DETECTION_ENABLED,
                default=config.SHAKE_DETECTION_ENABLED_DEFAULT,
            ),
            on_click=self._toggle_logout_shake_detection,
        )
        # Gravity threshold slider for shake detection
        self._slider_gravity_threshold: DescriptiveSlider = DescriptiveSlider(
            page=self._page,
            description=self._translator.t(
                key="settings_page.shake_gravity_threshold_slider.description"
            ),
            slider_value=self._storages.client_storage.get(
                key=config.CS_SHAKE_DETECTION_THRESHOLD_GRAVITY,
                default=config.SHAKE_DETECTION_THRESHOLD_GRAVITY_DEFAULT,
            )
            * config.SHAKE_DETECTION_THRESHOLD_GRAVITY_MULTIPLIER,
            slider_min=config.SHAKE_DETECTION_THRESHOLD_GRAVITY_MIN
            * config.SHAKE_DETECTION_THRESHOLD_GRAVITY_MULTIPLIER,
            slider_max=config.SHAKE_DETECTION_THRESHOLD_GRAVITY_MAX
            * config.SHAKE_DETECTION_THRESHOLD_GRAVITY_MULTIPLIER,
            on_change_end=self._change_shake_detection_gravity_threshold,
            slider_label=self._translator.t(
                key="settings_page.shake_gravity_threshold_slider.slider_label"
            ),
            slider_divisions=int(
                abs(
                    config.SHAKE_DETECTION_THRESHOLD_GRAVITY_MAX
                    - config.SHAKE_DETECTION_THRESHOLD_GRAVITY_MIN
                )
                * config.SHAKE_DETECTION_THRESHOLD_GRAVITY_MULTIPLIER
            ),
            slider_default_value=config.SHAKE_DETECTION_THRESHOLD_GRAVITY_DEFAULT
            * config.SHAKE_DETECTION_THRESHOLD_GRAVITY_MULTIPLIER,
        )
        # Logout on top bar label click
        self._toggle_tblc: SectionToggle = SectionToggle(
            text=self._translator.t(key="settings_page.toggle_tblc"),
            toggle_value=self._storages.client_storage.get(
                key=config.CS_LOGOUT_ON_TOP_BAR_LABEL_CLICK,
                default=config.TOP_BAR_LOGOUT_ON_LABEL_CLICK_DEFAULT,
            ),
            on_click=self._toggle_logout_on_top_bar_label_click,
        )

        " === LOAD SECTIONS === "
        # Create sections
        self._appearance_section: Section = Section(
            title=self._translator.t(key="settings_page.appearance_section"),
            content=[
                # Change theme color button
                ActionButton(
                    page=self._page,
                    text=self._translator.t(
                        key="settings_page.change_theme_color_button"
                    ),
                    icon=ft.Icons.COLOR_LENS_OUTLINED,
                    on_click=lambda _: self._page.open(
                        self._theme_color_picker.build()
                    ),
                ).build(),
                # Font family chooser
                ft.Row(
                    controls=[self._font_family_chooser.build()],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                # Font size
                self._font_size_slider.build(),
            ],
        )
        self._security_section: Section = Section(
            title=self._translator.t(key="settings_page.security_section"),
            content=[
                self._toggle_lolf.build(),
                self._toggle_tblc.build(),
                self._toggle_shake_detection.build(),
                self._slider_gravity_threshold.build(),
            ],
        )
        # TODO: Don't use help section. Make the label of the toggles and sliders clickable instead!
        self._help_section: Section = Section(
            title=self._translator.t(key="settings_page.help_section"),
            content=[
                # TODO: Use locales yml files instead!
                InfoButtonAlert(
                    page=self._page,
                    label=label,
                    content=data["content"],
                    icon=data["icon"],
                ).build()
                for label, data in infos.items()
            ],
        )  # TODO: Add infos (about, why shaking, what is lost focus, ...)

        " === SUPPORT & ABOUT === "
        self._support_button: URLButton = URLButton(
            page=self._page,
            text=self._translator.t(key="settings_page.support_button"),
            url="https://ajservers.site/faqs",
            icon=ft.CupertinoIcons.HEART,
        )
        self._about_buttons: ft.Column = ft.Column(
            controls=[
                # TODO: Use locales yml files instead!
                InfoButtonAlert(
                    page=self._page,
                    label=label,
                    content=data["content"],
                    icon=data["icon"],
                ).build()
                for label, data in about.items()
            ]
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
        if not config.FONT_SIZE_MIN <= float(e.data) <= config.FONT_SIZE_MAX:
            raise ValueError(f"Font size not valid! Got font_size='{e.data}'")

        self._themes.change_font_size(new_font_size=int(float(e.data)))

    def _toggle_logout_lost_focus(self, e: ft.ControlEvent) -> None:
        value: bool = True if e.data == "true" else False

        self._storages.client_storage.set(
            key=config.CS_LOGOUT_ON_LOST_FOCUS,
            value=value,
        )

    def _toggle_logout_shake_detection(self, e: ft.ControlEvent) -> None:
        value: bool = True if e.data == "true" else False

        # Update storage and set enabled state
        self._storages.client_storage.set(
            key=config.CS_SHAKE_DETECTION_ENABLED,
            value=value,
        )
        self._shake_detector.enabled = value

    def _toggle_logout_on_top_bar_label_click(self, e: ft.ControlEvent) -> None:
        value: bool = True if e.data == "true" else False

        # Update storage and set enabled state
        self._storages.client_storage.set(
            key=config.CS_LOGOUT_ON_TOP_BAR_LABEL_CLICK,
            value=value,
        )
        # TODO: Set enabled state of top bar

    def _change_shake_detection_gravity_threshold(self, e: ft.ControlEvent) -> None:
        if e.data is None:
            raise ValueError("No gravity threshold provided!")

        # Divide gravity to store as actual number
        new_threshold: float = (
            float(e.data) / config.SHAKE_DETECTION_THRESHOLD_GRAVITY_MULTIPLIER
        )

        # Update client storage
        self._storages.client_storage.set(
            key=config.CS_SHAKE_DETECTION_THRESHOLD_GRAVITY,
            value=new_threshold,
        )

        # Update shake detector
        self._shake_detector.gravity_threshold = new_threshold

    def _update_sliders(self) -> None:
        # Font size slider
        self._font_size_slider.slider_value = self._storages.client_storage.get(
            key=config.CS_FONT_SIZE,
            default=config.APPEARANCE_FONT_SIZE_DEFAULT,
        )
        # Gravity threshold slider
        self._slider_gravity_threshold.slider_value = (
            self._storages.client_storage.get(
                key=config.CS_SHAKE_DETECTION_THRESHOLD_GRAVITY,
                default=config.SHAKE_DETECTION_THRESHOLD_GRAVITY_DEFAULT,
            )
            * config.SHAKE_DETECTION_THRESHOLD_GRAVITY_MULTIPLIER
        )

    def _change_theme_color(self, new_color: str) -> None:
        self._themes.color_seed = new_color

    def initialize(self) -> None:
        self._update_sliders()

    def build(self) -> ft.Container:
        return MasterContainer(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            SubPageTopBar(
                                page=self._page,
                                translator=self._translator,
                                router=self._router,
                                storages=self._storages,
                                title=self._translator.t(key="settings_page.top_bar"),
                            ).build(),
                            ft.ListView(
                                controls=[
                                    self._appearance_section.build(),
                                    self._security_section.build(),
                                    self._help_section.build(),
                                    self._support_button.build(),
                                    self._about_buttons,
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
