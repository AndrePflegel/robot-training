import numpy as np
import cv2


def build_color_masks(hsv, colors):
    masks = []

    for color in colors:
        lower = np.array(color["lower"])
        upper = np.array(color["upper"])

        mask = (color["name"], color["action"], lower, upper)

        masks.append(mask)

    return masks


def apply_color_masks(hsv, color_masks):
    results = []

    for name, action, lower, upper in color_masks:
        mask = cv2.inRange(hsv, lower, upper)
        pixel_count = cv2.countNonZero(mask)

        results.append({
            "name": name,
            "action": action,
            "pixels": pixel_count,
            "mask": mask
        })

    return results
