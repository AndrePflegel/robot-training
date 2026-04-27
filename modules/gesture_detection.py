import cv2
import mediapipe as mp


class HandGestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )
        self.mp_draw = mp.solutions.drawing_utils

    def count_fingers(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(frame_rgb)

        if not result.multi_hand_landmarks:
            return 0, None

        hand_landmarks = result.multi_hand_landmarks[0]
        lm = hand_landmarks.landmark

        fingers = []

        # Daumen
        if lm[4].x < lm[3].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # Zeige-, Mittel-, Ring-, kleiner Finger
        finger_tips = [8, 12, 16, 20]
        finger_pips = [6, 10, 14, 18]

        for tip, pip in zip(finger_tips, finger_pips):
            if lm[tip].y < lm[pip].y:
                fingers.append(1)
            else:
                fingers.append(0)

        count = sum(fingers)

        return count, hand_landmarks

    def draw_hand(self, frame, hand_landmarks):
        if hand_landmarks:
            self.mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS
            )
