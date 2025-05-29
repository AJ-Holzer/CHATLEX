from typing import Optional

import flet as ft  # type:ignore[import-untyped]

from env.app.widgets.container import MasterContainer
from env.classes.app_storage import Storages
from env.classes.router import AppRouter
from env.config import config


class ContactsPage:
    def __init__(self, page: ft.Page, storages: Storages, router: AppRouter) -> None:
        self._page: ft.Page = page
        self._storages: Storages = storages
        self._router: AppRouter = router

    def load_contacts(self) -> None:
        pass

    def build(self) -> ft.Container:
        return MasterContainer(content=ft.Row(controls=ft.Column(controls=[])))
