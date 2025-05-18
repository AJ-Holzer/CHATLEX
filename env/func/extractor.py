def retrieve_initials(text: str) -> str:
    return "".join(i[0].upper() for i in text.split(" ")[:2:])
