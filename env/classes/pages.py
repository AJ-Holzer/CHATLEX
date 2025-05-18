# import flet as ft  # type:ignore[import-untyped]

# # Classes
# from env.classes.widgets import MsgBubble

# # Types
# from env.typing.types import SenderType

# class Chat:
#     def __init__(self) -> None:
#         self._msg_list: ft.ListView = ft.ListView(
#             controls=[],
#             padding=5,
#             auto_scroll=False,
#             expand=True,
#         )
        
#     def load_msgs(self) -> None:
#         raise NotImplementedError("This function is not implemented yet!")
    
#     def create_msg_bubble(self, sender: SenderType, msg: str, timestamp: float) -> None:
#         self._msg_list.controls.append(MsgBubble(sender=sender, message=msg, timestamp=timestamp).build())

#     def build(self) -> ft.Container:
#         return ft.Container(
#             expand=True,
#             padding=20,
#             content=ft.Column(
#                 horizontal_alignment=ft.CrossAxisAlignment.START,
#                 spacing=20,
#                 controls=[self._msg_list]
#             )
#         )
