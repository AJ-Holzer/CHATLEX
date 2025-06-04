import flet as ft  # type:ignore[import-untyped]

from env.classes.contact import Contact
from env.classes.router import AppRouter
from env.config import config
from env.typing.dicts import ContactData


class ContactWidget:
    def __init__(self, contact_data: ContactData, router: AppRouter) -> None:
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

    def _open_chat(self) -> None:
        # TODO: Add open chat logic here!
        # TODO: Load messages, open chat and load contact info
        raise NotImplementedError("Function not implemented yet!")

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
            on_click=lambda _: self._open_chat,
        )
