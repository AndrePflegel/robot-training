from collections import deque

import cv2
import numpy as np

from camera import open_camera, close_camera
from config.settings import (
    DIGIT_BLUR_KERNEL,
    DIGIT_MIN_CONFIDENCE,
    DIGIT_THRESHOLD,
)
from modules.digit_dataset_utils import save_digit_correction
from modules.digit_preprocess_utils import (
    center_digit,
    extract_largest_digit,
    threshold_digit_roi,
)
from modules.digit_result_utils import format_digit_result
from modules.digit_stability_utils import get_stable_digit
from modules.model_loader import load_digit_model


def run_digit_recognition(model_name="mnist"):
    model_mnist = load_digit_model("mnist")

    model_custom = None
    if model_name in ("custom", "dual"):
        try:
            model_custom = load_digit_model("custom")
            print("Custom-Modell geladen")
        except FileNotFoundError:
            print("Kein Custom-Modell gefunden. Nutze MNIST.")

    print(f"Modus: {model_name}")

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

        digit, confidence, source = predict_digit(
            input_image,
            model_name,
            model_mnist,
            model_custom
        )

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
            text = f"{format_digit_result(stable_digit, confidence)} ({source})"

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

        key = cv2.waitKey(1)

        if key >= ord("0") and key <= ord("9"):
            label = chr(key)

            try:
                file_path = save_digit_correction(prepared, label)
                print(f"Gespeichert als {label}: {file_path}")
            except Exception as e:
                print(f"Fehler beim Speichern: {e}")

        if key == 27:
            break

    close_camera(cap)


def predict_digit(input_image, model_name, model_mnist, model_custom=None):
    prediction_mnist = model_mnist.predict(input_image, verbose=0)
    digit_mnist = int(np.argmax(prediction_mnist))
    confidence_mnist = float(np.max(prediction_mnist))

    if model_name == "mnist" or model_custom is None:
        return digit_mnist, confidence_mnist, "MNIST"

    prediction_custom = model_custom.predict(input_image, verbose=0)
    digit_custom = int(np.argmax(prediction_custom))
    confidence_custom = float(np.max(prediction_custom))

    if model_name == "custom":
        return digit_custom, confidence_custom, "CUSTOM"

    if confidence_custom >= DIGIT_MIN_CONFIDENCE:
        return digit_custom, confidence_custom, "CUSTOM"

    return digit_mnist, confidence_mnist, "MNIST"
