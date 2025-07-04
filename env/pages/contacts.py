import uuid
from typing import Optional

import flet as ft  # type: ignore[import-untyped]

from env.app.widgets.contact import ContactWidget
from env.app.widgets.container import MasterContainer
from env.app.widgets.top_bars import TopBar
from env.classes.database import SQLiteDatabase
from env.classes.encryption import AES_256_GCM
from env.classes.router import AppRouter
from env.classes.storages import Storages
from env.classes.translate import Translator
from env.config import config
from env.func.converter import str_to_byte
from env.func.validations import is_valid_onion_address
from env.typing.dicts import ContactData


class ContactsPage:
    def __init__(
        self,
        page: ft.Page,
        translator: Translator,
        storages: Storages,
        router: AppRouter,
    ) -> None:
        self._page: ft.Page = page
        self._translator: Translator = translator
        self._storages: Storages = storages
        self._router: AppRouter = router
        self._top_bar: TopBar = TopBar(
            page=self._page,
            translator=self._translator,
            router=self._router,
            storages=self._storages,
            title=config.APP_TITLE,
        )

        # Contacts list
        # Use ReorderableListView to allow manual arrangement of contacts
        self._contacts_list: ft.ListView = ft.ListView(controls=[], expand=True)

        # Buttons
        self._add_user_button: ft.FloatingActionButton = ft.FloatingActionButton(
            icon=ft.Icons.PERSON_ADD_ALT_1_ROUNDED,
            tooltip=self._translator.t(key="contacts_page.add_user_button.tooltip"),
            on_click=lambda _: self._open_contact_alert(),
        )

        # Define types for encryptor and database
        self._aes_encryptor: AES_256_GCM

    def _on_add_contact_submit(
        self,
        username: str,
        description: Optional[str],
        onion_address: str,
        alert: ft.AlertDialog,
    ) -> None:
        # Add '.onion' suffix to onion address
        modified_onion_address: str = onion_address + ".onion"

        # Check if everything provided
        if not all([username, onion_address]):
            print(
                f"Username and onion address have to be provided to add contact! Got username='{username}', onion_address='{onion_address}'"
            )
            return

        # Check if onion address is valid
        if not is_valid_onion_address(addr=modified_onion_address):
            print(f"Onion address not valid! addr='{onion_address}'")
            return

        # Initialize new database instance to avoid thread error
        db: SQLiteDatabase = SQLiteDatabase(aes_encryptor=self._aes_encryptor)

        # Generate new random uuid
        contact_uuid: str = str(uuid.uuid4())

        # Define contact data
        contact_data: ContactData = {
            "contact_uuid": contact_uuid,
            "username": username,
            "description": description,
            "onion_address": modified_onion_address,
            "last_message_timestamp": None,
            "muted": False,
            "blocked": False,
        }

        # Insert contact into database
        try:
            db.insert_contact(contact_data=contact_data)
        except Exception as e:
            # Show the error
            self._page.open(
                ft.SnackBar(
                    content=ft.Text(
                        value=self._translator.t(
                            key="contacts_page.on_add_contact_submit.error",
                            e=e,
                        )
                    ),
                    duration=10_000,  # Show for 10 seconds
                    dismiss_direction=ft.DismissDirection.HORIZONTAL,
                )
            )
            return

        # Close alert
        self._page.close(control=alert)

        # Add contact widget to list view
        self._add_contact(contact_data=contact_data)

        # Update page to apply changes
        self._page.update()  # type: ignore

    def _open_contact_alert(self) -> None:
        # Create entries
        # TODO: Make description entry scrollable!
        username_entry: ft.TextField = ft.TextField(
            label=self._translator.t(
                key="contacts_page.add_contact_alert.username_entry"
            ),
            autofocus=True,
        )
        description_entry: ft.TextField = ft.TextField(
            label=self._translator.t(
                key="contacts_page.add_contact_alert.description_entry"
            ),
            multiline=True,
            max_lines=None,
            height=120,
        )
        description_container: ft.Container = ft.Container(
            content=ft.Column(
                controls=[description_entry],
                scroll=ft.ScrollMode.AUTO,
            ),
            height=120,
        )
        onion_address_entry: ft.TextField = ft.TextField(
            label=self._translator.t(
                key="contacts_page.add_contact_alert.onion_address_entry"
            ),
            suffix_text=".onion",
        )

        # Open the alert
        alert: ft.AlertDialog = ft.AlertDialog(
            title=ft.Text(
                value=self._translator.t(key="contacts_page.add_contact_alert.title")
            ),
            content=ft.Column(
                controls=[username_entry, description_container, onion_address_entry],
                tight=True,
            ),
            actions=[
                ft.TextButton(
                    text=self._translator.t(
                        key="contacts_page.add_contact_alert.cancel_button"
                    ),
                    on_click=lambda e: self._page.close(alert),
                ),
                ft.TextButton(
                    text=self._translator.t(
                        key="contacts_page.add_contact_alert.add_button"
                    ),
                    on_click=lambda _: self._on_add_contact_submit(
                        username=str(username_entry.value),
                        description=description_entry.value,
                        onion_address=str(onion_address_entry.value),
                        alert=alert,
                    ),
                ),
            ],
        )
        self._page.open(alert)
        self._page.update()  # type: ignore

    def _add_contact(self, contact_data: ContactData) -> None:
        # Create new contact widget
        contact_widget: ContactWidget = ContactWidget(
            page=self._page,
            translator=self._translator,
            contact_data=contact_data,
            router=self._router,
            contacts_list=self._contacts_list,
            aes_encryptor=self._aes_encryptor,
        )

        # Add contact widget
        self._contacts_list.controls.append(contact_widget.build())

    def _initialize_aes_encryptor(self) -> None:
        # Initialize AES_256_GCM encryptor
        self._aes_encryptor = AES_256_GCM(
            derived_key=str_to_byte(
                data=self._storages.session_storage.get(key=config.SS_USER_SESSION_KEY)
            ),
        )

    def _load_contacts(self) -> None:
        print("Loading contacts...")

        # Initialize a new database instance to avoid thread error
        db: SQLiteDatabase = SQLiteDatabase(aes_encryptor=self._aes_encryptor)

        # Empty contacts list to avoid duplicates
        self._contacts_list.controls.clear()

        # Retrieve contacts
        contacts: Optional[list[ContactData]] = db.retrieve_contacts()

        # Skip if no contacts
        if contacts is None:
            print("No contacts found!")
            return

        # Add contacts
        for contact_data in contacts:
            self._add_contact(contact_data=contact_data)

        # Update list view to apply changes
        self._contacts_list.update()

    def initialize(self) -> None:
        self._initialize_aes_encryptor()
        self._load_contacts()

    def build(self) -> ft.Container:
        return MasterContainer(
            content=ft.Stack(
                controls=[
                    ft.Row(
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
                    ft.Container(
                        content=ft.Column(
                            controls=[self._add_user_button],
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
            expand=True,
        )
