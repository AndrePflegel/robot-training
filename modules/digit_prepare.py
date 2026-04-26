import cv2
import numpy as np
from camera import open_camera, close_camera
from config.settings import DIGIT_BOX_SIZE, DIGIT_BLUR_KERNEL, DIGIT_THRESHOLD

def run_digit_prepare():
    cap = open_camera()

    if cap is None:
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Kein Kamerabild erhalten.")
            break

        height, width = frame.shape[:2]

        # Bereich in der Mitte des Bildes festlegen
        box_size = DIGIT_BOX_SIZE
        x1 = width // 2 - box_size // 2
        y1 = height // 2 - box_size // 2
        x2 = width // 2 + box_size // 2
        y2 = height // 2 + box_size // 2

        # Bereich ausschneiden
        roi = frame[y1:y2, x1:x2]

        # In Graustufen umwandeln
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # Weichzeichnen gegen Bildrauschen
        blur = cv2.GaussianBlur(gray, (DIGIT_BLUR_KERNEL, DIGIT_BLUR_KERNEL), 0)

        # In Schwarz-Weiß umwandeln
        _, threshold = cv2.threshold(
            blur,
            DIGIT_THRESHOLD,
            255,
            cv2.THRESH_BINARY_INV
        )

        # Auf MNIST-Größe bringen
        resized = cv2.resize(threshold, (28, 28))

        # Zur Anzeige wieder vergrößern
        preview = cv2.resize(resized, (280, 280), interpolation=cv2.INTER_NEAREST)

        # Rahmen im Originalbild anzeigen
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.putText(
            frame,
            "Zahl in den Rahmen halten",
            (30, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

        cv2.imshow("Original", frame)
        cv2.imshow("Ausschnitt", roi)
        cv2.imshow("Vorbereitet 28x28", preview)

        if cv2.waitKey(1) == 27:
            break

    close_camera(cap)
