# Robot Training

Kleines Trainingsprojekt zur Vorbereitung auf ein Robotik-/KI-Projekt mit Python, OpenCV und Kamera.

Das Projekt testet grundlegende Bildverarbeitung mit einer Webcam.  
Die entwickelten Module können später auf einem Raspberry Pi oder einem fahrbaren Roboter eingesetzt werden.

---

## Aktueller Stand

### 1. Kamera-Test

Datei:
cam_test.py

Funktion:
- öffnet die Webcam
- zeigt ein Livebild an
- beendet das Programm mit ESC

Start:
python3 cam_test.py

---

### 2. Farberkennung

Datei:
color_detect.py

Funktion:
- erkennt rote Flächen im Kamerabild
- erstellt eine Schwarz-Weiß-Maske
- markiert das größte rote Objekt mit einem Rahmen
- berechnet den Mittelpunkt des Objekts
- zeigt an, ob das Objekt links, mittig oder rechts im Bild liegt

Start:
python3 color_detect.py

Verwendung:
Ein rotes Objekt vor die Kamera halten.  
Das erkannte Objekt wird eingerahmt und klassifiziert (Links / Mitte / Rechts).

---

### 3. Linienerkennung

Datei:
line_detect.py

Funktion:
- verwendet nur den unteren Bereich des Kamerabildes (ROI)
- erkennt schwarze Linien
- entfernt Störungen durch Filterung
- berechnet die Position der Linie
- gibt eine Fahrtrichtung aus:

Links lenken  
Rechts lenken  
Geradeaus  
Keine Linie

Start:
python3 line_detect.py

Verwendung:
Ein weißes Blatt mit schwarzer Linie oder Klebeband vor die Kamera halten.

---

### 4. Mehrfarb-Erkennung (Zustände)

Datei:
multi_color.py

Funktion:
- erkennt mehrere Farben gleichzeitig
- definiert einfache Zustände:

ROT   → STOP  
GRÜN  → GO  
KEIN SIGNAL → WAIT  

Start:
python3 multi_color.py

---

## Installation (Ubuntu / Linux Mint)

### 1. Repository klonen

git clone https://github.com/AndrePflegel/robot-training.git  
cd robot-training

---

### 2. Benötigte Pakete installieren

sudo apt update  
sudo apt install python3 python3-opencv python3-numpy -y

---

### 3. OpenCV testen

python3 -c "import cv2; print(cv2.__version__)"

Wenn eine Versionsnummer erscheint, ist OpenCV korrekt installiert.

---

### 4. Kamera prüfen

ls /dev/video*

Die Kamera ist meist unter /dev/video0 erreichbar.

---

## Bedienung

Alle Programme werden im Terminal gestartet.

Beenden:
ESC

---

## Projektstruktur

robot-training/
├── cam_test.py
├── color_detect.py
├── line_detect.py
├── multi_color.py
└── README.md

---

## Technisches Prinzip

Kamera → Bild erfassen → OpenCV verarbeitet Bild → Ergebnis anzeigen → Entscheidung treffen

Beispiele:

Rotes Objekt links  → Links  
Rotes Objekt mittig → Mitte  
Schwarze Linie rechts → Rechts lenken  

---

## Hinweise

Dieses Projekt enthält:
- keine Motorsteuerung
- keine selbst trainierten KI-Modelle

Es dient als Trainingsprojekt für Bildverarbeitung und Entscheidungslogik.

---

## Mögliche Erweiterungen

- mehrere Farben gleichzeitig auswerten
- Linienverfolgung weiter verbessern
- Zahlenerkennung (MNIST / KI-Modell)
- Handgesten erkennen
- Motorsteuerung für Raspberry Pi integrieren
- Kombination aus Linie + Farbe (z. B. STOP bei Rot)
