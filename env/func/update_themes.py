import flet as ft  # type:ignore[import-untyped]

from env.themes.themes import Themes


def set_theme(page: ft.Page, themes: Themes) -> None:
    if page.platform_brightness == ft.Brightness.DARK:
        page.theme = themes.DARK
    else:
        page.theme = themes.LIGHT

    page.update()  # type:ignore
