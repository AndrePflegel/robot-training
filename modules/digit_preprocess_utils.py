import cv2
import numpy as np


def threshold_digit_roi(roi, blur_kernel=5, threshold_value=100):
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(
        gray,
        (blur_kernel, blur_kernel),
        0
    )

    _, threshold = cv2.threshold(
        blur,
        threshold_value,
        255,
        cv2.THRESH_BINARY_INV
    )

    return threshold


def resize_to_mnist(image):
    resized = cv2.resize(image, (28, 28))
    normalized = resized / 255.0

    return normalized
