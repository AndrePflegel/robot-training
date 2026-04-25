import cv2
import numpy as np

cap = cv2.VideoCapture(0)

last_direction = "Keine Linie"

while True:
	ret, frame = cap.read()

	if not ret:
		print("Keine Kamera erkannt")
		break

	# Bildgröße holen
	height, width = frame.shape[:2]

	#Nur unteren Bildbereich verwenden
	roi_start = int(height * 0.6)
	roi = frame[roi_start:height, 0:width]

	#In Graustufen umwandeln
	gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

	#Leicht weichzeichnen gegen Bildrauschen
	blur = cv2.GaussianBlur(gray, (5, 5), 0)

	#schwarze Linien erkennen
	_, mask = cv2.threshold(blur, 80, 255, cv2.THRESH_BINARY_INV)

	#Störungen entfernen
	kernel = np.ones((5, 5), np.uint8)
	mask = cv2.erode(mask, kernel, iterations=1)
	mask = cv2.dilate(mask, kernel, iterations=2)

	#Konturen finden
	contours, _ = cv2.findContours(
		mask,
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

			left_limit = width // 3
			right_limit = 2 * width // 3

			if cx < left_limit:
				direction = "Links lenken"
			elif cx > right_limit:
				direction = "Rechts lenken"
			else:
				direction = "Geradeaus"
			
			last_direction = direction
		else:
			direction = last_direction


	#Orientierungslinien im ROI
	cv2.line(roi, (width // 3, 0), (width // 3, roi.shape[0]), (255, 255, 0), 2)
	cv2.line(roi, (2 * width // 3, 0), (2 * width // 3, roi.shape[0]), (255, 255, 0), 2)

	#ROI-Grenze im Originalbild
	cv2.line(frame, (0, roi_start), (width, roi_start), (255, 0, 0), 2)

	cv2.putText(
		frame,
		direction,
		(50, 50),
		cv2.FONT_HERSHEY_SIMPLEX,
		1,
		(0, 0, 255),
		2
	)

	cv2.imshow("Linienerkennung", frame)
	cv2.imshow("Maske", mask)

	if cv2.waitKey(1) == 27:
		break

cap.release()
cv2.destroyAllWindows()
