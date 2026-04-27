import cv2
import numpy as np


def detect_finger_count(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Hautbereich (einfach gehalten)
    lower = np.array([0, 30, 60])
    upper = np.array([20, 150, 255])

    mask = cv2.inRange(hsv, lower, upper)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return 0

    biggest = max(contours, key=cv2.contourArea)

    if cv2.contourArea(biggest) < 2000:
        return 0

    hull = cv2.convexHull(biggest)
    defects = cv2.convexityDefects(biggest, cv2.convexHull(biggest, returnPoints=False))

    if defects is None:
        return 1

    count = 0

    for i in range(defects.shape[0]):
        s, e, f, d = defects[i][0]

        if d > 10000:
            count += 1

    return count + 1
