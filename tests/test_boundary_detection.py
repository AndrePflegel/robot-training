import cv2
from modules.profile_loader import load_profiles, get_active_profile
from modules.color_profile_utils import detect_boundary_color


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

        result = detect_boundary_color(hsv, width, height, boundary_color)

        roi_y = result.get("roi_start_y", int(height * 0.50))

        # ROI-Bereich anzeigen
        cv2.rectangle(frame, (0, roi_y), (width, height), (255, 255, 255), 2)

        if result["found"]:
            x, y, w, h = result["bbox"]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)

            text = f"BOUNDARY FOUND | area={int(result['area'])} | px={result['pixels']}"
            color = (0, 255, 255)
        else:
            text = f"BOUNDARY NOT FOUND | area={int(result['area'])} | px={result['pixels']}"
            color = (0, 0, 255)

        cv2.putText(
            frame,
            text,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )

        cv2.imshow("Boundary Detection Test", frame)

        # Debug-Maske anzeigen: weiß = erkanntes Gelb
        if "debug_mask" in result:
            cv2.imshow("Boundary Mask", result["debug_mask"])

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
