import flet as ft  # type:ignore[import-untyped]

from env.app.widgets.container import MasterContainer
from env.app.widgets.top_bar import TopBar
from env.classes.app_storage import Storages
from env.classes.router import AppRouter


class ContactsPage:
    def __init__(self, page: ft.Page, storages: Storages, router: AppRouter) -> None:
        self._page: ft.Page = page
        self._storages: Storages = storages
        self._router: AppRouter = router
        self._top_bar: TopBar = TopBar(router=self._router)

        # Contacts list
        self._contacts_list: ft.ListView = ft.ListView(
            controls=[],
            expand=True,
        )

    def _add_contact(
        self,
        username: str,
        contact_uid: str,
    ) -> None:
        pass

    def load_contacts(self) -> None:
        print("Loading contacts...")

    def build(self) -> ft.Container:
        return MasterContainer(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            self._top_bar.build(),
                            self._contacts_list,
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=True,
        )
