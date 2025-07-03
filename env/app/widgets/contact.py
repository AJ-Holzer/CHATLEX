import flet as ft  # type: ignore[import-untyped]

from env.classes.contact import Contact
from env.classes.database import SQLiteDatabase
from env.classes.encryption import AES_CBC
from env.classes.router import AppRouter
from env.classes.translate import Translator
from env.config import config
from env.typing.actions import ContactAction
from env.typing.dicts import ContactData


class ContactWidget:
    def __init__(
        self,
        page: ft.Page,
        translator: Translator,
        contact_data: ContactData,
        router: AppRouter,
        contacts_list: ft.ListView,
        aes_encryptor: AES_CBC,
    ) -> None:
        self._page: ft.Page = page
        self._translator: Translator = translator
        self._contact: Contact = Contact(contact_data=contact_data)
        self._router: AppRouter = router
        self._contacts_list: ft.ListView = contacts_list
        self._aes_encryptor: AES_CBC = aes_encryptor

        # Initialize status icons
        self._muted_icon: ft.Icon = ft.Icon(
            name=ft.Icons.VOLUME_OFF,
            visible=self._contact.is_muted and not self._contact.is_blocked,
            tooltip=self._translator.t(key="contact_widget.muted_icon"),
        )
        self._blocked_icon: ft.Icon = ft.Icon(
            name=ft.Icons.BLOCK,
            visible=self._contact.is_blocked,
            tooltip=self._translator.t(key="contact_widget.blocked_icon"),
        )

        # Initialize icon
        self._icon_background: ft.CircleAvatar = ft.CircleAvatar(
            content=ft.Text(value=self._contact.initials, size=15),
            max_radius=20,
            bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.PRIMARY),
            color=ft.Colors.ON_PRIMARY,
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
        self._username_label: ft.Text = ft.Text(value=self._contact.username)

        # Finalize contact widget
        self._contact_widget: ft.Container = ft.Container(
            content=ft.Row(
                controls=[
                    self._icon,
                    self._username_label,
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                self._muted_icon,
                                self._blocked_icon,
                            ],
                            spacing=5,
                            alignment=ft.MainAxisAlignment.END,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        expand=True,
                        alignment=ft.alignment.center_right,
                    ),
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
            title=ft.Text(self._translator.t(key="contact_widget.remove_alert.title")),
            content=ft.Text(
                value=self._translator.t(
                    key="contact_widget.remove_alert.content",
                    username=self._contact.username,
                )
            ),
            actions=[
                ft.TextButton(
                    text=self._translator.t(
                        key="contact_widget.remove_alert.cancel_button"
                    ),
                    on_click=lambda e: self._page.close(alert),
                ),
                ft.TextButton(
                    text=self._translator.t(
                        key="contact_widget.remove_alert.delete_button"
                    ),
                    on_click=lambda _: self._rm_contact(alert),
                ),
            ],
        )
        self._page.open(alert)

    def _refresh_status_icons(self) -> None:
        self._muted_icon.visible = (
            self._contact.is_muted and not self._contact.is_blocked
        )
        self._blocked_icon.visible = self._contact.is_blocked

        self._muted_icon.update()
        self._blocked_icon.update()

    def _update_database(self) -> None:
        db: SQLiteDatabase = SQLiteDatabase(aes_encryptor=self._aes_encryptor)

        db.update_contact(
            contact_uuid=self._contact.contact_uuid,
            contact_data=self._contact.contact_data,
        )

    def refresh_widget(self) -> None:
        self._contact_widget.update()
        self._muted_icon.update()
        self._blocked_icon.update()

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

            def on_rename() -> None:
                new_username: str = str(username_entry.value)
                if not new_username:
                    return

                self._contact.username = new_username
                self._update_database()
                self._page.close(username_alert)

                # Update icon and username label
                self._username_label.value = new_username
                if isinstance(self._icon_background.content, ft.Text):
                    self._icon_background.content.value = self._contact.initials
                    self._icon_background.update()
                self._username_label.update()

            match action:
                case ContactAction.RENAME:
                    username_entry: ft.TextField = ft.TextField(
                        label=self._translator.t(
                            key="contact_widget.username_entry",
                        ),
                        value=self._contact.username,
                        autofocus=True,
                    )

                    username_alert: ft.AlertDialog = ft.AlertDialog(
                        title=ft.Text(
                            value=self._translator.t(
                                key="contact_widget.rename_action_alert.title",
                                username=self._contact.username,
                            )
                        ),
                        content=username_entry,
                        actions=[
                            # Cancel button
                            ft.TextButton(
                                text=self._translator.t(
                                    key="contact_widget.rename_action_alert.cancel_button",
                                ),
                                on_click=lambda _: self._page.close(username_alert),
                            ),
                            # Proceed button
                            ft.TextButton(
                                text=self._translator.t(
                                    key="contact_widget.rename_action_alert.proceed_button",
                                ),
                                on_click=lambda _: on_rename(),
                            ),
                        ],
                    )

                    self._page.open(username_alert)

                case ContactAction.DELETE:
                    self._remove_contact()

                case ContactAction.CANCEL:
                    self._page.close(bottom_sheet)

                case ContactAction.TOGGLE_MUTE:
                    self.muted = not self._contact.is_muted

                    update_sheet(
                        action_sheet=button_toggle_mute,
                        text=(
                            self._translator.t(
                                key="contact_widget.mute_button",
                            )
                            if not self._contact.is_muted
                            else self._translator.t(
                                key="contact_widget.unmute_button",
                            )
                        ),
                    )
                    button_toggle_mute.update()

                    self._update_database()

                case ContactAction.TOGGLE_BLOCK:
                    self.blocked = not self._contact.is_blocked

                    # Update opacity of mute action to visualize if the action is clickable
                    button_toggle_mute.opacity = (
                        0.5 if self._contact.is_blocked else 1.0
                    )

                    update_sheet(
                        action_sheet=button_toggle_block,
                        text=(
                            self._translator.t(
                                key="contact_widget.block_button",
                            )
                            if not self._contact.is_blocked
                            else self._translator.t(
                                key="contact_widget.unblock_button",
                            )
                        ),
                    )
                    button_toggle_mute.disabled = (
                        True if self._contact.is_blocked else False
                    )
                    button_toggle_mute.update()

                    self._update_database()

                case _:
                    raise ValueError(f"Action '{action.value}' not available!")

            self.refresh_widget()

        # Create buttons
        button_rename: ft.CupertinoActionSheetAction = ft.CupertinoActionSheetAction(
            content=ft.Text(
                self._translator.t(
                    key="contact_widget.rename_button",
                    username=self._contact.username,
                )
            ),
            on_click=lambda _: handle_click(action=ContactAction.RENAME),
        )
        button_toggle_mute: ft.CupertinoActionSheetAction = (
            ft.CupertinoActionSheetAction(
                content=ft.Text(
                    self._translator.t(
                        key="contact_widget.mute_button",
                        username=self._contact.username,
                    )
                    if not self._contact.is_muted
                    else self._translator.t(
                        key="contact_widget.unmute_button",
                        username=self._contact.username,
                    )
                ),
                disabled=self._contact.is_blocked,
                on_click=lambda _: handle_click(action=ContactAction.TOGGLE_MUTE),
                opacity=0.5 if self._contact.is_blocked else 1.0,
            )
        )
        button_toggle_block: ft.CupertinoActionSheetAction = (
            ft.CupertinoActionSheetAction(
                content=ft.Text(
                    self._translator.t(
                        key="contact_widget.block_button",
                        username=self._contact.username,
                    )
                    if not self._contact.is_blocked
                    else self._translator.t(
                        key="contact_widget.unblock_button",
                        username=self._contact.username,
                    )
                ),
                on_click=lambda _: handle_click(action=ContactAction.TOGGLE_BLOCK),
            )
        )
        button_delete: ft.CupertinoActionSheetAction = ft.CupertinoActionSheetAction(
            content=ft.Text(
                self._translator.t(
                    key="contact_widget.delete_button",
                    username=self._contact.username,
                )
            ),
            is_destructive_action=True,
            on_click=lambda _: handle_click(action=ContactAction.DELETE),
        )

        # Create action alert
        action_alert: ft.CupertinoActionSheet = ft.CupertinoActionSheet(
            title=ft.Row(
                controls=[
                    ft.Text(
                        value=self._translator.t(
                            key="contact_widget.title",
                            username=self._contact.username,
                        ),
                        weight=ft.FontWeight.BOLD,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            cancel=ft.CupertinoActionSheetAction(
                content=ft.Text(
                    value=self._translator.t(
                        key="contact_widget.cancel_button",
                    )
                ),
                on_click=lambda _: handle_click(action=ContactAction.CANCEL),
                is_default_action=True,
            ),
            actions=[
                # Rename
                button_rename,
                # Mute/Unmute
                button_toggle_mute,
                # Block/Unblock
                button_toggle_block,
                # Delete
                button_delete,
            ],
        )

        bottom_sheet: ft.BottomSheet = ft.BottomSheet(content=action_alert)
        self._page.open(bottom_sheet)

    def build(self) -> ft.Container:
        return self._contact_widget

    @property
    def contact_uuid(self) -> str:
        return self._contact.contact_uuid

    @property
    def muted(self) -> bool:
        return self._contact.is_muted

    @muted.setter
    def muted(self, value: bool) -> None:
        self._contact.is_muted = value
        self._refresh_status_icons()

    @property
    def blocked(self) -> bool:
        return self._contact.is_blocked

    @blocked.setter
    def blocked(self, value: bool) -> None:
        self._contact.is_blocked = value
        self._refresh_status_icons()
