import flet as ft  # type:ignore[import-untyped]
import time
import random
from typing import Callable, Any, Optional

# Types
from env.typing.types import SenderType

# Func
from env.func.extractor import retrieve_initials

# # Classes
# from env.classes.pages import Chat

# Config
from env.config import config

class Chat:
    def __init__(self) -> None:
        self._msg_list: ft.ListView = ft.ListView(
            controls=[],
            padding=5,
            auto_scroll=True,
            expand=True  # allow ListView to take all available vertical space
        )
        
        for _ in range(2000):
            self.create_msg_bubble(sender=random.choice([SenderType.SELF, SenderType.OTHER]), msg="Hello World! " * 5, timestamp=time.time())
        
        # Create message input TextField
        self._msg_input = ft.TextField(expand=True, hint_text="Type a message...")
        
        # Create send button
        self._send_button = ft.IconButton(
            icon=ft.Icons.SEND,
            on_click=self.send_message
        )

    def scroll_to_bottom(self) -> None:        
        self._msg_list.scroll_to(offset=-1, duration=0, curve=ft.AnimationCurve.EASE_IN_OUT)

    def send_message(self, e: ft.ControlEvent) -> None:
        msg_text = str(self._msg_input.value).strip()
        if msg_text:
            self.create_msg_bubble(sender=SenderType.SELF, msg=msg_text, timestamp=time.time())
            self._msg_input.value = ""  # clear input field
            self._msg_input.update()
            self._msg_list.update()

    def load_msgs(self) -> None:
        raise NotImplementedError("This function is not implemented yet!")
    
    def create_msg_bubble(self, sender: SenderType, msg: str, timestamp: float) -> None:
        self._msg_list.controls.append(MsgBubble(sender=sender, message=msg, timestamp=timestamp).build())
    
    def build(self) -> ft.Container:
        return ft.Container(
            expand=True,
            padding=20,
            content=ft.Column(
            [
                self._msg_list,
                ft.Row(
                controls=[
                    ft.IconButton(
                    icon=ft.Icons.ARROW_DOWNWARD,
                    tooltip="Scroll to bottom",
                    on_click=lambda e: self.scroll_to_bottom(),
                    )
                ],
                alignment=ft.MainAxisAlignment.END,
                spacing=5,
                ),
                ft.Row(
                controls=[self._msg_input, self._send_button],
                spacing=5,
                )
            ],
            expand=True,
            ),
        )


class MsgBubble:
    def __init__(self, message: str, timestamp: float, sender: SenderType = SenderType.SELF) -> None:
        self._sender: SenderType = sender
        self._message: str = message
        self._timestamp: float = timestamp

        # Determine alignment and color
        self._bg_color: ft.ColorValue = (
            config.SELF_SENDER_COLOR if self._sender == SenderType.SELF else config.OTHER_SENDER_COLOR
        )

        self._alignment = ft.MainAxisAlignment.END if self._sender == SenderType.SELF else ft.MainAxisAlignment.START

    def build(self) -> ft.Container:
        # The actual message container (80% of parent column)
        bubble = ft.Container(
            content=ft.Text(self._message),
            bgcolor=self._bg_color,
            padding=10,
            border_radius=10,
            width=400 * 0.5,  # or dynamically: constraints or MediaQuery, if available
        )

        # Timestamp and optional sender name (currently only timestamp is used)
        metadata = ft.Text(
            time.strftime("%Y-%m-%d %H:%M", time.localtime(self._timestamp)),
            size=10,
            italic=True,
            color=ft.Colors.GREY,
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(controls=[bubble]  , alignment=self._alignment),
                    ft.Row(controls=[metadata], alignment=self._alignment)
                ],
                spacing=5,
            ),
            padding=ft.padding.symmetric(vertical=5),
        )

class Contact:
    def __init__(
        self,
        username: str,
        size: int,
        contact_uid: str,
        tab_change_function: Callable[[int], None],
        chat_tab: ft.Tab,
        contact_info_tab: ft.Tab,
        icon: Optional[ft.CircleAvatar] = None,
        padding: int = 10,
        icon_min_size: int = 17,
        icon_color: ft.ColorValue = ft.Colors.PURPLE_900,
        is_online: bool = False
    ) -> None:
        self._chat_tab          : ft.Tab                = chat_tab
        self._contact_info_tab  : ft.Tab                = contact_info_tab
        self._contact_uid       : str                   = contact_uid
        self._icon_color        : ft.ColorValue         = icon_color
        self._icon_min_size     : int                   = icon_min_size
        self._is_online         : bool                  = is_online
        self._padding           : int                   = padding
        self._size              : int                   = size
        self._text_widget       : ft.Text               = ft.Text(value=username, size=size)
        self._username          : str                   = username
        self.tab_change_function: Callable[[int], None] = tab_change_function

        self._icon_background  : ft.CircleAvatar  = (
            icon
            or ft.CircleAvatar(
                content=ft.Text(retrieve_initials(text=username)),
                color=ft.Colors.WHITE,
                max_radius=icon_min_size,
                bgcolor=icon_color,
            )
        )

        self._icon_foreground  : ft.CircleAvatar  = ft.CircleAvatar(
            bgcolor=config.COLOR_ONLINE if is_online else config.COLOR_OFFLINE,
            radius=5
        )

        self._icon             : ft.Stack         = ft.Stack(
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
            self._icon_foreground.bgcolor = ft.Colors.GREEN if is_online else ft.Colors.RED
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
        
    def open_chat(self, e: ft.ControlEvent) -> None:
        print(f"Opening chat for user '{self._username}'.")
        
        # Switch to chat page
        self.tab_change_function(2)
        
        chat: Chat = Chat()        
        self._chat_tab.content = chat.build()
        self._chat_tab.update()
        
        chat.scroll_to_bottom()
        
    def build(self) -> ft.Container:
        self._container =  ft.Container(
            content=ft.Row(
            controls=[
                self._icon,
                self._text_widget
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=self._padding,
            alignment=ft.alignment.center_left,
            on_click=self.open_chat
        )

        return self._container
