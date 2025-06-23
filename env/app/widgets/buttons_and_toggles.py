from typing import Any, Callable, Optional

import flet as ft  # type:ignore[import-untyped]


class SectionButton:
    def __init__(
        self,
        text: str,
        icon: Optional[ft.IconValue] = None,
        func: Optional[Callable[..., Any]] = None,
        func_args: Optional[tuple[Any, ...]] = None,
    ) -> None:
        self._text: str = text
        self._icon: Optional[ft.IconValue] = icon
        self._func: Optional[Callable[..., Any]] = func
        self._func_args: Optional[tuple[Any, ...]] = func_args

        # Modern, stylized button
        self._text_button: ft.ElevatedButton = ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            (
                                ft.Icon(self._icon, size=20)
                                if self._icon
                                else ft.Container()
                            ),
                        ],
                    ),
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
            style=ft.ButtonStyle(
                padding=ft.Padding(left=16, top=12, right=16, bottom=12),
                shape=ft.RoundedRectangleBorder(radius=12),
                elevation=4,
                overlay_color=ft.Colors.with_opacity(0.08, ft.Colors.ON_PRIMARY),
            ),
        )

    def _on_click(self, e: ft.ControlEvent) -> None:
        if self._func:
            if self._func_args:
                self._func(*self._func_args)
            else:
                self._func()

    def build(self) -> ft.Container:
        return ft.Container(
            content=self._text_button,
            alignment=ft.alignment.center,
            expand=True,
            padding=ft.Padding(left=20, top=0, right=20, bottom=0),
        )


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
