import cv2
from collections import Counter

from modules.profile_loader import load_profiles, get_active_profile
from modules.signal_logic import resolve_action
from modules.color_profile_utils import detect_target_color
from modules.boundary_detection import detect_boundary_line
from modules.motor_control import execute_action


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


def smooth_action(action_history, new_action, history_size=5):
    action_history.append(new_action)

    if len(action_history) > history_size:
        action_history.pop(0)

    counter = Counter(action_history)
    return counter.most_common(1)[0][0]


def get_soft_target_action(target, frame_width):
    """
    Macht aus der groben Richtung eine weichere Lenkentscheidung.
    Je weiter das Ziel vom Mittelpunkt entfernt ist, desto stärker wird gelenkt.
    """
    cx = target["cx"]
    center_x = frame_width // 2
    offset = cx - center_x

    soft_zone = frame_width * 0.10
    strong_zone = frame_width * 0.25

    if abs(offset) < soft_zone:
        return "DRIVE_FORWARD_SLOW"

    if offset < 0:
        if abs(offset) > strong_zone:
            return "TURN_LEFT"
        return "CURVE_LEFT"

    if abs(offset) > strong_zone:
        return "TURN_RIGHT"

    return "CURVE_RIGHT"


def get_boundary_action(boundary):
    """
    Übersetzt erkannte Begrenzungsgeometrie in eine weiche Aktion.
    """
    if not boundary["found"]:
        return None

    if boundary.get("is_corner") and boundary.get("near_bottom"):
        return "ESCAPE_CORNER"

    if not boundary.get("near_bottom"):
        return None

    suggested = boundary.get("suggested_action")

    if suggested == "turn_left":
        return "CURVE_LEFT_AWAY_FROM_BOUNDARY"

    if suggested == "turn_right":
        return "CURVE_RIGHT_AWAY_FROM_BOUNDARY"

    if suggested == "turn_around":
        return "TURN_AROUND"

    if suggested == "slow_down":
        return "DRIVE_FORWARD_VERY_SLOW"

    if suggested == "escape_corner":
        return "ESCAPE_CORNER"

    return "DRIVE_FORWARD_SLOW"


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

    action_history = []

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Keine Kamera erkannt")
            break

        height, width = frame.shape[:2]
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        boundary = detect_boundary_line(hsv, width, height, boundary_color)
        target = detect_target_color(hsv, width, target_color)

        boundary_action = get_boundary_action(boundary)

        if boundary_action is not None:
            raw_action = boundary_action
        elif target["found"]:
            raw_action = get_soft_target_action(target, width)
        else:
            raw_action = "SEARCH_TARGET_SLOW_TURN"

        action = smooth_action(action_history, raw_action, history_size=5)
        
        #Motor-Mapping testen
        execute_action(action)

        roi_y = boundary.get("roi_start_y", int(height * 0.35))
        cv2.rectangle(frame, (0, roi_y), (width, height), (255, 255, 255), 2)

        if boundary["found"]:
            x1, y1, x2, y2 = boundary["line"]

            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 255), 4)

            boundary_text = (
                f"{boundary['line_type']} | "
                f"{boundary['position']} | "
                f"angle={int(boundary['angle'])} | "
                f"lines={boundary['line_count']} | "
                f"corner={boundary['is_corner']} | "
                f"near={boundary['near_bottom']}"
            )

            cv2.putText(
                frame,
                boundary_text,
                (30, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 255, 255),
                2
            )

        if target["found"]:
            x, y, w, h = target["bbox"]
            cx = target["cx"]
            cy = target["cy"]

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 6, (0, 255, 0), -1)

            cv2.line(frame, (width // 2, 0), (width // 2, height), (255, 255, 255), 1)
            cv2.line(frame, (int(width * 0.40), 0), (int(width * 0.40), height), (180, 180, 180), 1)
            cv2.line(frame, (int(width * 0.60), 0), (int(width * 0.60), height), (180, 180, 180), 1)
            cv2.line(frame, (int(width * 0.25), 0), (int(width * 0.25), height), (120, 120, 120), 1)
            cv2.line(frame, (int(width * 0.75), 0), (int(width * 0.75), height), (120, 120, 120), 1)

            target_text = f"TARGET area={int(target['area'])} cx={target['cx']}"
            cv2.putText(
                frame,
                target_text,
                (30, 105),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 255, 0),
                2
            )

        cv2.putText(
            frame,
            f"ACTION: {action}",
            (30, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 0, 255),
            2
        )

        cv2.putText(
            frame,
            f"RAW: {raw_action}",
            (30, height - 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2
        )

        cv2.imshow("Robot Logic", frame)

        if "debug_mask" in boundary:
            cv2.imshow("Boundary Line Mask", boundary["debug_mask"])

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
