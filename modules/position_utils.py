def get_horizontal_position(cx, width):
    if cx < width // 3:
        return "Links"

    if cx > 2 * width // 3:
        return "Rechts"

    return "Mitte"
