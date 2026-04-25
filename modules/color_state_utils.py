def get_color_state(red_pixels, green_pixels, threshold=2000):
    if red_pixels > threshold:
        return "STOP"

    if green_pixels > threshold:
        return "GO"

    return "WAIT"
