from enum import Enum


class ContactAction(Enum):
    DELETE = "delete"
    CANCEL = "cancel"
    RENAME = "rename"

    TOGGLE_MUTE = "toggle-mute"
    TOGGLE_BLOCK = "toggle-block"
