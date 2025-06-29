from enum import Enum
from typing import Literal, Optional, TypeAlias, TypedDict

import flet as ft  # type:ignore[import-untyped]

TRANSLATION_CONTROLS: TypeAlias = (
    ft.Text  # Done
    | ft.TextField  # Done
    | ft.TextButton  # Done
    | ft.IconButton  # Done
    | ft.ElevatedButton  # Done
    | ft.FilledButton  # Done
    | ft.OutlinedButton  # Done
    | ft.FilledTonalButton  # Done
    | ft.FloatingActionButton  # Done
    | ft.Checkbox  # Done
    | ft.Slider  # Done
    | ft.CupertinoSwitch  # Done
    | ft.Switch
)


class Language(Enum):
    DE_AT = "de-at"
    EN_US = "en-us"


class LanguageData(TypedDict):
    value: dict[str, Optional[str]]
    label: dict[str, Optional[str]]
    text: dict[str, Optional[str]]
    helper_text: dict[str, Optional[str]]
    error_text: dict[str, Optional[str]]
    tooltip: dict[str, Optional[str]]


class ControlAddingData(TypedDict):
    control_name: str
    control: TRANSLATION_CONTROLS


class ControlStates(TypedDict):
    value: Optional[str]
    label: Optional[str]
    text: Optional[str]
    helper_text: Optional[str]
    error_text: Optional[str]
    tooltip: Optional[str]


CONTROL_STATE_KEYS: TypeAlias = Literal[
    "label", "text", "helper_text", "error_text", "tooltip"
]


class ControlLanguageData(TypedDict):
    value: Optional[str]
    label: Optional[str]
    text: Optional[str]
    helper_text: Optional[str]
    error_text: Optional[str]
    tooltip: Optional[str]
