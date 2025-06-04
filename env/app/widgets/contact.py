import flet as ft  # type:ignore[import-untyped]

from env.classes.contact import Contact
from env.classes.router import AppRouter
from env.config import config
from env.typing.actions import ContactAction
from env.typing.dicts import ContactData


class ContactWidget:
    def __init__(
        self, page: ft.Page, contact_data: ContactData, router: AppRouter
    ) -> None:
        self._page: ft.Page = page
        self._user: Contact = Contact(contact_data=contact_data)
        self._router: AppRouter = router

        # Initialize icon
        self._icon_background: ft.CircleAvatar = ft.CircleAvatar(
            content=ft.Text(value=self._user.initials),
            max_radius=17,
            bgcolor=ft.Colors.PURPLE_900,
            color=ft.Colors.WHITE,
        )
        self._icon_online_indicator: ft.CircleAvatar = ft.CircleAvatar(
            bgcolor=(
                config.COLOR_ONLINE if self._user.is_online else config.COLOR_OFFLINE
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
        self._text_label: ft.Text = ft.Text(value=self._user.username)

    def _open_chat(self, e: ft.ControlEvent) -> None:
        # TODO: Add open chat logic here!
        # TODO: Load messages, open chat and load contact info
        raise NotImplementedError("Function not implemented yet!")

    def open_action_menu(self, e: ft.ControlEvent) -> None:
        def handle_click(action: ContactAction) -> None:
            match action:
                case ContactAction.DELETE:
                    # TODO: Delete contact and remove it from the list
                    # TODO: Let the user confirm to make sure it hasn't been chosen by mistake
                    return
                case ContactAction.CANCEL:
                    self._page.close(bottom_sheet)  # Close alert
                    return
                case ContactAction.MUTE:
                    # TODO: Mute contact
                    return
                case ContactAction.RENAME:
                    # TODO: Rename contact
                    return
                case ContactAction.UNBLOCK:
                    # TODO: Unblock contact
                    return
                case ContactAction.BLOCK:
                    # TODO: Block contact
                    return
                case _:
                    raise ValueError(f"Action '{action.value}' not available!")

        action_alert: ft.CupertinoActionSheet = ft.CupertinoActionSheet(
            title=ft.Row(
                controls=[
                    ft.Text(
                        f"Actions for '{self._user.username}'",
                        weight=ft.FontWeight.BOLD,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            cancel=ft.CupertinoActionSheetAction(
                content=ft.Text("Cancel"),
                on_click=lambda _: handle_click(action=ContactAction.CANCEL),
            ),
            actions=[
                ft.CupertinoActionSheetAction(
                    content=ft.Text("Delete Contact"),
                    is_destructive_action=True,
                    on_click=lambda _: handle_click(action=ContactAction.DELETE),
                ),
            ],
        )

        bottom_sheet: ft.BottomSheet = ft.BottomSheet(content=action_alert)
        self._page.open(bottom_sheet)

        # # TODO: Add missing code!
        # raise NotImplementedError("This function is not implemented yet!")

    def build(self) -> ft.Container:
        return ft.Container(
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
