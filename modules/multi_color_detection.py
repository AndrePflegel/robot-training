import cv2
import numpy as np

def run_multi_color_detection():


	cap = cv2.VideoCapture(0)

	state = "Unbekannt"

	while True:
		ret, frame = cap.read()
		if not ret:
			break

		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		#Rot
		lower_red1 = np.array([0, 120, 70])
		upper_red1 = np.array([10, 255, 255])
		lower_red2 = np.array([170, 120, 70])
		upper_red2 = np.array([180, 255, 255])

		mask_red = cv2.inRange(hsv, lower_red1, upper_red1) + \
				cv2.inRange(hsv, lower_red2, upper_red2)

		#Grün
		lower_green = np.array([40, 70, 70])
		upper_green = np.array([80, 255, 255])

		mask_green = cv2.inRange(hsv, lower_green, upper_green)

		#Pixel zählen
		red_pixels = cv2.countNonZero(mask_red)
		green_pixels = cv2.countNonZero(mask_green)

		#Entscheidung
		if red_pixels > 2000:
			state = "STOP"
		elif green_pixels > 2000:
			state = "GO"
		else:
			state = "WAIT"

		#Anzeige
		cv2.putText(frame, state, (50, 50),
				cv2.FONT_HERSHEY_SIMPLEX, 1,
				(255, 255, 0), 2)

		cv2.imshow("Frame", frame)
		cv2.imshow("Red Mask", mask_red)
		cv2.imshow("Green Mask", mask_green)

		if cv2.waitKey(1) == 27:
			break

	cap.release()
	cv2.destroyAllWindows()
