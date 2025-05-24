import uuid
from typing import Optional

import flet as ft  # type:ignore[import-untyped]

from env.classes.database import DatabaseHandler
from env.classes.router import Router
from env.classes.widgets import Contact
from env.config import config
from env.func.get_session_key import get_key_or_default


class ContactsPage:
    def __init__(
        self,
        page: ft.Page,
        router: Router,
    ) -> None:
        self._page: ft.Page = page
        self._router: Router = router
        self._database_handler: Optional[DatabaseHandler] = None

        # Chats list view
        self._list_view: ft.ListView = ft.ListView(
            controls=[],
            expand=True,
            spacing=10,
            padding=10,
        )

    def display_existing_contacts(self) -> None:
        self._database_handler = DatabaseHandler(
            page=self._page,
            key=get_key_or_default(
                page=self._page, key_name=config.CS_SESSION_KEY, default=b""
            ),
            iv=get_key_or_default(
                page=self._page, key_name=config.CS_PASSWORD_IV, default=b""
            ),
        )

        self._database_handler.retrieve_contacts()

    def _remove_contact(self, contact_name: str) -> None:
        raise NotImplementedError("This function is not implemented yet!")

    def _add_contact(self) -> None:
        username_field: ft.TextField = ft.TextField(label="Username", autofocus=True)
        description_field: ft.TextField = ft.TextField(label="User Description")
        dialog: ft.AlertDialog = ft.AlertDialog(
            title=ft.Text("Add Contact"),
            content=ft.Column(
                controls=[username_field, description_field],
                tight=True,
            ),
            actions=[
                ft.TextButton(
                    "Add",
                    on_click=lambda e: self._on_add_contact_submit(
                        username=str(username_field.value),
                        user_description=str(description_field.value),
                        dialog=dialog,
                    ),
                ),
                ft.TextButton(
                    "Cancel",
                    on_click=lambda e: self._page.close(dialog),
                ),
            ],
        )
        self._page.open(dialog)
        self._page.update()  # type:ignore

    def _on_add_contact_submit(
        self, username: str, user_description: str, dialog: ft.AlertDialog
    ) -> None:
        if not username:
            return

        self._list_view.controls.append(
            Contact(
                page=self._page,
                router=self._router,
                username=username,
                description=user_description,
                contact_uid=str(uuid.uuid4()),  # Generate a unique ID for the contact
            ).build()
        )
        dialog.open = False
        self._page.update()  # type:ignore

    def build(self) -> ft.Container:
        return ft.Container(
            content=ft.Stack(
                controls=[
                    # List and title column (scrollable)
                    ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        "ChatLex", size=30, weight=ft.FontWeight.BOLD
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            self._list_view,
                        ],
                        expand=True,
                    ),
                    # Overlay FABs in bottom-right corner
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.FloatingActionButton(
                                    icon=ft.Icons.PERSON_ADD_ALT_1_ROUNDED,
                                    tooltip="Add Contact",
                                    on_click=lambda e: self._add_contact(),
                                ),
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.END,
                        ),
                        alignment=ft.alignment.bottom_right,
                        margin=10,
                        right=0,
                        bottom=0,
                    ),
                ],
            ),
            border_radius=8,
            padding=20,
            expand=True,
        )
