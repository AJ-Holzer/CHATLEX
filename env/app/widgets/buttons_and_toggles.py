from typing import Optional

import flet as ft  # type: ignore[import-untyped]

from env.app.widgets.links import LinkAlert


class SimpleButton:
    def __init__(
        self,
        page: ft.Page,
        text: str,
        icon: Optional[ft.IconValue],
        is_destructive: bool,
        on_click: ft.OptionalControlEventCallable = None,
        url: Optional[str] = None,
    ) -> None:
        self._page: ft.Page = page
        self._text: str = text
        self._icon: Optional[ft.IconValue] = icon
        self._is_destructive: bool = is_destructive
        self._on_click_action: ft.OptionalControlEventCallable = on_click
        self._url: Optional[str] = url

        # Raise exception if url and on_click_action are provided
        if self._url is not None and self._on_click_action is not None:
            raise ValueError("Expected url or on_click_action but both were given!")
        # Raise exception if no url and no on_click_action provided
        if self._url is None and self._on_click_action is None:
            raise ValueError("Expected url or on_click_action but none were given!")

        # Modern, stylized button
        self._text_button: ft.ElevatedButton = ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    # Icon
                    ft.Column(
                        controls=[
                            (
                                ft.Icon(self._icon, size=20)
                                if self._icon
                                else ft.Container()
                            ),
                        ],
                    ),
                    # Text
                    ft.Column(
                        controls=[
                            ft.Text(
                                self._text,
                                theme_style=ft.TextThemeStyle.BODY_LARGE,
                                max_lines=None,
                            ),
                        ],
                        expand=True,
                    ),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            on_click=self._on_click,
            color=None if not self._is_destructive else ft.Colors.RED,
            style=ft.ButtonStyle(
                padding=ft.Padding(left=16, top=12, right=16, bottom=12),
                shape=ft.RoundedRectangleBorder(radius=12),
                elevation=4,
                overlay_color=ft.Colors.with_opacity(0.08, ft.Colors.ON_PRIMARY),
            ),
        )

    def _on_click(self, e: ft.ControlEvent) -> None:
        # Run action if provided
        if self._on_click_action:
            self._on_click_action(e)
            return

        # Check if link exists
        if not self._url:
            raise ValueError("No URL provided!")

        # Create and open link open alert
        LinkAlert(page=self._page, url=self._url).open()

    def build(self) -> ft.Container:
        return ft.Container(
            content=self._text_button,
            alignment=ft.alignment.center,
            expand=True,
            padding=ft.Padding(left=20, top=0, right=20, bottom=0),
        )


class ActionButton:
    def __init__(
        self,
        page: ft.Page,
        text: str,
        icon: Optional[ft.IconValue] = None,
        on_click: ft.OptionalControlEventCallable = None,
        is_destructive: bool = False,
    ) -> None:
        self._page: ft.Page = page
        self._text: str = text
        self._icon: Optional[ft.IconValue] = icon
        self._on_click: ft.OptionalControlEventCallable = on_click
        self._is_destructive: bool = is_destructive

        # Modern, stylized button
        self._button: SimpleButton = SimpleButton(
            page=self._page,
            text=self._text,
            icon=self._icon,
            is_destructive=self._is_destructive,
            on_click=self._on_click,
        )

    def build(self) -> ft.Container:
        return self._button.build()


class URLButton:
    def __init__(
        self,
        page: ft.Page,
        text: str,
        url: str,
        icon: Optional[ft.IconValue] = None,
    ) -> None:
        self._page: ft.Page = page
        self._text: str = text
        self._icon: Optional[ft.IconValue] = icon
        self._url: str = url

        # Modern, stylized button
        self._button: SimpleButton = SimpleButton(
            page=self._page,
            text=self._text,
            icon=self._icon,
            is_destructive=False,
            url=self._url,
        )

    def build(self) -> ft.Container:
        return self._button.build()


class SectionToggle:
    def __init__(
        self,
        text: str,
        toggle_value: bool,
        on_click: ft.OptionalControlEventCallable,
    ) -> None:
        self._text: str = text
        self._toggle_value: bool = toggle_value
        self._on_click: ft.OptionalControlEventCallable = on_click

        # Create toggle
        self._toggle: ft.CupertinoSwitch = ft.CupertinoSwitch(
            value=self._toggle_value,
            on_change=self._on_click,
        )

        # Create label
        self._label: ft.Text = ft.Text(value=self._text, expand=True)

    def build(self) -> ft.Container:
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[self._label],
                        expand=True,
                    ),
                    ft.Column(
                        controls=[self._toggle],
                    ),
                ],
                expand=True,
            ),
            padding=ft.Padding(left=20, top=0, right=20, bottom=0),
        )
