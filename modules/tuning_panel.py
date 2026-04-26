import cv2
import numpy as np


def nothing(value):
    pass


def run_tuning_panel():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Keine Kamera erkannt")
        return

    cv2.namedWindow("Tuning", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Tuning", 600, 500)
    
    cv2.namedWindow("Original", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Original", 640, 480)

    cv2.namedWindow("Maske", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Maske", 640, 480)

    cv2.namedWindow("Ergebnis", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Ergebnis", 640, 480)	

    cv2.createTrackbar("Hue min", "Tuning", 0, 180, nothing)
    cv2.createTrackbar("Hue max", "Tuning", 180, 180, nothing)
    cv2.createTrackbar("Saturation min", "Tuning", 0, 255, nothing)
    cv2.createTrackbar("Saturation max", "Tuning", 255, 255, nothing)
    cv2.createTrackbar("Value min", "Tuning", 0, 255, nothing)
    cv2.createTrackbar("Value max", "Tuning", 255, 255, nothing)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Kein Kamerabild erhalten.")
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        h_min = cv2.getTrackbarPos("Hue min", "Tuning")
        h_max = cv2.getTrackbarPos("Hue max", "Tuning")
        s_min = cv2.getTrackbarPos("Saturation min", "Tuning")
        s_max = cv2.getTrackbarPos("Saturation max", "Tuning")
        v_min = cv2.getTrackbarPos("Value min", "Tuning")
        v_max = cv2.getTrackbarPos("Value max", "Tuning")

        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])

        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(frame, frame, mask=mask)

        info = f"H:{h_min}-{h_max} S:{s_min}-{s_max} V:{v_min}-{v_max}"

        cv2.putText(
            frame,
            info,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 255),
            2
        )

        cv2.imshow("Original", frame)
        cv2.imshow("Maske", mask)
        cv2.imshow("Ergebnis", result)

        key = cv2.waitKey(1)

        if key == 27:
            break

        if key == ord("p"):
            print()
            print("Aktuelle HSV-Werte:")
            print(f"LOWER = np.array([{h_min}, {s_min}, {v_min}])")
            print(f"UPPER = np.array([{h_max}, {s_max}, {v_max}])")

    cap.release()
    cv2.destroyAllWindows()
