import base64
from typing import Optional


def byte_to_str(data: bytes) -> Optional[str]:
    """Convert bytes to string using base64 encoding.

    Args:
        data(bytes): Bytes data to be converted.

    Returns:
        str: Base64 encoded string.

    Raises:
        binascii.Error: If the bytes data is not valid base64 encoded data.
        UnicodeDecodeError: If the base64 encoded data cannot be decoded using UTF-8.
    """
    return base64.b64encode(data).decode("UTF-8") if data else None


def str_to_byte(data: str) -> Optional[bytes]:
    """Convert a string to bytes using base64 decoding.

    Args:
        data(str): String to be converted to bytes.

    Returns:
        bytes: Bytes representation of the input string.

    Raises:
        binascii.Error: Raised if the input string is not a valid base64 encoded string.
        UnicodeEncodeError: Raised if the input string cannot be encoded using UTF-8.
    """
    return base64.b64decode(data.encode("UTF-8")) if data else None
