import time
from typing import Any, Callable, Optional

import flet as ft  # type:ignore[import-untyped]

# Classes
from env.classes.faker import Faker

# Config
from env.config import config

# Func
from env.func.extractor import retrieve_initials
from env.func.get_session_key import get_key_or_default

# Types
from env.typing.types import SenderType

faker: Faker = Faker()


class SettingSwitch:
    """A switch control with a text label, built using Flutter widgets.

    Attributes:
        _page(ft.Page): The Flutter page where the switch is displayed.
        _txt(str): The text label for the switch.
        _state(bool): The current state (on/off) of the switch.
        _event(ft.OptionalControlEventCallable): An optional callback function triggered when the switch state changes.
        _text_widget(ft.Text): The Flutter Text widget displaying the label.
        _switch_widget(ft.CupertinoSwitch): The Flutter CupertinoSwitch widget.
    """

    def __init__(
        self,
        page: ft.Page,
        text: str,
        state: bool,
        event: ft.OptionalControlEventCallable,
    ) -> None:
        self._page: ft.Page = page
        self._txt: str = text
        self._state: bool = state
        self._event: ft.OptionalControlEventCallable = event

        self._text_widget: ft.Text = CText(
            page=self._page,
            value=self._txt,
        )

        self._switch_widget: ft.CupertinoSwitch = ft.CupertinoSwitch(
            value=self._state,
            on_change=self._event,
        )

    @property
    def state(self) -> bool:
        return self._switch_widget.value

    def build(self) -> ft.Container:
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=self._text_widget,
                        alignment=ft.alignment.center_left,
                        expand=True,
                    ),
                    ft.Container(
                        content=self._switch_widget,
                        alignment=ft.alignment.center_right,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        )


class CText(ft.Text):
    """Enhanced text element inheriting from ft.Text, bound to a specific ft.Page instance.  Provides convenient defaults for font settings based on page configuration.

    Attributes:
        _page(ft.Page): Reference to the ft.Page instance this text element belongs to.
        value(str): The text content of this element.
        color(Optional[ft.ColorValue]): Color of the text. Defaults to None.
    """

    def __init__(
        self,
        page: ft.Page,
        value: str = "",
        use_default_size: bool = True,
        size_deviation: int = 0,
        color: Optional[ft.ColorValue] = None,
        **kwargs: Any,
    ) -> None:
        font_family: str = get_key_or_default(
            page=page,
            default=config.FONT_FAMILY_DEFAULT,
            key_name=config.CS_FONT_FAMILY,
        )
        size: int = (
            get_key_or_default(
                page=page,
                default=config.FONT_SIZE_DEFAULT,
                key_name=config.CS_FONT_SIZE,
            )
            + size_deviation
        )
        kwargs["no_wrap"] = False
        kwargs["max_lines"] = None
        if "font_family" not in kwargs:
            kwargs["font_family"] = font_family
        if "size" not in kwargs:
            if use_default_size:
                kwargs["size"] = size
        super().__init__(value=value, color=color, **kwargs)  # type:ignore
        self._page: ft.Page = page


class Chat:
    """Represents a chat interface with message sending and display capabilities.

    Attributes:
        _username(str): Username associated with the chat.
        _contact_uid(str): Unique identifier of the contact in the chat.
        _page(ft.Page): Flutter page object on which the chat UI is rendered.
        _msg_list(ft.ListView): ListView to display chat messages.
        _msg_input(ft.TextField): TextField for user message input.
        _send_button(ft.IconButton): Button to send messages.
    """

    def __init__(self, username: str, contact_uid: str, page: ft.Page) -> None:
        self._username: str = username
        self._contact_uid: str = contact_uid
        self._page: ft.Page = page

        self._msg_list: ft.ListView = ft.ListView(
            controls=[],
            padding=5,
            auto_scroll=False,
            expand=True,  # allow ListView to take all available vertical space
        )

        # Create message input TextField
        self._msg_input = ft.TextField(
            expand=True,
            hint_text="Type a message...",
            multiline=True,
            min_lines=1,
            max_lines=5,
        )

        # Create send button
        self._send_button = ft.IconButton(
            icon=ft.Icons.SEND, on_click=self.send_message
        )

    def scroll_to_bottom(self, duration: int) -> None:
        self._msg_list.scroll_to(
            offset=-1, duration=duration, curve=ft.AnimationCurve.EASE_IN_OUT
        )

    def send_message(self, e: ft.ControlEvent) -> None:
        msg_text = str(self._msg_input.value).strip()
        if msg_text:
            self.create_msg_bubble(
                sender=SenderType.SELF, msg=msg_text, timestamp=time.time()
            )
            self._msg_input.value = ""  # clear input field
            self._msg_input.update()
            self._msg_list.update()

    def load_msgs(self) -> None:
        raise NotImplementedError("This function is not implemented yet!")

    def create_msg_bubble(self, sender: SenderType, msg: str, timestamp: float) -> None:
        self._msg_list.controls.append(
            MsgBubble(
                page=self._page, message=msg, timestamp=timestamp, sender=sender
            ).build()
        )
        self.scroll_to_bottom(duration=500)

    def build(self) -> ft.Container:
        return ft.Container(
            expand=True,
            padding=20,
            content=ft.Column(
                [
                    # Username at the top, centered and bold
                    ft.Row(
                        controls=[
                            CText(
                                page=self._page,
                                value=self._username,
                                size_deviation=4,
                                weight=ft.FontWeight.BOLD,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    self._msg_list,
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.ARROW_DOWNWARD,
                                tooltip="Scroll to bottom",
                                on_click=lambda e: self.scroll_to_bottom(duration=500),
                            )
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=5,
                    ),
                    ft.Row(
                        controls=[self._msg_input, self._send_button],
                        spacing=5,
                    ),
                ],
                expand=True,
            ),
        )


class MsgBubble:
    """Represents a message bubble in a chat interface.

    Attributes:
        _sender(SenderType): Indicates whether the message was sent by the user (SELF) or another sender.
        _message(str): The text content of the message.
        _timestamp(float): Timestamp indicating when the message was sent.
        _page(ft.Page): Flutter page object to render the message bubble.
        _bg_color(ft.ColorValue): Background color of the message bubble, determined by the sender.
        _alignment(ft.MainAxisAlignment): Alignment of the message bubble, determined by the sender.
    """

    def __init__(
        self,
        page: ft.Page,
        message: str,
        timestamp: float,
        sender: SenderType = SenderType.SELF,
    ) -> None:
        self._sender: SenderType = sender
        self._message: str = message
        self._timestamp: float = timestamp
        self._page: ft.Page = page

        # Determine alignment and color
        self._bg_color: ft.ColorValue = (
            config.SELF_SENDER_COLOR
            if self._sender == SenderType.SELF
            else config.OTHER_SENDER_COLOR
        )
        self._alignment = (
            ft.MainAxisAlignment.END
            if self._sender == SenderType.SELF
            else ft.MainAxisAlignment.START
        )

    def build(self) -> ft.Container:
        # The actual message container (80% of parent column)
        bubble = ft.Container(
            content=CText(page=self._page, value=self._message, color=ft.Colors.WHITE),
            bgcolor=self._bg_color,
            padding=10,
            border_radius=10,
            width=400 * 0.5,  # or dynamically: constraints or MediaQuery, if available
        )

        # Timestamp and optional sender name (currently only timestamp is used)
        metadata = CText(
            page=self._page,
            value=time.strftime("%Y-%m-%d %H:%M", time.localtime(self._timestamp)),
            size_deviation=-5,
            italic=True,
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(controls=[bubble], alignment=self._alignment),
                    ft.Row(controls=[metadata], alignment=self._alignment),
                ],
                spacing=5,
            ),
            padding=ft.padding.symmetric(vertical=5),
        )


class ContactInfo:
    """Represents contact information, including icon and username.

    Attributes:
        _contact_icon(ft.CircleAvatar): Contact's profile picture.
        _username(str): Contact's username.
        _contact_name(ft.Text): Contact's name displayed as text.
    """

    def __init__(self, page: ft.Page, icon: ft.CircleAvatar, username: str) -> None:
        self._page: ft.Page = page
        self._contact_icon: ft.CircleAvatar = icon
        self._username: str = username
        self._contact_name: ft.Text = CText(page=self._page, value=self._username)

        # Make contact icon bigger
        self._contact_icon.max_radius = 70
        self._contact_icon.radius = 70

    def build(self) -> ft.Container:
        # Ensure the contact name text wraps if it's too long
        self._contact_name.no_wrap = False
        self._contact_name.max_lines = None  # Allow unlimited lines

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            self._contact_icon,
                            self._contact_name,
                            ft.Placeholder(
                                expand=True,  # This allows the Placeholder to expand
                                content=CText(page=self._page, value="Contact Info"),
                                color=ft.Colors.ORANGE,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True,  # This allows the Column to expand within the Row
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            alignment=ft.alignment.center,
            padding=20,
            expand=True,
        )


class Contact:
    """Represents a contact in a contact list.

    Attributes:
        _page(ft.Page): The FlutterFlow page where the contact widget is displayed.
        _chat_tab(ft.Tab): The FlutterFlow tab for chat.
        _contact_info_tab(ft.Tab): The FlutterFlow tab for contact information.
        _contact_uid(str): Unique identifier for the contact.
        _icon_color(ft.ColorValue): Color of the contact icon.
        _icon_min_size(int): Minimum size of the contact icon.
        _is_online(bool): Indicates whether the contact is online.
        _padding(int): Padding around the contact widget.
        _text_widget(ft.Text): FlutterFlow text widget displaying the contact's username.
        _username(str): Username of the contact.
        _initials(str): Initials of the contact's username.
        tab_change_function(Callable[[int], None]): Function to switch between tabs.
        _icon_background(ft.CircleAvatar): Background of the contact icon.
        _icon_foreground(ft.CircleAvatar): Foreground of the contact icon (online/offline indicator).
        _icon(ft.Stack): Stack containing the contact icon.
        _container(ft.Container): Container holding the contact widget.
    """

    def __init__(
        self,
        page: ft.Page,
        username: str,
        contact_uid: str,
        tab_change_function: Callable[[int], None],
        chat_tab: ft.Tab,
        contact_info_tab: ft.Tab,
        icon: Optional[ft.CircleAvatar] = None,
        padding: int = 10,
        icon_min_size: int = 17,
        icon_color: ft.ColorValue = ft.Colors.PURPLE_900,
        is_online: bool = False,
    ) -> None:
        self._page: ft.Page = page
        self._chat_tab: ft.Tab = chat_tab
        self._contact_info_tab: ft.Tab = contact_info_tab
        self._contact_uid: str = contact_uid
        self._icon_color: ft.ColorValue = icon_color
        self._icon_min_size: int = icon_min_size
        self._is_online: bool = is_online
        self._padding: int = padding
        self._text_widget: ft.Text = CText(page=self._page, value=username)
        self._username: str = username
        self._initials: str = retrieve_initials(text=username)
        self.tab_change_function: Callable[[int], None] = tab_change_function

        self._icon_background: ft.CircleAvatar = icon or ft.CircleAvatar(
            content=CText(
                page=self._page, value=self._initials, use_default_size=False
            ),
            max_radius=icon_min_size,
            bgcolor=icon_color,
            color=ft.Colors.WHITE,
        )

        self._icon_foreground: ft.CircleAvatar = ft.CircleAvatar(
            bgcolor=config.COLOR_ONLINE if is_online else config.COLOR_OFFLINE, radius=5
        )

        self._icon: ft.Stack = ft.Stack(
            controls=[
                self._icon_background,
                ft.Container(
                    content=self._icon_foreground,
                    alignment=ft.alignment.bottom_left,
                ),
            ],
            width=40,
            height=40,
        )

    @property
    def is_online(self) -> bool:
        return self._is_online

    @is_online.setter
    def is_online(self, is_online: bool) -> None:
        self._is_online = is_online

        try:
            self._is_online = is_online
            self._icon_foreground.bgcolor = (
                ft.Colors.GREEN if is_online else ft.Colors.RED
            )
            self._icon.update()
        except Exception as e:
            print(f"Error updating contact status: {e}")

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, new_size: int) -> None:
        self._size = new_size
        self._text_widget.size = new_size
        self.update()

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, new_username: str) -> None:
        self._username = new_username
        self._text_widget.value = new_username
        self.update()

    @property
    def text_widget(self) -> ft.Text:
        return self._text_widget

    @property
    def padding(self) -> int:
        return self._padding

    @padding.setter
    def padding(self, new_padding: int) -> None:
        if not self._container:
            raise RuntimeError(
                "Cannot change padding before the Contact widget is built. "
                "Please call the 'build()' method before setting the padding."
            )

        self._padding = new_padding
        self._container.padding = new_padding
        self._container.update()

    @property
    def icon_min_size(self) -> int:
        return self._icon_min_size

    @icon_min_size.setter
    def icon_min_size(self, new_min_size: int) -> None:
        self._icon_min_size = new_min_size
        self._icon_background.min_radius = new_min_size
        self._icon.update()

    @property
    def icon_color(self) -> ft.ColorValue:
        return self._icon_color

    @icon_color.setter
    def icon_color(self, new_color: ft.ColorValue) -> None:
        self._icon_color = new_color
        self._icon_background.bgcolor = new_color
        self._icon.update()

    def update(self) -> None:
        self._text_widget.update()
        self._icon.update()

    def open_chat(self) -> None:
        print(f"Opening chat for user '{self._username}'.")

        # Switch to chat page
        self.tab_change_function(2)

        chat: Chat = Chat(
            username=self._username, contact_uid=self._contact_uid, page=self._page
        )
        self._chat_tab.content = chat.build()
        self._chat_tab.update()

        chat.scroll_to_bottom(duration=0)

    def create_contact_info_page(self) -> None:
        print(f"Creating contact page for user '{self._username}'.")

        # Create a new icon instead of reusing the original
        new_icon = ft.CircleAvatar(
            content=CText(
                page=self._page, value=retrieve_initials(text=self._username), size=50
            ),
            max_radius=100,
            bgcolor=self._icon_color,
            color=ft.Colors.WHITE,
        )

        contact_info: ContactInfo = ContactInfo(
            page=self._page, icon=new_icon, username=self._username
        )
        self._contact_info_tab.content = contact_info.build()
        self._contact_info_tab.update()

    def create_pages(self, e: ft.ControlEvent) -> None:
        self.create_contact_info_page()
        self.open_chat()

    def build(self) -> ft.Container:
        self._container = ft.Container(
            content=ft.Row(
                controls=[
                    self._icon,
                    self._text_widget,
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=self._padding,
            alignment=ft.alignment.center_left,
            on_click=self.create_pages,
        )

        return self._container


# TODO: Actually use the ContactsPage class, but only return the stuff, do not use the contacts_tab --> makes problems!!!
class ContactsPage:
    """Represents the contacts page in the application.

    Attributes:
        _page(ft.Page): The Flutter page object.
        _contacts_tab(ft.Tab): The tab for managing contacts.
        _available_contacts(Optional[list[Contact]]): List of available contacts to display.
        _contacts_lv(Optional[ft.ReorderableListView]): Reorderable list view to display contacts; None if no contacts are available.
        _tab_column(ft.Column): Column layout containing the contacts list view or message.
    """

    def __init__(
        self,
        page: ft.Page,
        contacts_tab: ft.Tab,
        available_contacts: Optional[list[Contact]] = None,
    ) -> None:
        self._page: ft.Page = page
        self._contacts_tab: ft.Tab = contacts_tab
        self._available_contacts: Optional[list[Contact]] = available_contacts
        self._contacts_lv: Optional[ft.ReorderableListView] = None

        if self._available_contacts:
            self._contacts_lv = ft.ReorderableListView(
                controls=[contact.build() for contact in self._available_contacts]
            )

        self._tab_column: ft.Column = ft.Column(
            controls=[
                ft.Container(
                    content=(
                        self._contacts_lv
                        if self._contacts_lv is not None
                        # Display the msg to create a database if no file exists
                        else CText(
                            page=self._page,
                            value="Consider to create a database file in the settings.\n\nOtherwise, you won't be able to add any contacts.",
                        )
                    ),
                    alignment=(None if self._contacts_lv else ft.alignment.center),
                    expand=True,
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=20,
            expand=True,
        )

    def build(self) -> ft.Container:
        return ft.Container(
            content=self._tab_column,
            padding=20,
            expand=True,
        )
