from typing import Any, Callable, Optional

import flet as ft  # type: ignore[import-untyped]

from env.config import config
from env.func.colors import generate_color_wheel_hex


# FIXME: The UI elements are arranged really ugly!
class ColorPicker:
    def __init__(
        self,
        page: ft.Page,
        on_color_click: Optional[Callable[[ft.ColorValue], Any]] = None,
        title: str = "Choose a color",
    ) -> None:
        self._page: ft.Page = page
        self._on_click_func: Optional[Callable[[ft.ColorValue], Any]] = on_color_click
        self._title: str = title

        # Create color buttons
        self._colors: list[str] = self._safe_generate_colors(
            config.COLOR_PICKER_AMOUNT_COLORS
        )
        self._color_buttons: list[ft.Container] = [
            self._create_color_button(color) for color in self._colors
        ]

        # Create grid view with buttons
        color_grid: ft.GridView = ft.GridView(
            runs_count=6,
            max_extent=config.COLOR_PICKER_BUTTON_SIZE
            + 2 * config.COLOR_PICKER_BUTTON_SPACING,
            child_aspect_ratio=1.0,
            spacing=config.COLOR_PICKER_BUTTON_SPACING,
            run_spacing=config.COLOR_PICKER_BUTTON_SPACING,
            controls=self._color_buttons,
        )

        # Create color picker alert
        self._color_picker_alert: ft.AlertDialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(value=self._title),
            scrollable=True,
            content=ft.Container(
                content=color_grid,
                margin=20,
                bgcolor="#fff",
            ),
            actions=[
                ft.TextButton(
                    text="Reset",
                    on_click=lambda _: self._reset_default(),
                ),
                ft.TextButton(
                    text="Close",
                    on_click=lambda _: self._page.close(self._color_picker_alert),
                ),
            ],
        )

    def _safe_generate_colors(self, n: int) -> list[str]:
        try:
            colors: list[str] = generate_color_wheel_hex(n)
            return [c for c in colors if c.startswith("#") and len(c) in (7, 9)]
        except Exception:
            return ["#FF0000", "#00FF00", "#0000FF"]

    def _on_color_chosen(self, col: str) -> None:
        if self._on_click_func:
            self._on_click_func(col)
        self._page.close(self._color_picker_alert)

    def _create_color_button(self, color: ft.ColorValue) -> ft.Container:
        return ft.Container(
            bgcolor=color,
            width=config.COLOR_PICKER_BUTTON_SIZE,
            height=config.COLOR_PICKER_BUTTON_SIZE,
            border_radius=6,
            ink=True,
            tooltip=color,
            on_click=lambda _, col=color: self._on_color_chosen(col),
        )

    def _reset_default(self) -> None:
        self._on_color_chosen(config.APPEARANCE_COLOR_SEED_DEFAULT)

    def build(self) -> ft.AlertDialog:
        return self._color_picker_alert
