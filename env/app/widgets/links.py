import flet as ft  # type: ignore[import-untyped]


class LinkAlert:
    def __init__(self, page: ft.Page, url: str) -> None:
        self._page: ft.Page = page
        self._url: str = url

        self._alert: ft.AlertDialog = ft.AlertDialog(
            title=ft.Text(value="Open URL", text_align=ft.TextAlign.CENTER),
            content=ft.Text(
                value=f"Are you sure you want to open this URL in your browser?\n\n{self._url}",
                text_align=ft.TextAlign.START,
            ),
            actions=[
                ft.TextButton(
                    text="Copy URL",
                    on_click=lambda _: (
                        self._page.set_clipboard(value=self._url),
                        self._page.close(self._alert),
                        self._page.open(
                            ft.SnackBar(
                                content=ft.Text(
                                    value="Link copied!",
                                    text_align=ft.TextAlign.CENTER,
                                )
                            )
                        ),
                    ),
                ),
                ft.TextButton(
                    text="Open",
                    style=ft.ButtonStyle(
                        color=ft.Colors.RED,
                    ),
                    on_click=lambda _: (
                        self._page.launch_url(url=self._url),
                        self._page.close(self._alert),
                    ),
                ),
            ],
        )

    def open(self) -> None:
        self._page.open(self._alert)
