import cv2
import numpy as np

cap = cv2.VideoCapture(0)

last_direction = "Keine Linie"

while True:
	ret, frame = cap.read()

	if not ret:
		print("Keine Kamera erkannt")
		break

	height, width = frame.shape[:2]

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	#Rot erkennen
	lower_red1 = np.array([0, 120, 70])
	upper_red1 = np.array([10, 255, 255])
	lower_red2 = np.array([170, 120, 70])
	upper_red2 = np.array([180, 255, 255])

	mask_red = cv2.inRange(hsv, lower_red1, upper_red1) + cv2.inRange(hsv, lower_red2, upper_red2)

	#Grün erkennen
	lower_green = np.array([40, 70, 70])
	upper_green = np.array([80, 255, 255])

	mask_green = cv2.inRange(hsv, lower_green, upper_green)

	red_pixels = cv2.countNonZero(mask_red)
	green_pixels = cv2.countNonZero(mask_green)

	#Linienerkennung nur im unteren Bildbereich
	roi_start = int(height * 0.6)
	roi = frame[roi_start:height, 0:width]

	gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray, (5, 5), 0)

	_, mask_line = cv2.threshold(blur, 80, 255, cv2.THRESH_BINARY_INV)

	kernel = np.ones((5, 5), np.uint8)
	mask_line = cv2.erode(mask_line, kernel, iterations=1)
	mask_line = cv2.dilate(mask_line, kernel, iterations=2)

	contours, _ = cv2.findContours(
		mask_line,
		cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE
	)

	direction = "Keine Linie"

	if len(contours) > 0:
		biggest = max(contours, key=cv2.contourArea)
		area = cv2.contourArea(biggest)

		if area > 800:
			x, y, w, h = cv2.boundingRect(biggest)

			cx = x + w // 2
			cy = y + h // 2

			cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
			cv2.circle(roi, (cx, cy), 6, (255, 0, 0), -1)

			if cx < width // 3:
				direction = "Links lenken"
			elif cx > 2 * width // 3:
				direction = "Rechts lenken"
			else:
				direction = "geradeaus"

			last_direction = direction
		else:
			direction = last_direction

	#Entscheidung: farbe hat Vorrang vor Linie
	if red_pixels > 2000:
		action = "STOP"
	elif green_pixels > 2000:
		action = "GO: " + direction
	else:
		action = "WAIT: " + direction

	#Hilfslinien anzeigen
	cv2.line(roi, (width // 3, 0), (width // 3, roi.shape[0]), (255, 255, 0), 2)
	cv2.line(roi, (2 * width // 3, 0), (2 * width // 3, roi.shape[0]), (255, 255, 0), 2)
	cv2.line(frame, (0, roi_start), (width, roi_start), (255, 0, 0), 2)

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
	cv2.imshow("Red Mask", mask_red)
	cv2.imshow("Green Mask", mask_green)

	if cv2.waitKey(1) == 27:
		break

cap.release()
cv2.destroyAllWindows()
