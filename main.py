import flet as ft  # type:ignore[import-untyped]

from env.config import config


def main(page: ft.Page) -> None:
    # Initialize window
    page.title = config.APP_TITLE
    page.window.resizable = config.APP_RESIZABLE
    page.window.width = config.APP_WIDTH
    page.window.height = config.APP_HEIGHT


if __name__ == "__main__":
    ft.app(target=main)  # type:ignore
