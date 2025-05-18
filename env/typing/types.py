from enum import Enum


class SenderType(str, Enum):
    SELF = "self"
    OTHER = "other"
