from functools import lru_cache
from typing import Any

import flet as ft  # type:ignore[import-untyped]


# Cache 100 values to improve performance
@lru_cache(maxsize=100)
def get_key_or_default(page: ft.Page, default: Any, key_name: str) -> Any:
    """Retrieves a value from a session by key, returning a default if the key is not found.

    Args:
        page(ft.Page): The page object containing the session.
        default(Any): The default value to return if the key is not found.
        key_name(str): The name of the key to retrieve.

    Returns:
        Any: The value associated with the key, or the default value if the key is not found.

    Raises:
        KeyError: If the key is not found in the session and no default is provided.
    """
    value: Any = None

    if page.client_storage.contains_key(key_name):
        value = page.client_storage.get(key_name)
        print(f"Key '{key_name}' found in client storage! Returning value '{value}'")
        return value

    elif page.session.contains_key(key_name):
        value = page.session.get(key_name)
        print(f"Key '{key_name}' found in session! Returning value '{value}'")
        return value

    print(f"Key not found! Returning default value '{default}'")
    return default
