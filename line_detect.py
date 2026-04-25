import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
	ret, frame = cap.read()

	if not ret:
		print("Keine Kamera erkannt")
		break

	# Bildgröße holen
	height, width = frame.shape[:2]

	#Nur unteren Bildbereich verwenden
	roi = frame[int(height * 0.6):height, 0:width]

	#In Graustufen umwandeln
	gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

	#schwarze Linien herausfiltern
	_, mask = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)

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

		if area > 500:
			x, y, w, h = cv2.boundingRect(biggest)

			cx = x + w // 2
			cy = y + h // 2

			cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
			cv2.circle(roi, (cx, cy), 5, (255, 0, 0), -1)

			if cx < width // 3:
				direction = "Links lenken"
			elif cx > 2 * width // 3:
				direction = "Rechts lenken"
			else:
				direction = "Geradeaus"

	cv2.putText(frame, direction, (50, 50),
				cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

	#ROT im Originalbild markieren
	cv2.line(frame, (0, int(height * 0.6)), (width, int(height * 0.6)), (255, 0, 0), 2)

	cv2.imshow("Linienerkennung", frame)
	cv2.imshow("Maske", mask)

	if cv2.waitKey(1) == 27:
		break

cap.release()
cv2.destroyAllWindows()
