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
    cy = y + h // 2
    area = cv2.contourArea(biggest)

    direction = get_direction_from_center(cx, frame_width)

    return {
        "found": True,
        "cx": cx,
        "cy": cy,
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


def detect_boundary_color(hsv, frame_width, frame_height, color_config):
    # Arbeitskopie, damit das Original-HSV-Bild nicht verändert wird
    hsv_work = hsv.copy()

    # Helligkeit stabilisieren
    hsv_work[:, :, 2] = cv2.normalize(
        hsv_work[:, :, 2],
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    lower = np.array(color_config["lower"])
    upper = np.array(color_config["upper"])

    mask = cv2.inRange(hsv_work, lower, upper)

    # Sättigung filtern, damit heller Boden weniger stört
    sat = hsv_work[:, :, 1]
    sat_mask = cv2.inRange(sat, 80, 255)

    mask = cv2.bitwise_and(mask, sat_mask)

    # Nur untere Bildhälfte prüfen: dort wird die Begrenzung gefährlich
    roi_start_y = int(frame_height * 0.50)
    roi = mask[roi_start_y:frame_height, 0:frame_width]

    # Bildrauschen reduzieren und Lücken in der Linie schließen
    kernel = np.ones((7, 7), np.uint8)
    roi = cv2.morphologyEx(roi, cv2.MORPH_OPEN, kernel)
    roi = cv2.morphologyEx(roi, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(
        roi,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        return {
            "found": False,
            "pixels": 0,
            "area": 0,
            "roi_start_y": roi_start_y,
            "debug_mask": roi
        }

    biggest = max(contours, key=cv2.contourArea)

    area = cv2.contourArea(biggest)
    pixels = cv2.countNonZero(roi)
    x, y, w, h = cv2.boundingRect(biggest)

    # Linie kann schmal sein, aber soll entweder lang oder groß genug sein
    is_wide_line = w > frame_width * 0.25
    is_tall_line = h > (frame_height - roi_start_y) * 0.25
    is_big_enough = area > 800 or pixels > 1200

    found = is_big_enough and (is_wide_line or is_tall_line)

    return {
        "found": found,
        "pixels": pixels,
        "area": area,
        "roi_start_y": roi_start_y,
        "bbox": (x, y + roi_start_y, w, h),
        "debug_mask": roi
    }
