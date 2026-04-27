import cv2
from modules.profile_loader import load_profiles, get_active_profile
from modules.boundary_detection import detect_boundary_line


def run_test_boundary_detection():
    cap = cv2.VideoCapture(0)

    data = load_profiles()
    profile = get_active_profile(data)

    boundary_color = next(
        (c for c in profile["colors"] if c["name"].lower() in ["yellow", "gelb"]),
        None
    )

    if boundary_color is None:
        print("Keine gelbe Farbe im Profil gefunden.")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Keine Kamera")
            break

        height, width = frame.shape[:2]
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        result = detect_boundary_line(hsv, width, height, boundary_color)

        roi_y = result.get("roi_start_y", int(height * 0.35))
        cv2.rectangle(frame, (0, roi_y), (width, height), (255, 255, 255), 2)

        if result["found"]:
            x1, y1, x2, y2 = result["line"]

            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 255), 4)

            text = (
                f"{result['line_type']} | "
                f"{result['position']} | "
                f"angle={int(result['angle'])} | "
                f"lines={result['line_count']} | "
                f"corner={result['is_corner']} | "
                f"{result['suggested_action']}"
            )

            color = (0, 255, 255)
        else:
            text = "NO BOUNDARY LINE"
            color = (0, 0, 255)

        cv2.putText(
            frame,
            text,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            color,
            2
        )

        cv2.imshow("Boundary Line Test", frame)

        if "debug_mask" in result:
            cv2.imshow("Boundary Line Mask", result["debug_mask"])

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
