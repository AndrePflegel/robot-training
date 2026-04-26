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
    
def extract_largest_digit(threshold_image, min_area=100):
    contours, _ = cv2.findContours(
        threshold_image,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    
    if not contours:
        return None
        
    biggest = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(biggest)
    
    if area < min_area:
        return None
        
    x, y, w, h = cv2.boundingRect(biggest)
    digit = threshold_image[y:y + h, x:x + w]
    return digit
    
def center_digit(image, size=28, padding=4):
    h, w = image.shape

    # größtes Maß bestimmen
    max_dim = max(h, w)

    # leeres Quadrat erzeugen
    square = np.zeros((max_dim, max_dim), dtype=np.uint8)

    # Bild zentriert einfügen
    y_offset = (max_dim - h) // 2
    x_offset = (max_dim - w) // 2

    square[y_offset:y_offset + h, x_offset:x_offset + w] = image

    # verkleinern mit Rand
    new_size = size - 2 * padding

    resized = cv2.resize(square, (new_size, new_size))

    final = np.zeros((size, size), dtype=np.uint8)
    final[padding:padding + new_size, padding:padding + new_size] = resized

    return final
