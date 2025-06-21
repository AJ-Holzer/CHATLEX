import flet as ft  # type:ignore[import-untyped]


class Section:
    def __init__(self, title: str, content: list[ft.Control]) -> None:
        # Create section
        self._title: ft.Container = ft.Container(
            content=ft.Text(
                value=title,
                expand=True,
                text_align=ft.TextAlign.CENTER,
                theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
            ),
            expand=True,
            padding=ft.Padding(left=20, top=20, right=20, bottom=0),
        )
        self._divider: ft.Container = ft.Container(
            ft.Divider(),
            padding=ft.Padding(left=30, top=0, right=30, bottom=0),
        )
        self._content: ft.Container = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=content,
                        expand=True,
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    ),
                ],
                expand=True,
            ),
            expand=True,
            padding=ft.Padding(left=20, top=0, right=20, bottom=20),
        )

    def build(self) -> ft.Container:
        return ft.Container(
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            self._title,
                            self._divider,
                            self._content,
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    ),
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            border=ft.border.all(
                width=1,
                color=ft.Colors.PRIMARY,
            ),
            border_radius=15,
            expand=True,
        )
