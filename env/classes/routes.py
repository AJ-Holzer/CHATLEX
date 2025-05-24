import flet as ft  # type:ignore[import-untyped]

from env.classes.pages import Router


class ContactsPage:
    def __init__(self, page: ft.Page, router: Router) -> None:
        self._page: ft.Page = page
        self._router: Router = router

    def _remove_contact(self, contact_name: str) -> None:
        raise NotImplementedError("This function is not implemented yet!")

    def _add_contact(
        self, contact_name: str, contact_info: str, ip_address: str
    ) -> None:
        raise NotImplementedError("This function is not implemented yet!")

    def build(self) -> ft.Container:
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text("ChatLex", bgcolor="red"),
                            ft.ListView(
                                controls=[],  # TODO: Add contacts here
                                expand=True,
                            ),
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
            ),
            expand=True,
            padding=20,
        )
