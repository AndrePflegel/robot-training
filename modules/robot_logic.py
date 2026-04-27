import cv2
from collections import Counter

from modules.profile_loader import load_profiles, get_active_profile
from modules.signal_logic import resolve_action
from modules.color_profile_utils import detect_target_color
from modules.boundary_detection import detect_boundary_line
from modules.motor_control import execute_action, stop_all
from modules.mission_control import MissionController
from modules.gesture_detection import detect_finger_count


def decide_action(*args):
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


def handle_mode_key(key, mission, action_history):
    if key == ord("1"):
        mission.set_mode(1)
        action_history.clear()
        print("MODE 1 aktiviert")

    elif key == ord("2"):
        mission.set_mode(2)
        action_history.clear()
        print("MODE 2 aktiviert")

    elif key == ord("3"):
        mission.set_mode(3)
        action_history.clear()
        print("MODE 3 aktiviert")


def handle_gesture_mode(frame, mission, action_history, gesture_buffer, gesture_mode_locked):
    if gesture_mode_locked:
        return gesture_mode_locked, 0

    fingers = detect_finger_count(frame)

    if fingers in [1, 2, 3]:
        gesture_buffer.append(fingers)

        if len(gesture_buffer) > 10:
            gesture_buffer.pop(0)

        most_common = max(set(gesture_buffer), key=gesture_buffer.count)

        if gesture_buffer.count(most_common) > 6:
            mission.set_mode(most_common)
            action_history.clear()
            gesture_mode_locked = True
            print(f"GESTURE MODE {most_common} stabil erkannt")

    return gesture_mode_locked, fingers


def run_robot_logic():
    cap = cv2.VideoCapture(0)

    data = load_profiles()
    profile = get_active_profile(data)

    boundary_color = find_color_config(profile, ["yellow", "gelb"])

    if boundary_color is None:
        print("Keine Begrenzungs-Farbe gelb im Profil gefunden.")
        return

    action_history = []
    gesture_buffer = []
    gesture_mode_locked = False
    last_fingers = 0

    mission = MissionController()
    mission.set_mode(2)  # Default: rot -> blau, später durch Geste ersetzt

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Keine Kamera erkannt")
            break

        height, width = frame.shape[:2]
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        gesture_mode_locked, last_fingers = handle_gesture_mode(
            frame,
            mission,
            action_history,
            gesture_buffer,
            gesture_mode_locked
        )

        current_target_name = mission.get_current_target()

        if current_target_name is None:
            raw_action = "STOP"
            action = smooth_action(action_history, raw_action, history_size=5)
            execute_action(action)

            cv2.putText(
                frame,
                "MISSION FINISHED",
                (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

            cv2.putText(
                frame,
                f"MODE: {mission.mode} TARGET: none",
                (30, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"GESTURE locked={gesture_mode_locked} fingers={last_fingers}",
                (30, 115),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 0),
                2
            )

            cv2.imshow("Robot Logic", frame)

            key = cv2.waitKey(1)

            handle_mode_key(key, mission, action_history)

            if key == ord("r"):
                gesture_mode_locked = False
                gesture_buffer.clear()
                print("GESTURE RESET")

            if key == 27:
                stop_all()
                break

            continue

        target_color = find_color_config(profile, [current_target_name])

        if target_color is None:
            raw_action = "STOP"
            action = smooth_action(action_history, raw_action, history_size=5)
            execute_action(action)

            cv2.putText(
                frame,
                f"Ziel-Farbe fehlt im Profil: {current_target_name}",
                (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

            cv2.imshow("Robot Logic", frame)

            key = cv2.waitKey(1)

            handle_mode_key(key, mission, action_history)

            if key == ord("r"):
                gesture_mode_locked = False
                gesture_buffer.clear()
                print("GESTURE RESET")

            if key == 27:
                stop_all()
                break

            continue

        boundary = detect_boundary_line(hsv, width, height, boundary_color)
        target = detect_target_color(hsv, width, target_color)

        if target["found"] and target["area"] > 4000:
            mission.target_reached()
            action_history.clear()
            raw_action = "STOP"
        else:
            boundary_action = get_boundary_action(boundary)

            if boundary_action is not None:
                raw_action = boundary_action
            elif target["found"]:
                raw_action = get_soft_target_action(target, width)
            else:
                raw_action = "SEARCH_TARGET_SLOW_TURN"

        action = smooth_action(action_history, raw_action, history_size=5)

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

            target_text = (
                f"TARGET {current_target_name} "
                f"area={int(target['area'])} "
                f"cx={target['cx']}"
            )

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
            f"MODE: {mission.mode} TARGET: {current_target_name}",
            (30, 135),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"GESTURE locked={gesture_mode_locked} fingers={last_fingers}",
            (30, 165),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 0),
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

        key = cv2.waitKey(1)

        handle_mode_key(key, mission, action_history)

        if key == ord("r"):
            gesture_mode_locked = False
            gesture_buffer.clear()
            print("GESTURE RESET")

        if key == 27:
            stop_all()
            break

    cap.release()
    cv2.destroyAllWindows()
