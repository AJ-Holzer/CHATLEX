import flet as ft  # type:ignore[import-untyped]
from typing import Any

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
    if page.client_storage.contains_key(key_name):
        value: Any = page.client_storage.get(key_name)
        print(f"Key found! Returning value '{value}'")
        return value
    
    print(f"Key not found! Returning default value '{default}'")
    return default
