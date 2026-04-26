import cv2
import numpy as np

from modules.line_utils import get_direction_from_center
from modules.line_contour_utils import get_biggest_valid_contour
from modules.profile_loader import load_profiles, get_active_profile
from modules.signal_logic import resolve_action
from modules.color_profile_utils import build_color_masks, apply_color_masks

def decide_action(*args):
    """
    Kompatibilität:
    ALT: decide_action(red_pixels, green_pixels, direction)
    NEU: decide_action(profile, signals)
    """
    
    #Neue Variante
    if len(args) == 2:
        profile, signals = args
        return resolve_action(profile, signals)
        
    #Alte Variante(für Tests)
    elif len(args) == 3:
        red_pixels, green_pixels, direction = args
        
        if red_pixels > 2000:
            return "STOP"
            
        if green_pixels > 2000:
            return f"GO: {direction}"
            
        return f"WAIT: {direction}"
        
    else:
        raise ValueError("Ungültige Argumente für decide_action()")


def run_robot_logic():
    cap = cv2.VideoCapture(0)

    data = load_profiles()
    profile = get_active_profile(data)
    color_masks = build_color_masks(None, profile["colors"])

    last_direction = "Keine Linie"

    while True:
        ret, frame = cap.read()
        signals = []

        if not ret:
            print("Keine Kamera erkannt")
            break

        height, width = frame.shape[:2]

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Farben auswerten
        results = apply_color_masks(hsv, color_masks)

        for result in results:
            if result["pixels"] > 2000:
                signals.append(f"color_{result['name']}")

        # Linienerkennung
        roi_start = int(height * 0.6)
        roi = frame[roi_start:height, 0:width]

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        _, mask_line = cv2.threshold(
            blur,
            80,
            255,
            cv2.THRESH_BINARY_INV
        )

        kernel = np.ones((5, 5), np.uint8)
        mask_line = cv2.erode(mask_line, kernel, iterations=1)
        mask_line = cv2.dilate(mask_line, kernel, iterations=2)

        contours, _ = cv2.findContours(
            mask_line,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        contour_data = [
            (contour, cv2.contourArea(contour))
            for contour in contours
        ]

        biggest = get_biggest_valid_contour(contour_data, min_area=800)

        if biggest is not None:
            x, y, w, h = cv2.boundingRect(biggest)

            cx = x + w // 2
            cy = y + h // 2

            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(roi, (cx, cy), 6, (255, 0, 0), -1)

            direction = get_direction_from_center(cx, width)
            last_direction = direction
        else:
            direction = last_direction

        # Linien-Signal erzeugen
        if direction == "Links lenken":
            signals.append("line_left")
        elif direction == "Rechts lenken":
            signals.append("line_right")
        elif direction == "Geradeaus":
            signals.append("line_center")

        # Entscheidung aus Profil
        action = resolve_action(profile, signals)

        # Visualisierung
        cv2.line(
            roi,
            (width // 3, 0),
            (width // 3, roi.shape[0]),
            (255, 255, 0),
            2
        )
        cv2.line(
            roi,
            (2 * width // 3, 0),
            (2 * width // 3, roi.shape[0]),
            (255, 255, 0),
            2
        )
        cv2.line(
            frame,
            (0, roi_start),
            (width, roi_start),
            (255, 0, 0),
            2
        )

        cv2.putText(
            frame,
            action,
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

        cv2.imshow("Robot Logic", frame)
        cv2.imshow("Line Mask", mask_line)

        for result in results:
            cv2.imshow(result["name"], result["mask"])

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
