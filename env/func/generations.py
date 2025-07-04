from secrets import token_bytes


def generate_iv(length: int) -> bytes:
    return token_bytes(length)


def generate_salt(length: int) -> bytes:
    return token_bytes(length)
