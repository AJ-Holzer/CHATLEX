def normalize_route(path: str) -> str:
    # Split by "/" and filter out empty parts
    parts: list[str] = [part for part in path.split("/") if part]

    # Join with single slash and prepend one slash
    normalized: str = "/" + "/".join(parts)

    return normalized
