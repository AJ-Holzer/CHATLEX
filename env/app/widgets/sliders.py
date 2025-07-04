from typing import Optional

import flet as ft  # type: ignore[import-untyped]

from env.app.widgets.info import InfoAlert


class DescriptiveSlider:
    def __init__(
        self,
        page: ft.Page,
        description: str,
        slider_value: ft.OptionalNumber,
        slider_min: ft.OptionalNumber,
        slider_max: ft.OptionalNumber,
        on_change_end: ft.OptionalControlEventCallable,
        slider_label: Optional[str] = None,
        slider_divisions: Optional[int] = None,
        slider_default_value: Optional[ft.OptionalNumber] = None,
        help_title: Optional[str] = None,
        help_content: Optional[str] = None,
    ) -> None:
        self._page: ft.Page = page
        self._description: str = description
        self._slider_value: ft.OptionalNumber = slider_value
        self._slider_min: ft.OptionalNumber = slider_min
        self._slider_max: ft.OptionalNumber = slider_max
        self._on_change_end: ft.OptionalControlEventCallable = on_change_end
        self._slider_divisions: Optional[int] = slider_divisions
        self._slider_label: Optional[str] = slider_label
        self._slider_default_value: Optional[ft.OptionalNumber] = slider_default_value
        self._help_title: Optional[str] = help_title
        self._help_content: Optional[str] = help_content

        # Descriptive text above the slider
        self._description_label: ft.Text = ft.Text(
            value=self._description,
            theme_style=ft.TextThemeStyle.TITLE_SMALL,
            weight=ft.FontWeight.W_500,
            text_align=ft.TextAlign.START,
            no_wrap=False,
            max_lines=None,
        )

        # Create help alert
        self._help_alert: ft.AlertDialog = InfoAlert(
            title=self._help_title,
            content=self._help_content,
        ).build()

        # Show reset button only if default value is set
        self._reset_button: ft.IconButton = ft.IconButton(
            icon=ft.Icons.SETTINGS_BACKUP_RESTORE_ROUNDED,
            visible=True if self._slider_default_value is not None else False,
            on_click=lambda _: self._reset_value(),
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

    def _reset_value(self) -> None:
        if self._on_change_end:
            self._slider.value = self._slider_default_value
            self._on_change_end(
                ft.ControlEvent(
                    data=str(self._slider.value),
                    control=self._slider,
                    name="on_change_end",
                    page=self._page,
                    target=str(self._slider),
                )
            )

    def build(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Container(
                                            content=self._description_label,
                                            on_click=lambda _: (
                                                self._page.open(
                                                    control=self._help_alert
                                                )
                                                if self._help_title
                                                and self._help_content
                                                else None
                                            ),
                                        )
                                    ],
                                    expand=True,
                                ),
                                ft.Column(
                                    controls=[self._reset_button],
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            expand=True,
                        ),
                        padding=ft.Padding(left=25, top=0, right=20, bottom=0),
                        expand=True,
                    ),
                    self._slider,
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
        )

    @property
    def slider_value(self) -> float:
        return self._slider.value

    @slider_value.setter
    def slider_value(self, value: float | int) -> None:
        self._slider.value = value
