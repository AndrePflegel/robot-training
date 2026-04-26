from modules.cam_test import run_camera_test
from modules.color_detection import run_color_detection
from modules.line_detection import run_line_detection
from modules.multi_color_detection import run_multi_color_detection
from modules.robot_logic import run_robot_logic
from modules.digit_prepare import run_digit_prepare
from modules.digit_recognition import run_digit_recognition
from modules.tuning_panel import run_tuning_panel
from modules.tuning_gui import run_tuning_gui

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
	print("8 - Tuning Panel Farben")
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
			print("Modell auswählen:")
			print("1 - MNIST")
			print("2 - Custom")
			print("3 - Dual: Custom zuerst, sonst MNIST")
			model_choice = input("Auswahl: ")
			
			if model_choice == "2":
			    run_digit_recognition("custom")
			elif model_choice == "3":
			    run_digit_recognition("dual")
			else:
			    run_digit_recognition("mnist")
		elif choice == "8":
			run_tuning_gui()
		elif choice == "0":
			print("Programm beendet.")
			break
		else:
			print("Ungültige Auswahl.")

if __name__ == "__main__":
	main()
