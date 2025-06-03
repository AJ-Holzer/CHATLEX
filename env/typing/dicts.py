from typing import Any, Callable, Optional, TypedDict

import flet as ft  # type:ignore[import-untyped]


class PageContent(TypedDict):
    title: str
    page_content: Optional[list[ft.Control]]
    execute_function: Optional[Callable[..., Any]]
    function_args: Optional[list[Any] | dict[str, Any]]


class ContactData(TypedDict):
    contact_uuid: str
    username: str
    description: str
    onion_address: str


class MessageData(TypedDict):
    id: str
    contact_uuid: str
    message: str
    timestamp: float


class DeviceData(TypedDict):
    uuid: str
    onion_address: str
    name: str


PageRoute = dict[str, PageContent]
