import cv2
import numpy as np


def preprocess_digit_image(frame, x1, y1, x2, y2):
    roi = frame[y1:y2, x1:x2]

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    _, threshold = cv2.threshold(
        blur,
        100,
        255,
        cv2.THRESH_BINARY_INV
    )

    resized = cv2.resize(threshold, (28, 28))
    normalized = resized / 255.0

    return normalized
