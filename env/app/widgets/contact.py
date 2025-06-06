import flet as ft  # type:ignore[import-untyped]

from env.classes.contact import Contact
from env.classes.database import SQLiteDatabase
from env.classes.encryption import AES
from env.classes.router import AppRouter
from env.config import config
from env.typing.actions import ContactAction
from env.typing.dicts import ContactData


class ContactWidget:
    def __init__(
        self,
        page: ft.Page,
        contact_data: ContactData,
        router: AppRouter,
        contacts_list: ft.ReorderableListView,
        aes_encryptor: AES,
    ) -> None:
        self._page: ft.Page = page
        self._contact: Contact = Contact(contact_data=contact_data)
        self._router: AppRouter = router
        self._contacts_list: ft.ReorderableListView = contacts_list
        self._aes_encryptor: AES = aes_encryptor

        # Initialize icon
        self._icon_background: ft.CircleAvatar = ft.CircleAvatar(
            content=ft.Text(value=self._contact.initials),
            max_radius=17,
            bgcolor=ft.Colors.PURPLE_900,
            color=ft.Colors.WHITE,
        )
        self._icon_online_indicator: ft.CircleAvatar = ft.CircleAvatar(
            bgcolor=(
                config.COLOR_ONLINE if self._contact.is_online else config.COLOR_OFFLINE
            ),
            radius=5,
        )
        self._icon: ft.Stack = ft.Stack(
            controls=[
                self._icon_background,
                ft.Container(
                    content=self._icon_online_indicator,
                    alignment=ft.alignment.bottom_left,
                    margin=ft.margin.only(left=0, bottom=0),  # Ensure no margin offsets
                    expand=False,
                ),
            ],
            alignment=ft.alignment.bottom_left,
        )

        # Initialize text label
        self._text_label: ft.Text = ft.Text(value=self._contact.username)

        self._contact_widget: ft.Container = ft.Container(
            content=ft.Row(
                controls=[
                    self._icon,
                    self._text_label,
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=10,
            alignment=ft.alignment.center_left,
            on_click=self._open_chat,
            on_long_press=self.open_action_menu,
        )

    def _open_chat(self, e: ft.ControlEvent) -> None:
        # TODO: Add open chat logic here!
        # TODO: Load messages, open chat and load contact info
        raise NotImplementedError("Function not implemented yet!")

    def _rm_contact(self, alert: ft.AlertDialog):
        # Initialize new database instance to avoid thread error (not in the same thread)
        db: SQLiteDatabase = SQLiteDatabase(aes_encryptor=self._aes_encryptor)

        self._page.close(alert)
        self._contacts_list.controls.remove(self._contact_widget)
        self._contacts_list.update()

        db.delete_contact(contact_uuid=self._contact.contact_uuid)

    def _remove_contact(self) -> None:
        alert: ft.AlertDialog = ft.AlertDialog(
            title=ft.Text("Delete Contact"),
            content=ft.Text(
                value=(
                    f"Are you sure you want to delete '{self._contact.username}' and all of its messages?\n"
                    f"This action can NOT be undone!"
                )
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self._page.close(alert)),
                ft.TextButton(
                    "Delete",
                    on_click=lambda _: self._rm_contact(alert),
                ),
            ],
        )
        self._page.open(alert)

    def _update_contact(self) -> None:
        db: SQLiteDatabase = SQLiteDatabase(aes_encryptor=self._aes_encryptor)

        db.update_contact(
            contact_uuid=self._contact.contact_uuid,
            contact_data=self._contact.contact_data,
        )

    def open_action_menu(self, e: ft.ControlEvent) -> None:
        def handle_click(action: ContactAction) -> None:
            def update_sheet(
                action_sheet: ft.CupertinoActionSheetAction,
                text: str,
            ) -> None:
                # Update the label of the given action sheet button
                if hasattr(action_sheet, "content") and isinstance(
                    action_sheet.content, ft.Text
                ):
                    action_sheet.content.value = text
                    action_sheet.content.update()
                action_sheet.update()

            match action:
                case ContactAction.RENAME:
                    # TODO: Add an alert to ask for the new username
                    pass

                case ContactAction.DELETE:
                    self._remove_contact()

                case ContactAction.CANCEL:
                    self._page.close(bottom_sheet)

                case ContactAction.MUTE:
                    update_sheet(action_sheet=button_mute_unmute, text="Unmute")
                    button_mute_unmute.update()

                    self._contact.is_muted = True
                    self._update_contact()

                case ContactAction.UNMUTE:
                    update_sheet(action_sheet=button_mute_unmute, text="Mute")
                    button_mute_unmute.update()

                    self._contact.is_muted = False
                    self._update_contact()

                case ContactAction.BLOCK:
                    update_sheet(action_sheet=button_block_unblock, text="Unblock")
                    button_block_unblock.disabled = True
                    button_block_unblock.update()

                    self._contact.is_blocked = True
                    self._update_contact()

                case ContactAction.UNBLOCK:
                    update_sheet(action_sheet=button_block_unblock, text="Block")
                    button_block_unblock.disabled = True
                    button_mute_unmute.update()

                    self._contact.is_blocked = False
                    self._update_contact()
                    pass

                case _:
                    raise ValueError(f"Action '{action.value}' not available!")

            action_alert.update()

        button_rename: ft.CupertinoActionSheetAction = ft.CupertinoActionSheetAction(
            content=ft.Text("Rename"),
            on_click=lambda _: handle_click(action=ContactAction.RENAME),
        )
        button_mute_unmute: ft.CupertinoActionSheetAction = (
            ft.CupertinoActionSheetAction(
                content=ft.Text(("Mute" if not self._contact.is_muted else "Unmute")),
                on_click=lambda _: handle_click(
                    action=(
                        ContactAction.MUTE
                        if not self._contact.is_muted
                        else ContactAction.UNMUTE
                    )
                ),
            )
        )
        button_block_unblock: ft.CupertinoActionSheetAction = (
            ft.CupertinoActionSheetAction(
                content=ft.Text("Block" if not self._contact.is_blocked else "Unblock"),
                on_click=lambda _: handle_click(
                    action=(
                        ContactAction.BLOCK
                        if not self._contact.is_blocked
                        else ContactAction.UNBLOCK
                    )
                ),
            )
        )
        button_delete: ft.CupertinoActionSheetAction = ft.CupertinoActionSheetAction(
            content=ft.Text("Delete"),
            is_destructive_action=True,
            on_click=lambda _: handle_click(action=ContactAction.DELETE),
        )

        # Create action alert
        action_alert: ft.CupertinoActionSheet = ft.CupertinoActionSheet(
            title=ft.Row(
                controls=[
                    ft.Text(
                        f"Actions for '{self._contact.username}'",
                        weight=ft.FontWeight.BOLD,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            cancel=ft.CupertinoActionSheetAction(
                content=ft.Text("Cancel"),
                on_click=lambda _: handle_click(action=ContactAction.CANCEL),
                is_default_action=True,
            ),
            actions=[
                # Rename
                button_rename,
                # Mute/Unmute
                button_mute_unmute,
                # Block/Unblock
                button_block_unblock,
                # Delete
                button_delete,
            ],
        )

        bottom_sheet: ft.BottomSheet = ft.BottomSheet(content=action_alert)
        self._page.open(bottom_sheet)

    def build(self) -> ft.Container:
        return self._contact_widget
