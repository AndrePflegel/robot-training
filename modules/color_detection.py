import cv2

from modules.position_utils import get_horizontal_position
from modules.profile_loader import load_profiles, get_active_profile
from modules.color_profile_utils import build_color_masks, apply_color_masks


COLOR_MIN_AREA = 1000


def run_color_detection():
    cap = cv2.VideoCapture(0)

    data = load_profiles()
    profile = get_active_profile(data)

    color_masks = build_color_masks(None, profile["colors"])

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Keine Kamera erkannt")
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        results = apply_color_masks(hsv, color_masks)

        combined_mask = None
        active_action = None

        for result in results:
            if combined_mask is None:
                combined_mask = result["mask"]
            else:
                combined_mask = combined_mask + result["mask"]

            if result["pixels"] > 2000:
                active_action = result["action"]

        if combined_mask is None:
            combined_mask = hsv[:, :, 0] * 0  # leere Maske

        draw_biggest_object(frame, combined_mask)

        if active_action is None:
            text = "WAIT"
        else:
            text = active_action

        cv2.putText(
            frame,
            text,
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )

        cv2.imshow("Erkennung", frame)
        cv2.imshow("Maske", combined_mask)

        for result in results:
            cv2.imshow(result["name"], result["mask"])

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


def draw_biggest_object(frame, mask):
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if len(contours) == 0:
        return

    biggest = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(biggest)

    if area <= COLOR_MIN_AREA:
        return

    x, y, w, h = cv2.boundingRect(biggest)

    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cx = x + w // 2
    cy = y + h // 2

    cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

    frame_width = frame.shape[1]
    direction = get_horizontal_position(cx, frame_width)

    cv2.putText(
        frame,
        "Objekt erkannt",
        (x, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        direction,
        (50, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        2
    )
