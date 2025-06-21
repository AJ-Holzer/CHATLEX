import flet as ft  # type: ignore


class Themes:
    def __init__(self, page: ft.Page, color_seed: ft.ColorValue) -> None:
        self._color_seed: ft.ColorValue = color_seed
        self._page: ft.Page = page

        self._light: ft.Theme = ft.Theme(
            color_scheme_seed=self._color_seed,
            use_material3=True,
        )

        self._dark: ft.Theme = ft.Theme(
            color_scheme_seed=self._color_seed,
            use_material3=True,
        )

        self._all_themes: list[ft.Theme] = [self._light, self._dark]

    def change_seed_color(self, new_color: ft.ColorValue) -> None:
        # TODO: Save the theme seed color!

        self._color_seed = new_color

        # Update themes
        for theme in self._all_themes:
            theme.color_scheme_seed = self._color_seed

        print(f"Changed color to '{self._color_seed}'")

    @property
    def DARK(self) -> ft.Theme:
        return self._dark

    @property
    def LIGHT(self) -> ft.Theme:
        return self._light
