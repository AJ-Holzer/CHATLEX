import flet as ft  # type: ignore[import-untyped]


class SectionDropDown:
    def __init__(
        self,
        value: str,
        label: str,
        options: list[ft.dropdown.Option],
        on_change: ft.OptionalControlEventCallable,
    ) -> None:
        self._value: str = value
        self._label: str = label
        self._options: list[ft.dropdown.Option] = options
        self._on_change: ft.OptionalControlEventCallable = on_change

        # Create drop down menu
        self._drop_down: ft.Dropdown = ft.Dropdown(
            value=self._value,
            options=self._options,
            label=self._label,
            on_change=self._on_change,
            expand=True,
        )

    def build(self) -> ft.Container:
        return ft.Container(
            content=self._drop_down,
            padding=ft.Padding(left=20, top=0, right=20, bottom=0),
            expand=True,
        )
