import cv2
import numpy as np
import tensorflow as tf

from camera import open_camera, close_camera


def run_digit_recognition():
    model = tf.keras.models.load_model("models/digit_model.keras")

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

        input_image = normalized.reshape(1, 28, 28)

        prediction = model.predict(input_image, verbose=0)

        digit = int(np.argmax(prediction))
        confidence = float(np.max(prediction))

        preview = cv2.resize(resized, (280, 280), interpolation=cv2.INTER_NEAREST)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        text = f"Zahl: {digit} ({confidence:.2f})"

        if confidence < 0.70:
            text = "Unsicher"

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
