from enum import Enum


class ContactAction(Enum):
    DELETE = "delete"
    CANCEL = "cancel"
    RENAME = "rename"
    BLOCK = "block"
    UNBLOCK = "unblock"
    MUTE = "mute"
    UNMUTE = "unmute"
