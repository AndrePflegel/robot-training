import cv2
from camera import open_camera, close_camera

def run_camera_test():
	cap = open_camera()

	if cap is None:
		return

	while True:
		ret, frame = cap.read()

		if not ret:
			print("Kein Kamerabild erhalten.")
			break

		cv2.imshow("Kamera-test", frame)

		if cv2.waitKey(1) == 27:
			break

	close_camera(cap)
