import cv2
from config.settings import (
    COLOR_MIN_AREA,
    GREEN_LOWER,
    GREEN_UPPER,
    RED_LOWER_1,
    RED_LOWER_2,
    RED_UPPER_1,
    RED_UPPER_2,
)
from modules.color_state_utils import get_color_state
from modules.position_utils import get_horizontal_position


def run_color_detection():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Keine Kamera erkannt")
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask_red = create_red_mask(hsv)
        mask_green = create_green_mask(hsv)
        mask_combined = mask_red + mask_green

        red_pixels = cv2.countNonZero(mask_red)
        green_pixels = cv2.countNonZero(mask_green)
        state = get_color_state(red_pixels, green_pixels)

        draw_biggest_object(frame, mask_combined)

        cv2.putText(
            frame,
            state,
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )

        cv2.imshow("Erkennung", frame)
        cv2.imshow("Maske", mask_combined)
        cv2.imshow("Red Mask", mask_red)
        cv2.imshow("Green Mask", mask_green)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


def create_red_mask(hsv):
    mask_red1 = cv2.inRange(hsv, RED_LOWER_1, RED_UPPER_1)
    mask_red2 = cv2.inRange(hsv, RED_LOWER_2, RED_UPPER_2)

    return mask_red1 + mask_red2


def create_green_mask(hsv):
    return cv2.inRange(hsv, GREEN_LOWER, GREEN_UPPER)


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
