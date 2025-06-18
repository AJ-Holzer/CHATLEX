import re


def is_valid_onion_address(addr: str) -> bool:
    return bool(re.fullmatch(r"[a-z2-7]{16,56}\.onion", addr))
