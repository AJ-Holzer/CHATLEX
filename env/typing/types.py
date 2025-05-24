from enum import Enum
from typing import Any, Callable, Optional, TypedDict

import flet as ft  # type:ignore[import-untyped]


class SenderType(str, Enum):
    SELF = "self"
    OTHER = "other"


class ContactType(TypedDict):
    user_uid: str
    username: str
    description: str
    ip: str


class PageContent(TypedDict):
    title: str
    content: list[ft.Control]
    start_function: Optional[Callable[..., Any]]
    function_args: Optional[dict[str, Any]]


# Define
SitePages = dict[str, PageContent]
