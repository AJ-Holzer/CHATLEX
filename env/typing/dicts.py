from typing import Any, Callable, Optional, TypedDict

import flet as ft  # type:ignore[import-untyped]


class PageContent(TypedDict):
    title: str
    page_content: Optional[list[ft.Control]]
    execute_function: Optional[Callable[..., Any]]
    function_args: Optional[list[Any] | dict[str, Any]]


PageRoute = dict[str, PageContent]
