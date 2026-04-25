import cv2

cap = cv2.VideoCapture(0)

while True:
	ret, frame = cap.read()

	if not ret:
		print("Keine Kamera erkannt")
		break

	cv2.imshow("Kamera", frame)

	if cv2.waitKey(1) == 27: #ESC
		break

cap.release()
cv2.destroyAllWindows()
