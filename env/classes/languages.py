import flet as ft  # type:ignore[import-untyped]


class Translator:
    def __init__(self, language: str) -> None:
        self._current_language: str = language

        # TODO: Init language and load it.
        raise NotImplementedError("This function is not implemented yet!")

    def add_control(self, key: str, flet_control: ft.Control) -> ft.Control:
        # TODO: Get value from json
        raise NotImplementedError("This function is not implemented yet!")

    def update_language(self, language: str) -> None:
        # TODO: Add language update logic (update controls)
        raise NotImplementedError("This function is not implemented yet!")
