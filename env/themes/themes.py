from typing import Any

import flet as ft  # type: ignore

from env.classes.storages import Storages
from env.config import config


class Themes:
    def __init__(
        self,
        page: ft.Page,
        storages: Storages,
    ) -> None:
        self._page: ft.Page = page
        self._storages: Storages = storages
        self._color_seed: ft.ColorValue = self._storages.client_storage.get(
            key=config.CS_COLOR_SEED,
            default=config.APPEARANCE_COLOR_SEED_DEFAULT,
        )
        self._font_family: str = self._storages.client_storage.get(
            key=config.CS_FONT_FAMILY,
            default=config.APPEARANCE_FONT_FAMILY_DEFAULT,
        )
        self._font_size: int = self._storages.client_storage.get(key=config.CS_FONT_SIZE, default=config.APPEARANCE_FONT_SIZE_DEFAULT)

        # Set themes
        self._light: ft.Theme = ft.Theme(
            color_scheme_seed=self._color_seed,
            use_material3=True,
            text_theme=self._generate_text_theme(),
        )
        self._dark: ft.Theme = ft.Theme(
            color_scheme_seed=self._color_seed,
            use_material3=True,
            text_theme=self._generate_text_theme(),
        )
        self._all_themes: list[ft.Theme] = [self._light, self._dark]

    def _update(
        self,
        key: str,
        value: Any,
    ) -> None:
        self._storages.client_storage.set(key=key, value=value)
        self.set_theme()

    def _generate_text_theme(self) -> ft.TextTheme:
        def ts(size_multiplier: float) -> ft.TextStyle:
            return ft.TextStyle(
                size=self._font_size * size_multiplier,
                font_family=self._font_family,
                color=ft.Colors.ON_SURFACE
            )

        return ft.TextTheme(
            body_large=ts(size_multiplier=1.1),
            body_medium=ts(size_multiplier=1.0),
            body_small=ts(size_multiplier=0.85),

            display_large=ts(size_multiplier=2.2),
            display_medium=ts(size_multiplier=1.8),
            display_small=ts(size_multiplier=1.5),

            headline_large=ts(size_multiplier=1.7),
            headline_medium=ts(size_multiplier=1.5),
            headline_small=ts(size_multiplier=1.3),

            label_large=ts(size_multiplier=0.95),
            label_medium=ts(size_multiplier=0.85),
            label_small=ts(size_multiplier=0.75),

            title_large=ts(size_multiplier=1.4),
            title_medium=ts(size_multiplier=1.2),
            title_small=ts(size_multiplier=1.0),
        )

    def _update_text_themes(self) -> None:
        for theme in self._all_themes:
            theme.text_theme = self._generate_text_theme()

    def set_theme(self) -> None:
        if self._page.platform_brightness == ft.Brightness.DARK:
            self._page.theme = self.DARK
        else:
            self._page.theme = self.LIGHT

        self._page.update()  # type:ignore

    def change_seed_color(self, new_color: ft.ColorValue) -> None:
        self._color_seed = new_color

        # Update themes
        for theme in self._all_themes:
            theme.color_scheme_seed = self._color_seed

        self._update(key=config.CS_COLOR_SEED, value=self._color_seed)

    def change_font_family(self, new_font_family: str) -> None:
        if not self._page.fonts:
            raise ValueError("No fonts available!")

        if new_font_family not in self._page.fonts:
            raise ValueError(f"Font '{new_font_family}' not found! Use one of these instead: [{", ".join(font_family for font_family in self._page.fonts)}]")

        self._font_family = new_font_family

        self._update_text_themes()
        self._update(key=config.CS_FONT_FAMILY, value=self._font_family)

    def change_font_size(self, new_font_size: int) -> None:
        if new_font_size < 0:
            raise ValueError("New font size must be positive!")

        self._font_size = new_font_size

        self._update_text_themes()
        self._update(key=config.CS_FONT_SIZE, value=self._font_size)

    @property
    def DARK(self) -> ft.Theme:
        return self._dark

    @property
    def LIGHT(self) -> ft.Theme:
        return self._light

    @property
    def font_family(self) -> str:
        return self._font_family

    @property
    def font_size(self) -> int:
        return self._font_size
