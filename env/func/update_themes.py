import flet as ft  # type:ignore[import-untyped]

from env.themes.themes import themes


def update_theme(page: ft.Page) -> None:
    if page.platform_brightness == ft.Brightness.DARK:
        page.theme = themes.DARK
    else:
        page.theme = themes.LIGHT

    page.update()  # type:ignore
