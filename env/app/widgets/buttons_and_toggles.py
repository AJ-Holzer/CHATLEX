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
                    ft.Icon(self._icon, size=20) if self._icon else ft.Container(),
                    ft.Text(self._text, theme_style=ft.TextThemeStyle.BODY_LARGE),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            on_click=self._on_click,
            style=ft.ButtonStyle(
                padding=ft.Padding(16, 12, 16, 12),
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
            padding=8,
            alignment=ft.alignment.center,
            expand=True,
        )


class SectionToggle:
    def __init__(self) -> None:
        # TODO: Add toggle button code!
        raise NotImplementedError("This function is not implemented yet!")

    def build(self) -> ft.Container:
        # TODO: Add build code!
        return ft.Container()
