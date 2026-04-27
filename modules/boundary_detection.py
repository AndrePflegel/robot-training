import numpy as np
import cv2
from modules.line_contour_utils import get_biggest_valid_contour
from modules.line_utils import get_direction_from_center

def detect_boundary_line(hsv, frame_width, frame_height, color_config):
    hsv_work = hsv.copy()

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

    sat = hsv_work[:, :, 1]
    sat_mask = cv2.inRange(sat, 70, 255)
    mask = cv2.bitwise_and(mask, sat_mask)

    roi_start_y = int(frame_height * 0.35)
    roi = mask[roi_start_y:frame_height, 0:frame_width]

    kernel = np.ones((5, 5), np.uint8)
    roi = cv2.morphologyEx(roi, cv2.MORPH_CLOSE, kernel)

    edges = cv2.Canny(roi, 50, 150)

    lines = cv2.HoughLinesP(
        edges,
        1,
        np.pi / 180,
        threshold=35,
        minLineLength=40,
        maxLineGap=25
    )

    if lines is None:
        return {
            "found": False,
            "is_corner": False,
            "line_count": 0,
            "suggested_action": "search_boundary",
            "debug_mask": roi,
            "roi_start_y": roi_start_y
        }

    detected_lines = []
    best_line = None
    best_length = 0

    has_horizontal = False
    has_vertical = False
    has_diagonal = False

    for line in lines:
        x1, y1, x2, y2 = line[0]

        dx = x2 - x1
        dy = y2 - y1
        length = (dx ** 2 + dy ** 2) ** 0.5

        if length < 35:
            continue

        angle = np.degrees(np.arctan2(dy, dx))
        abs_angle = abs(angle)

        if abs_angle < 20:
            line_type = "horizontal"
            has_horizontal = True
        elif abs_angle > 70:
            line_type = "vertical"
            has_vertical = True
        else:
            line_type = "diagonal"
            has_diagonal = True

        x1_abs = x1
        y1_abs = y1 + roi_start_y
        x2_abs = x2
        y2_abs = y2 + roi_start_y

        detected_lines.append({
            "line": (x1_abs, y1_abs, x2_abs, y2_abs),
            "angle": angle,
            "length": length,
            "line_type": line_type
        })

        if length > best_length:
            best_length = length
            best_line = detected_lines[-1]

    if best_line is None:
        return {
            "found": False,
            "is_corner": False,
            "line_count": 0,
            "suggested_action": "search_boundary",
            "debug_mask": roi,
            "roi_start_y": roi_start_y
        }

    x1, y1, x2, y2 = best_line["line"]

    center_x = (x1 + x2) // 2

    if center_x < frame_width // 3:
        position = "left"
    elif center_x > 2 * frame_width // 3:
        position = "right"
    else:
        position = "center"

    bottom_y = max(y1, y2)
    near_bottom = bottom_y > int(frame_height * 0.80)

    is_corner = has_horizontal and has_vertical

    suggested_action = "observe"

    if is_corner and near_bottom:
        suggested_action = "escape_corner"
    elif near_bottom and best_line["line_type"] == "horizontal":
        suggested_action = "turn_around"
    elif near_bottom and position == "left":
        suggested_action = "turn_right"
    elif near_bottom and position == "right":
        suggested_action = "turn_left"
    elif near_bottom and position == "center":
        suggested_action = "slow_down"

    return {
        "found": True,
        "line": best_line["line"],
        "angle": best_line["angle"],
        "line_type": best_line["line_type"],
        "position": position,
        "near_bottom": near_bottom,
        "suggested_action": suggested_action,
        "length": best_line["length"],
        "is_corner": is_corner,
        "line_count": len(detected_lines),
        "has_horizontal": has_horizontal,
        "has_vertical": has_vertical,
        "has_diagonal": has_diagonal,
        "lines": detected_lines,
        "debug_mask": roi,
        "roi_start_y": roi_start_y
    }
