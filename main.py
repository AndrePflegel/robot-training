from modules.cam_test import run_camera_test
from modules.color_detection import run_color_detection
from modules.line_detection import run_line_detection
from modules.multi_color_detection import run_multi_color_detection
from modules.robot_logic import run_robot_logic
from modules.digit_prepare import run_digit_prepare
from modules.digit_recognition import run_digit_recognition

def print_menu():
	print()
	print("Robot Training")
	print("=============")
	print("1 - Kamera-Test")
	print("2 - Farberkennung mit Masken")
	print("3 - Linienerkennung")
	print("4 - Farbzustand: STOP / GO / WAIT")
	print("5 - Robot-Logik: Linie + Farbe")
	print("6 - Zahlenerkennung vorbereiten")
	print("7 - Zahlenerkennung")
	print("0 - Beenden")
	print()


def main():
	while True:
		print_menu()
		choice = input("Auswahl: ")

		if choice == "1":
			run_camera_test()
		elif choice == "2":
			run_color_detection()
		elif choice == "3":
			run_line_detection()
		elif choice == "4":
			run_multi_color_detection()
		elif choice == "5":
			run_robot_logic()
		elif choice == "6":
			run_digit_prepare()
		elif choice == "7":
			run_digit_recognition()
		elif choice == "0":
			print("Programm beendet.")
			break
		else:
			print("Ungültige Auswahl.")

if __name__ == "__main__":
	main()
