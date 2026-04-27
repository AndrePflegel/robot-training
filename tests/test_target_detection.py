import cv2
from modules.profile_loader import load_profiles, get_active_profile
from modules.color_profile_utils import detect_target_color


def run_test_target_detection():
    cap = cv2.VideoCapture(0)

    data = load_profiles()
    profile = get_active_profile(data)

    target_color = next(
        (c for c in profile["colors"] if c["name"].lower() in ["green", "gruen", "grün"]),
        None
    )

    if target_color is None:
        print("Keine grüne Farbe im Profil gefunden.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Keine Kamera")
            break

        height, width = frame.shape[:2]
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        result = detect_target_color(hsv, width, target_color)

        if result["found"]:
            cx = result["cx"]
            area = int(result["area"])
            direction = result["direction"]
            x, y, w, h = result["bbox"]
            cx = result["cx"]
            cy = result["cy"]

            #Kasten
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.circle(frame, (cx, height // 2), 8, (0, 255, 0), -1)

            cv2.putText(
                frame,
                f"GREEN FOUND | {direction} | area={area}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )
        else:
            cv2.putText(
                frame,
                "GREEN NOT FOUND",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

        cv2.line(frame, (width // 3, 0), (width // 3, height), (255, 255, 255), 1)
        cv2.line(frame, (2 * width // 3, 0), (2 * width // 3, height), (255, 255, 255), 1)

        cv2.imshow("Target Detection Test", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
