import re


def is_valid_onion_address(addr: str) -> bool:
    return bool(re.fullmatch(r"[a-z2-7]{16,56}\.onion", addr))


def is_valid_color_code(color: str) -> bool:
    """
    Checks if the given string is a valid hexadecimal color code.
    Accepts #RGB, #RRGGBB, #RRGGBBAA (with or without #).
    """
    pattern = r"^#?([A-Fa-f0-9]{3}|[A-Fa-f0-9]{6}|[A-Fa-f0-9]{8})$"
    return bool(re.fullmatch(pattern, color))
