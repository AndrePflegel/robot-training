import cv2

from modules.profile_loader import load_profiles, get_active_profile
from modules.signal_logic import resolve_action
from modules.color_profile_utils import detect_target_color, detect_boundary_color


def decide_action(*args):
    """
    Kompatibilität:
    ALT: decide_action(red_pixels, green_pixels, direction)
    NEU: decide_action(profile, signals)
    """

    if len(args) == 2:
        profile, signals = args
        return resolve_action(profile, signals)

    elif len(args) == 3:
        red_pixels, green_pixels, direction = args

        if red_pixels > 2000:
            return "STOP"

        if green_pixels > 2000:
            return f"GO: {direction}"

        return f"WAIT: {direction}"

    else:
        raise ValueError("Ungültige Argumente für decide_action()")


def find_color_config(profile, names):
    for color in profile["colors"]:
        if color["name"].lower() in names:
            return color

    return None


def run_robot_logic():
    cap = cv2.VideoCapture(0)

    data = load_profiles()
    profile = get_active_profile(data)

    target_color = find_color_config(profile, ["green", "gruen", "grün"])
    boundary_color = find_color_config(profile, ["yellow", "gelb"])

    if target_color is None:
        print("Keine Ziel-Farbe grün im Profil gefunden.")
        return

    if boundary_color is None:
        print("Keine Begrenzungs-Farbe gelb im Profil gefunden.")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Keine Kamera erkannt")
            break

        height, width = frame.shape[:2]
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        boundary = detect_boundary_color(hsv, width, height, boundary_color)
        target = detect_target_color(hsv, width, target_color)

        if boundary["found"]:
            action = "AVOID_BOUNDARY"
        elif target["found"]:
            action = f"APPROACH_TARGET: {target['direction']}"
        else:
            action = "SEARCH_TARGET"

        roi_y = boundary.get("roi_start_y", int(height * 0.50))
        cv2.rectangle(frame, (0, roi_y), (width, height), (255, 255, 255), 2)

        if boundary["found"]:
            x, y, w, h = boundary["bbox"]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)

        if target["found"]:
            x, y, w, h = target["bbox"]
            cx = target["cx"]
            cy = target["cy"]

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 6, (0, 255, 0), -1)

            cv2.line(frame, (width // 3, 0), (width // 3, height), (255, 255, 255), 1)
            cv2.line(frame, (2 * width // 3, 0), (2 * width // 3, height), (255, 255, 255), 1)

        cv2.putText(
            frame,
            action,
            (30, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

        cv2.imshow("Robot Logic", frame)

        if "debug_mask" in boundary:
            cv2.imshow("Boundary Mask", boundary["debug_mask"])

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
