import flet as ft  # type:ignore[import-untyped]

from env.app.widgets.container import MasterContainer
from env.app.widgets.top_bars import SubPageTopBar
from env.classes.router import AppRouter
from env.classes.storages import Storages


class UserProfilePage:
    def __init__(
        self,
        page: ft.Page,
        router: AppRouter,
        storages: Storages,
    ) -> None:
        self._page: ft.Page = page
        self._router: AppRouter = router
        self._storages: Storages = storages

        # TODO: Add statistics and about section!

    def build(self) -> ft.Container:
        return MasterContainer(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            SubPageTopBar(
                                page=self._page,
                                router=self._router,
                                storages=self._storages,
                                title="Your Profile",
                            ).build(),
                            ft.Text("TEST"),
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
        )


# TODO: Add 'ContactProfilePage'!
