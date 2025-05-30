import flet as ft  # type:ignore[import-untyped]

from env.classes.contact import Contact
from env.classes.router import AppRouter


class ContactWidget:
    def __init__(self, contact_uuid: str, router: AppRouter) -> None:
        self._user: Contact = Contact(contact_uuid=contact_uuid)
        self._router: AppRouter = router

    def build(self) -> ft.Container:
        # TODO: Add missing code!
        return ft.Container()
