import flet as ft  # type: ignore

class Themes:
    LIGHT: ft.Theme = ft.Theme(
        color_scheme_seed=ft.Colors.PURPLE,
        use_material3=True,
    )

    DARK: ft.Theme = ft.Theme(
        color_scheme_seed=ft.Colors.PURPLE,
        use_material3=True,
    )


themes: Themes = Themes()
