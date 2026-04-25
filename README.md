#Robot Training

Kleines Trainingsprojekt zur Vorbereitung auf ein Robotik-/KI-Projekt mit Python, OpenCV und Kamera.

Das Projekt testet grundlegende Bildverarbeitung mit einer Webcam. Später können diese Bausteine auf einem Rasperry Pi oder einen fahrbaren Roboter übertragen werden.

## Aktueller Stand

### 1. Kamera-Test

'''text
cam_test.py

Funktion:
- öffnet die Webcam
- zeigt ein Livebild an
- beendet das Programm mit ESC

Start (in der konsole):
python3 cam_text.py

### Farberkennung

Datei:
color_detect.py

Funktion:
-erkennt rote Flächen im Kamerabild
-erstellt eine Schwarz-Weiß-Maske
-markiert das größte rote Objekt mit einem Rahmen
-berechnet den Mittelpunkt des Objekts
-zeigt an, ob das Objekt links, mittig oder rechts im Bild liegt

Start (in der Konsole):
python3 color_detect.py

Verwendung:
Ein rotes Objekt vor die Kamera halten. Das erkannte Objekt wird eingerahmt.

### Linienerkennung

Datei:
line_detect.py

Funktion:
-verwendet den unteren Bereich des Kamerabildes
-erkennt dunkle bzw. schwarze Linien
-markiert erkannte Linien
-berechnet die Position der Linie
-gibt eine einfache Richtung aus:
	links lenken
	Rechts lenken
	Geradeaus
	Keine Linie

Start (in der Konsole):
python3 line_detect.py

Verwendung:

Ein weißes Blatt mit schwarzer Linie oder schwarzes Klebeband vor die Kamera halten.

## installation auf Ubuntu/Linux Mint

1. repository herunterladen

konsole:
git clone https://github.com/AndrePflegel/robot-training.git
cd robot-training

2. benötigte Pakete installieren

sudo apt update
sudo apt install python3 python3-opencv python3-numpy -y

3. OpenCV testen

python3 -c "import cv2; print(cv2.__version__)"

Wenn eine Versionsnummer erscheint, ist openCV installiert

4. Kamera prüfen

ls /dev/video*

Meistens ist die Kamera unter /dev/video0 erreichbar

Bedienung

Alle Programme werden im Terminal gestartet

Beenden:
ESC

### Projektstruktur

robot-training/
|––cam_test.py
|––color_detect.py
|––line_detect.py
|––README.md

### technisches Prinzip
Das Projekt folgt dem grundprinzip:

Kamera->Bild erfassen->OpenCV verarbeitet Bild-> Ergebnis anzeigen->einfache Entscheidung treffen

Beispiele:
Rotes objekt links -> Links
Rotes Objekt mittig -> Mitte
Schwarze Linie rechts -> Rechts lenken

## hinweise
Dieses Projekt enthält noch keine Motorsteuerung und keine echte KI-Modell-Anbindung.
Es ist ein Trainingsprojekt für Bildverarbeitung und einfache Entscheidungslogik, was man kurz und
einfach am eigenen Laptop (wenn eine Webcam installiert ist) ausprobieren kann.

## Spätere Erweiterungen:
-mehrere Farben erkennen
-Linienverfolgung verbessern
-Zahlenerkennung integrieren
-handgesten erkennen
Motorsteuerung für RasperyPi ergänzen
