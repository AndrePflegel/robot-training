import cv2
import numpy as np
from modules.line_contour_utils import get_biggest_valid_contour
from modules.line_utils import get_direction_from_center
from config.settings import (
	LINE_DILATE_ITERATIONS,
	LINE_ERODE_ITERATIONS,
	LINE_KERNEL_SIZE,
	LINE_MIN_AREA,
	LINE_ROI_START_RATIO,
	LINE_THRESHOLD,
)

def run_line_detection():
    cap = cv2.VideoCapture(0)

    last_direction = "Keine Linie"

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Keine Kamera erkannt")
            break

        height, width = frame.shape[:2]

        roi_start = int(height * LINE_ROI_START_RATIO)
        roi = frame[roi_start:height, 0:width]

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        _, mask = cv2.threshold(blur, LINE_THRESHOLD, 255, cv2.THRESH_BINARY_INV)

        kernel = np.ones((LINE_KERNEL_SIZE, LINE_KERNEL_SIZE), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=LINE_ERODE_ITERATIONS)
        mask = cv2.dilate(mask, kernel, iterations=LINE_DILATE_ITERATIONS)

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        direction = "Keine Linie"

        contour_data = [
            (contour, cv2.contourArea(contour))
            for contour in contours
        ]

        biggest = get_biggest_valid_contour(contour_data, min_area=LINE_MIN_AREA)

        if biggest is not None:
            x, y, w, h = cv2.boundingRect(biggest)

            cx = x + w // 2
            cy = y + h // 2

            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(roi, (cx, cy), 6, (255, 0, 0), -1)

            direction = get_direction_from_center(cx, width)
            last_direction = direction
        else:
            direction = last_direction

        cv2.line(roi, (width // 3, 0), (width // 3, roi.shape[0]), (255, 255, 0), 2)
        cv2.line(roi, (2 * width // 3, 0), (2 * width // 3, roi.shape[0]), (255, 255, 0), 2)

        cv2.line(frame, (0, roi_start), (width, roi_start), (255, 0, 0), 2)

        cv2.putText(
            frame,
            direction,
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

        cv2.imshow("Linienerkennung", frame)
        cv2.imshow("Maske", mask)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
