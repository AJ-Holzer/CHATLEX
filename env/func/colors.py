import colorsys


def generate_color_wheel_hex(n: int) -> list[str]:
    """
    Return `n` colors evenly spaced around the HSV color wheel as hex strings.
    """
    if n <= 0:
        return []

    return [
        "#{:02X}{:02X}{:02X}".format(
            *(int(c * 255) for c in colorsys.hsv_to_rgb(i / n, 1, 1))
        )
        for i in range(n)
    ]