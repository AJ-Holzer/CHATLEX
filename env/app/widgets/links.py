import flet as ft  # type:ignore[import-untyped]

from env.classes.translations import Translator


class LinkAlert:
    def __init__(
        self,
        page: ft.Page,
        translator: Translator,
        link_id: str,
        url: str,
    ) -> None:
        self._page: ft.Page = page
        self._translator: Translator = translator
        self._link_id: str = link_id
        self._url: str = url

        self._alert: ft.AlertDialog = ft.AlertDialog(
            title=self._translator.wrap_control(
                route="/link/",
                control_name="label",
                control=ft.Text(text_align=ft.TextAlign.CENTER),
            ),
            content=self._translator.wrap_control(
                route="/link",
                control_name="info",
                control=ft.Text(
                    text_align=ft.TextAlign.START,
                ),
                url=self._url,
            ),
            actions=[
                # Copy URL button
                self._translator.wrap_control(
                    route="/link",
                    control_name="copy-url-button",
                    control=ft.TextButton(
                        on_click=lambda _: (
                            self._page.set_clipboard(value=self._url),
                            self._page.close(self._alert),
                            self._page.open(
                                ft.SnackBar(
                                    content=self._translator.wrap_control(
                                        route="/link",
                                        control_name="snackbar-info-url-copied",
                                        control=ft.Text(
                                            text_align=ft.TextAlign.CENTER,
                                        ),
                                    )
                                )
                            ),
                        ),
                    ),
                ),
                # Open URL button
                self._translator.wrap_control(
                    route="/link",
                    control_name="open-url-button",
                    control=ft.TextButton(
                        style=ft.ButtonStyle(
                            color=ft.Colors.RED,
                        ),
                        on_click=lambda _: (
                            self._page.launch_url(url=self._url),
                            self._page.close(self._alert),
                        ),
                    ),
                ),
            ],
        )

    def open(self) -> None:
        self._page.open(self._alert)
