import cv2
import numpy as np
from modules.position_utils import get_horizontal_position
from config.settings import RED_LOWER_1, RED_UPPER_1, RED_LOWER_2, RED_UPPER_2, COLOR_MIN_AREA


def run_color_detection():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Keine Kamera erkannt")
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


        mask1 = cv2.inRange(hsv, RED_LOWER_1, RED_UPPER_1)
        mask2 = cv2.inRange(hsv, RED_LOWER_2, RED_UPPER_2)
        mask = mask1 + mask2

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if len(contours) > 0:
            biggest = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(biggest)

            if area > COLOR_MIN_AREA:
                x, y, w, h = cv2.boundingRect(biggest)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                cx = x + w // 2
                cy = y + h // 2

                cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

                frame_width = frame.shape[1]
                direction = get_horizontal_position(cx, frame_width)

                cv2.putText(
                    frame,
                    "Rot erkannt",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    direction,
                    (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0),
                    2
                )

        cv2.imshow("Erkennung", frame)
        cv2.imshow("Maske", mask)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
