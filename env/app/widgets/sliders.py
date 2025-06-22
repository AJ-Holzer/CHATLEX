from typing import Optional

import flet as ft  # type: ignore[import-untyped]


class DescriptiveSlider:
    def __init__(
        self,
        description: str,
        slider_value: ft.OptionalNumber,
        slider_min: ft.OptionalNumber,
        slider_max: ft.OptionalNumber,
        on_change_end: ft.OptionalControlEventCallable,
        slider_label: Optional[str] = None,
        slider_divisions: Optional[int] = None,
    ) -> None:
        self._description: str = description
        self._slider_value: ft.OptionalNumber = slider_value
        self._slider_min: ft.OptionalNumber = slider_min
        self._slider_max: ft.OptionalNumber = slider_max
        self._on_change_end: ft.OptionalControlEventCallable = on_change_end
        self._slider_divisions: Optional[int] = slider_divisions
        self._slider_label: Optional[str] = slider_label

        # Descriptive text above the slider
        self._description_label: ft.Text = ft.Text(
            value=self._description,
            theme_style=ft.TextThemeStyle.TITLE_SMALL,
            weight=ft.FontWeight.W_500,
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.ON_SURFACE_VARIANT,
        )

        # Slider widget
        self._slider: ft.Slider = ft.Slider(
            value=self._slider_value,
            min=self._slider_min,
            max=self._slider_max,
            divisions=self._slider_divisions,
            label=self._slider_label,
            on_change_end=self._on_change_end,
            expand=True,
        )

    def build(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[self._description_label, self._slider],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            padding=10,
        )
