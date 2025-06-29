import uuid
from typing import Optional, cast

import flet as ft  # type:ignore[import-untyped]

from env.app.widgets.contact import ContactWidget
from env.app.widgets.container import MasterContainer
from env.app.widgets.top_bars import TopBar
from env.classes.database import SQLiteDatabase
from env.classes.encryption import AES_CBC
from env.classes.router import AppRouter
from env.classes.storages import Storages
from env.classes.translations import Translator
from env.config import config
from env.func.converter import str_to_byte
from env.func.validations import is_valid_onion_address
from env.typing.dicts import ContactData


class ContactsPage:
    def __init__(
        self,
        page: ft.Page,
        storages: Storages,
        router: AppRouter,
        translator: Translator,
    ) -> None:
        self._page: ft.Page = page
        self._storages: Storages = storages
        self._router: AppRouter = router
        self._translator: Translator = translator

        # Initialize top bar
        self._top_bar: TopBar = TopBar(
            page=self._page,
            router=self._router,
            storages=self._storages,
            translator=self._translator,
        )

        # Contacts list
        self._contacts_list: ft.ListView = ft.ListView(controls=[], expand=True)

        # Buttons
        self._add_contact_button: ft.Control = self._translator.wrap_control(
            route=config.ROUTE_CONTACTS,
            control_name="add-contact-button",
            control=ft.FloatingActionButton(
                icon=ft.Icons.PERSON_ADD_ALT_1_ROUNDED,
                on_click=lambda _: self._open_contact_alert(),
            ),
        )

        # Snack bar
        self._add_contact_error_label: ft.Control = self._translator.wrap_control(
            route=config.ROUTE_CONTACTS,
            control_name="add-contact-error-label",
            control=ft.Text(text_align=ft.TextAlign.CENTER),
        )
        self._add_contact_error_snackbar: ft.SnackBar = ft.SnackBar(
            content=self._add_contact_error_label,
            duration=10_000,  # Show for 10 seconds
            dismiss_direction=ft.DismissDirection.HORIZONTAL,
        )

        # Define types for encryptor and database
        self._aes_encryptor: AES_CBC

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
        except:
            self._page.open(self._add_contact_error_snackbar)
            return

        # Close alert
        self._page.close(control=alert)

        # Add contact widget to list view
        self._add_contact(contact_data=contact_data)

        # Update page to apply changes
        self._page.update()  # type:ignore

    def _open_contact_alert(self) -> None:
        # Create entries
        # TODO: Make description entry scrollable!
        username_entry: ft.Control = self._translator.wrap_control(
            route=config.ROUTE_CONTACTS,
            control_name="username-entry",
            control=ft.TextField(autofocus=True),
        )
        description_entry: ft.Control = self._translator.wrap_control(
            route=config.ROUTE_CONTACTS,
            control_name="description-entry",
            control=ft.TextField(
                multiline=True,
                max_lines=None,
            ),
        )
        description_container: ft.Container = ft.Container(
            content=ft.Column(
                controls=[description_entry],
                scroll=ft.ScrollMode.AUTO,
            ),
        )
        onion_address_entry: ft.Control = self._translator.wrap_control(
            route=config.ROUTE_CONTACTS,
            control_name="onion-address-entry",
            control=ft.TextField(
                suffix_text=".onion",
            ),
        )

        # Open the alert
        alert: ft.AlertDialog = ft.AlertDialog(
            title=self._translator.wrap_control(
                route=config.ROUTE_CONTACTS,
                control_name="add-contact-label",
                control=ft.Text(),
            ),
            content=ft.Column(
                controls=[username_entry, description_container, onion_address_entry],
                tight=True,
            ),
            actions=[
                # Cancel button
                self._translator.wrap_control(
                    route=config.ROUTE_CONTACTS,
                    control_name="add-contact-alert-cancel-button",
                    control=ft.TextButton(
                        on_click=lambda _: self._page.close(alert),
                    ),
                ),
                # Add button
                self._translator.wrap_control(
                    route=config.ROUTE_CONTACTS,
                    control_name="add-contact-alert-add-button",
                    control=ft.TextButton(
                        on_click=lambda _: self._on_add_contact_submit(
                            username=str(cast(ft.TextField, username_entry).value),
                            description=cast(ft.TextField, description_entry).value,
                            onion_address=str(
                                cast(ft.TextField, onion_address_entry).value
                            ),
                            alert=alert,
                        ),
                    ),
                ),
            ],
        )
        self._page.open(alert)
        self._page.update()  # type:ignore

    def _add_contact(self, contact_data: ContactData) -> None:
        # Create new contact widget
        contact_widget: ContactWidget = ContactWidget(
            page=self._page,
            contact_data=contact_data,
            router=self._router,
            contacts_list=self._contacts_list,
            aes_encryptor=self._aes_encryptor,
        )

        # Add contact widget
        self._contacts_list.controls.append(contact_widget.build())

    def _initialize_aes_encryptor(self) -> None:
        # Initialize AES_CBC encryptor
        self._aes_encryptor = AES_CBC(
            derived_key=str_to_byte(
                data=self._storages.session_storage.get(key=config.SS_USER_SESSION_KEY)
            ),
            salt=self._storages.client_storage.get(key=config.CS_USER_SALT),
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
                            controls=[self._add_contact_button],
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
