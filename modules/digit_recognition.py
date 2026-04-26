import cv2
import numpy as np
import tensorflow as tf

from camera import open_camera, close_camera
from modules.digit_result_utils import format_digit_result
from collections import deque
from modules.digit_stability_utils import get_stable_digit
from config.settings import DIGIT_MIN_CONFIDENCE
from modules.digit_preprocess_utils import (
    center_digit,
    extract_largest_digit,
    threshold_digit_roi,
)
from config.settings import DIGIT_BLUR_KERNEL, DIGIT_THRESHOLD


def run_digit_recognition():
    model = tf.keras.models.load_model("models/digit_model.keras")
    last_digits = deque(maxlen=10)

    cap = open_camera()

    if cap is None:
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Kein Kamerabild erhalten.")
            break

        height, width = frame.shape[:2]

        box_size = 220
        x1 = width // 2 - box_size // 2
        y1 = height // 2 - box_size // 2
        x2 = width // 2 + box_size // 2
        y2 = height // 2 + box_size // 2

        roi = frame[y1:y2, x1:x2]

        threshold = threshold_digit_roi(
            roi,
            blur_kernel=DIGIT_BLUR_KERNEL,
            threshold_value=DIGIT_THRESHOLD
        )
        
        digit_image = extract_largest_digit(threshold)
        
        if digit_image is None:
            prepared = center_digit(threshold)
        else:
            prepared = center_digit(digit_image)
            
        normalized = prepared / 255.0
        input_image = normalized.reshape(1, 28, 28)

        prediction = model.predict(input_image, verbose=0)

        digit = int(np.argmax(prediction))
        confidence = float(np.max(prediction))

        preview = cv2.resize(
            prepared,
            (280, 280),
            interpolation=cv2.INTER_NEAREST
        )

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        if confidence >= DIGIT_MIN_CONFIDENCE:
            last_digits.append(digit)
            
        stable_digit = get_stable_digit(list(last_digits))
        
        if stable_digit is None:
            text = "Unsicher"
        else:
            text = format_digit_result(stable_digit, confidence)

        cv2.putText(
            frame,
            text,
            (30, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

        cv2.imshow("Zahlenerkennung", frame)
        cv2.imshow("Vorbereitet 28x28", preview)

        if cv2.waitKey(1) == 27:
            break

    close_camera(cap)
