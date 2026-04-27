import numpy as np
import cv2
from modules.line_contour_utils import get_biggest_valid_contour
from modules.line_utils import get_direction_from_center


def detect_target_color(hsv, frame_width, color_config):
    lower = np.array(color_config["lower"])
    upper = np.array(color_config["upper"])

    mask = cv2.inRange(hsv, lower, upper)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contour_data = [(c, cv2.contourArea(c)) for c in contours]
    biggest = get_biggest_valid_contour(contour_data)

    if biggest is None:
        return {
            "found": False
        }

    x, y, w, h = cv2.boundingRect(biggest)
    cx = x + w // 2
    area = cv2.contourArea(biggest)

    direction = get_direction_from_center(cx, frame_width)

    return {
        "found": True,
        "cx": cx,
        "cy": y + h // 2,
        "area": area,
        "direction": direction,
        "bbox": (x, y, w, h)
    }


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
