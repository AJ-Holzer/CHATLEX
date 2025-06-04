from secrets import token_bytes


def generate_iv() -> bytes:
    return token_bytes(16)


def generate_salt(salt_length: int) -> bytes:
    return token_bytes(salt_length)
