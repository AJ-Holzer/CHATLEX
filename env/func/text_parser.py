import re
from typing import Any, Callable

import flet as ft  # type: ignore[import-untyped]


# TODO: Rewrite parser! (--> this thing is messed up as fuck)  --> Blame ChatGPT ;)
def parse_custom_markdown(input_str: str) -> ft.Container:
    supported_styles: dict[str, Callable[[str], dict[str, Any]]] = {
        "COLOR": lambda val: {"color": val},
        "WEIGHT": lambda val: {
            "weight": getattr(ft.FontWeight, val.upper(), ft.FontWeight.NORMAL)
        },
        "UNDERLINE": lambda _: {"decoration": ft.TextDecoration.UNDERLINE},
        "BG": lambda val: {"bgcolor": val},
    }

    active_styles: list[tuple[str, dict[str, Any]]] = []
    text_spans: list[ft.TextSpan] = []
    buffer: str = ""
    tag_pattern = re.compile(r"\{(/?[A-Z]+)(?::([^}]+))?\}")
    pos = 0

    while pos < len(input_str):
        match = tag_pattern.search(input_str, pos)
        if not match:
            buffer += input_str[pos:]
            break

        start, end = match.span()
        if start > pos:
            buffer += input_str[pos:start]

        # Flush buffer into spans with correct styling
        if buffer:
            combined_style: dict[str, Any] = {}
            for _, style_dict in active_styles:
                combined_style.update(style_dict)
            parts = buffer.split("\n")
            for i, part in enumerate(parts):
                if part:
                    text_spans.append(
                        ft.TextSpan(part, style=ft.TextStyle(**combined_style))
                    )
                if i < len(parts) - 1:
                    text_spans.append(ft.TextSpan("\n"))
            buffer = ""

        tag_name = match.group(1)
        tag_value = match.group(2)

        if not tag_name.startswith("/"):
            style_fn = supported_styles.get(tag_name)
            if style_fn:
                resolved = style_fn(tag_value)
                active_styles.append((tag_name, resolved))
        else:
            key_to_close = tag_name[1:]
            for i in range(len(active_styles) - 1, -1, -1):
                style_key, _ = active_styles[i]
                if style_key == key_to_close:
                    del active_styles[i]
                    break

        pos = end

    # Final buffer flush
    if buffer:
        combined_style = {}
        for _, style_dict in active_styles:
            combined_style.update(style_dict)
        parts = buffer.split("\n")
        for i, part in enumerate(parts):
            if part:
                text_spans.append(
                    ft.TextSpan(part, style=ft.TextStyle(**combined_style))
                )
            if i < len(parts) - 1:
                text_spans.append(ft.TextSpan("\n"))

    return ft.Container(
        content=ft.Text(spans=text_spans, selectable=True),
        padding=10,
        border_radius=5,
    )
