def get_direction_from_center(cx, width):
    if cx < width // 3:
        return "Links lenken"

    if cx > 2 * width // 3:
        return "Rechts lenken"

    return "Geradeaus"
