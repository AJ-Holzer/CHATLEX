# Create basic classes
from typing import TypedDict

import flet as ft  # type:ignore[import-untyped]


class PageContent(TypedDict):
    title: str
    content: list[ft.Control]


# Define
SitePages = dict[str, PageContent]
