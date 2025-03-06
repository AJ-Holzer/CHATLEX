import textwrap

# def insert_newlines_by_words(text: str, interval: int = 60) -> str:
#     words = text.split()
#     lines = []
#     current_line = ""

#     for word in words:
#         if len(word) > interval:
#             if current_line:
#                 lines.append(current_line)
#                 current_line = ""
#             lines.extend(textwrap.wrap(word, interval))
#         elif len(current_line) + len(word) + 1 <= interval:
#             current_line += (" " if current_line else "") + word
#         else:
#             lines.append(current_line)
#             current_line = word

#     if current_line:
#         lines.append(current_line)

#     return "\n".join(lines)

def insert_newlines_by_words(text: str, width: int) -> str:
    words = text.split(" ")
    lines: list[str] = []
    current_line: list[str] = []
    current_length = 0
    for word in words:
        if current_length + len(word) + 1 > width:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_length = len(word)
        else:
            current_line.append(word)
            current_length += len(word) + 1
    if current_line:
        lines.append(" ".join(current_line))
    return "\n".join(lines)
