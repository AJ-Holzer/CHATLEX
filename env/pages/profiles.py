import flet as ft  # type: ignore[import-untyped]

from env.app.widgets.container import MasterContainer
from env.app.widgets.top_bars import SubPageTopBar
from env.classes.router import AppRouter
from env.classes.storages import Storages
from env.classes.translate import Translator


class UserProfilePage:
    def __init__(
        self,
        page: ft.Page,
        translator: Translator,
        router: AppRouter,
        storages: Storages,
    ) -> None:
        self._page: ft.Page = page
        self._translator: Translator = translator
        self._router: AppRouter = router
        self._storages: Storages = storages

        # TODO: Add statistics section!

    def build(self) -> ft.Container:
        return MasterContainer(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            SubPageTopBar(
                                page=self._page,
                                translator=self._translator,
                                router=self._router,
                                storages=self._storages,
                                title=self._translator.t(
                                    key="user_profile_page.top_bar"
                                ),
                            ).build(),
                            ft.Text("<TEST>"),
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
