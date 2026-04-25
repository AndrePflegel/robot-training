import cv2

def open_camera(camera_index=0):
	cap = cv2.VideoCapture(camera_index)

	if not cap.isOpened():
		print("Kamera konnte nicht geöffnet werden")
		return None

	return cap

def close_camera(cap):
	if cap is not None:
		cap.release()

	cv2.destroyAllWindows()
