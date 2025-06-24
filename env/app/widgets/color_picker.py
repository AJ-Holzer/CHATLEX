from typing import Any, Callable, Optional

import flet as ft  # type: ignore[import-untyped]

from env.config import config
from env.func.colors import generate_color_wheel_hex
from env.func.validations import is_valid_color_code


class ColorPicker:
    def __init__(
        self,
        page: ft.Page,
        default_color: Optional[str] = None,
        on_color_click: Optional[Callable[[ft.ColorValue], Any]] = None,
        title: str = "Choose a color",
    ) -> None:
        self._page: ft.Page = page
        self._default_color: Optional[str] = default_color
        self._on_click_func: Optional[Callable[[ft.ColorValue], Any]] = on_color_click
        self._title: str = title

        # Create color buttons
        self._colors: list[str] = self._generate_colors(
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

        # Create custom color input field
        self._color_input_field: ft.TextField = ft.TextField(
            value=str(self._default_color).removeprefix("#"),
            prefix=ft.Text(value="#"),
            expand=True,
        )

        # Create color picker alert
        self._color_picker_alert: ft.AlertDialog = ft.AlertDialog(
            title=ft.Text(value=self._title, text_align=ft.TextAlign.CENTER),
            scrollable=True,
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=color_grid,
                        margin=20,
                    ),
                    ft.Container(
                        ft.Row(
                            controls=[
                                self._color_input_field,
                                ft.IconButton(
                                    icon=ft.Icons.CHECK_ROUNDED,
                                    tooltip="Confirm",
                                    on_click=lambda _: self._on_color_chosen(
                                        str(self._color_input_field.value)
                                    ),
                                ),
                            ]
                        ),
                        margin=20,
                    ),
                ],
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

    def _generate_colors(self, n: int) -> list[str]:
        try:
            colors: list[str] = generate_color_wheel_hex(n)
            return [c for c in colors if c.startswith("#") and len(c) in (7, 9)]
        except Exception:
            return ["#FF0000", "#00FF00", "#0000FF"]

    def _on_color_chosen(self, col: str) -> None:
        # Add '#' to color if not already
        modified_color: str = f"#{col}" if not col.startswith("#") else col

        print(f"{modified_color=}")

        # Return if color not valid
        if not is_valid_color_code(color=col):
            self._color_input_field.border_color = ft.Colors.RED
            self._color_input_field.update()
            return

        # Reset input field color and update input field value
        self._color_input_field.border_color = None
        self._color_input_field.value = col.removeprefix("#")
        self._color_input_field.update()

        # Run function
        if self._on_click_func:
            self._on_click_func(modified_color)

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
