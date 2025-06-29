from typing import Any, Callable, Optional, cast

import flet as ft  # type: ignore[import-untyped]

from env.config import config
from env.func.colors import generate_color_wheel_hex
from env.func.validations import is_valid_color_code
from env.classes.translations import Translator


class ColorPicker:
    def __init__(
        self,
        page: ft.Page,
        translator: Translator,
        default_color: Optional[str] = None,
        on_color_click: Optional[Callable[[ft.ColorValue], Any]] = None,
    ) -> None:
        self._page: ft.Page = page
        self._translator: Translator = translator
        self._default_color: Optional[str] = default_color
        self._on_click_func: Optional[Callable[[ft.ColorValue], Any]] = on_color_click

        # Save last color for resetting
        self._last_color: str = str(self._default_color)

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
        self._color_input_field: ft.Control = self._translator.wrap_control(
            route="/color-picker",
            control_name="color-input-field",
            control=ft.TextField(
                value=str(self._default_color).removeprefix("#"),
                prefix=ft.Text(value="#"),
                expand=True,
            ),
        )

        # Create color picker alert
        self._color_picker_alert: ft.AlertDialog = ft.AlertDialog(
            title=self._translator.wrap_control(
                route="/color-picker",
                control_name="title",
                control=ft.Text(text_align=ft.TextAlign.CENTER),
            ),
            scrollable=True,
            on_dismiss=self._on_dismiss,
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
                                # Confirm button
                                self._translator.wrap_control(
                                    route="/color-picker",
                                    control_name="apply-custom-color-button",
                                    control=ft.IconButton(
                                        icon=ft.Icons.CHECK_ROUNDED,
                                        on_click=lambda _: self._on_color_chosen(
                                            str(
                                                cast(
                                                    ft.TextField,
                                                    self._color_input_field,
                                                ).value
                                            )
                                        ),
                                    ),
                                ),
                            ]
                        ),
                        margin=20,
                    ),
                ],
            ),
            actions=[
                # Reset button
                self._translator.wrap_control(
                    route="/color-picker",
                    control_name="reset-button",
                    control=ft.TextButton(
                        text="Reset",
                        on_click=lambda _: self._reset_default(),
                    ),
                ),
                # Close button
                self._translator.wrap_control(
                    route="/color-picker",
                    control_name="cancel-button",
                    control=ft.TextButton(
                        text="Close",
                        on_click=self._on_dismiss,
                    ),
                ),
            ],
        )

    def _on_dismiss(self, e: ft.ControlEvent) -> None:
        # Reset color input field if invalid value
        cast(
            ft.TextField, self._color_input_field
        ).value = self._last_color.removeprefix("#")
        cast(ft.TextField, self._color_input_field).error_text = None
        self._color_input_field.update()

        self._page.close(self._color_picker_alert)

    def _generate_colors(self, n: int) -> list[str]:
        try:
            colors: list[str] = generate_color_wheel_hex(n)
            return [c for c in colors if c.startswith("#") and len(c) in (7, 9)]
        except Exception:
            return ["#FF0000", "#00FF00", "#0000FF"]

    def _on_color_chosen(self, col: str) -> None:
        # Add '#' to color if not already
        modified_color: str = (f"#{col}" if not col.startswith("#") else col).upper()

        print(f"{modified_color=}")

        # Change error text state and return if color not valid
        if not is_valid_color_code(color=col):
            self._translator.update_control_state(
                route="/color-picker",
                control_name="color-input-field",
                states={
                    "value": None,
                    "label": None,
                    "text": None,
                    "helper_text": None,
                    "error_text": "color-invalid",
                    "tooltip": None,
                },
            )
            return

        # Reset input field color and update input field value
        # TODO: Use translator state instead
        self._translator.update_control_state(
            route="/color-picker",
            control_name="color-input-field",
            states={
                "value": None,
                "label": None,
                "text": None,
                "helper_text": None,
                "error_text": "color-invalid",
                "tooltip": None,
            },
        )
        cast(ft.TextField, self._color_input_field).value = col.removeprefix("#")
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
