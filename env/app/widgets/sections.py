import flet as ft  # type:ignore[import-untyped]

from env.classes.translations import Translator


class Section:
    def __init__(
        self,
        translator: Translator,
        title: str,
        content: list[ft.Control],
    ) -> None:
        self._translator: Translator = translator
        self._title: ft.Container = ft.Container(
            content=translator.wrap_control(
                route=f"/section/{title}",
                control_name="title",
                control=ft.Text(
                    value=title,
                    expand=True,
                    text_align=ft.TextAlign.CENTER,
                    theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                ),
            ),
            expand=True,
            padding=ft.Padding(left=20, top=20, right=20, bottom=0),
        )
        self._content: list[ft.Control] = content

        # Create divider
        self._divider: ft.Container = ft.Container(
            ft.Divider(color=ft.Colors.PRIMARY),
            padding=ft.Padding(left=30, top=0, right=30, bottom=0),
        )

        # Create content
        self._section_content: ft.Container = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            (
                                item
                                if i == len(content) - 1
                                else ft.Column([item, ft.Divider()])
                            )
                            for i, item in enumerate(content)
                        ],
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
                            self._section_content,
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
                color=ft.Colors.with_opacity(0.5, ft.Colors.PRIMARY),
            ),
            border_radius=15,
            expand=True,
        )
