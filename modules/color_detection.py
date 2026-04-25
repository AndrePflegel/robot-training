import cv2
import numpy as np

def run_color_detection():


	cap = cv2.VideoCapture(0)

	while True:
		ret, frame = cap.read()
		if not ret:
			print("Keine Kamera erkannt")
			break

		# Bild von BGR -> HSV umwandeln
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		# ROT (unterer Bereich) Rot liegt im HSV-Farbraum an 2 Bereichen
		lower_red1 = np.array([0, 120, 70])
		upper_red1 = np.array([10, 255, 255])

		#ROT (oberer Bereich)
		lower_red2 = np.array([170, 120, 70])
		upper_red2 = np.array([180, 255, 255])

		#Masken kombinieren/Maske für rote Bereiche erstellen
		mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
		mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
		mask = mask1 + mask2

		# Konturen finden
		contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		if len(contours) > 0:
			biggest = max(contours, key=cv2.contourArea)
			area = cv2.contourArea(biggest)

			#Kleine Störungen ignorieren
			if area > 1000:
				x, y, w, h = cv2.boundingRect(biggest)

				# Rechteck um das erkannte Objekt zeichnen
				cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

				#Mittelpunkt berechnen
				cx = x + w // 2
				cy = y + h // 2

				#Mittelpunkt anzeigen
				cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

				#Bildbreite bestimmen
				frame_width = frame.shape[1]

				#Position auswerten
				if cx < frame_width // 3:
					direction = "Links"
				elif cx > 2 * frame_width // 3:
					direction = "Rechts"
				else:
					direction = "Mitte"

				# Text am Objekt anzeigen
				cv2.putText(
					frame,
					"Rot erkannt",
					(x, y - 10),
					cv2.FONT_HERSHEY_SIMPLEX,
					0.6,
					(0, 255, 0),
					2
				)

				#Richtung oben anzeigen
				cv2.putText(
					frame,
					direction,
					(50, 50),
					cv2.FONT_HERSHEY_SIMPLEX,
					1,
					(255, 0, 0),
					2
				)

		cv2.imshow("Erkennung", frame)
		cv2.imshow("Maske", mask)

		if cv2.waitKey(1) == 27:
			break

	cap.release()
	cv2.destroyAllWindows()
