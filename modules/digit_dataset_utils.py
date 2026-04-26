import os
from datetime import datetime

import cv2


def save_digit_correction(image, label, base_dir="data/corrections"):
    if label not in [str(i) for i in range(10)]:
        raise ValueError("Label muss eine Zahl von 0 bis 9 sein.")

    target_dir = os.path.join(base_dir, label)
    os.makedirs(target_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    file_path = os.path.join(target_dir, f"{timestamp}.png")

    success = cv2.imwrite(file_path, image)

    if not success:
        raise IOError("Bild konnte nicht gespeichert werden.")

    return file_path
