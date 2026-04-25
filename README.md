# Robot Training

Kleines Trainingsprojekt zur Vorbereitung auf ein Robotik-/KI-Projekt mit Python, OpenCV und Kamera.

Das Projekt testet grundlegende Bildverarbeitung mit einer Webcam. Die entwickelten Module können später auf einem Raspberry Pi oder einem fahrbaren Roboter eingesetzt werden.

---

## Aktueller Stand

Das Projekt wurde von einzelnen Testdateien zu einer modularen Struktur umgebaut.

Der Start erfolgt jetzt zentral über:

```bash
python3 main.py
```

Danach kann im Konsolenmenü ausgewählt werden, welches Modul gestartet werden soll.

---

## Funktionen

### 1. Kamera-Test

Modul:

```text
modules/cam_test.py
```

Funktion:

```text
run_camera_test()
```

Beschreibung:

- öffnet die Webcam
- zeigt ein Livebild an
- beendet das Programm mit ESC

---

### 2. Farberkennung Rot

Modul:

```text
modules/color_detection.py
```

Funktion:

```text
run_color_detection()
```

Beschreibung:

- erkennt rote Flächen im Kamerabild
- erstellt eine Schwarz-Weiß-Maske
- markiert das größte rote Objekt mit einem Rahmen
- berechnet den Mittelpunkt des Objekts
- zeigt an, ob das Objekt links, mittig oder rechts im Bild liegt

---

### 3. Linienerkennung

Modul:

```text
modules/line_detection.py
```

Funktion:

```text
run_line_detection()
```

Beschreibung:

- verwendet nur den unteren Bereich des Kamerabildes
- erkennt schwarze Linien
- entfernt kleine Störungen durch Filterung
- markiert die erkannte Linie
- berechnet die Position der Linie
- gibt eine einfache Richtung aus:

```text
Links lenken
Rechts lenken
Geradeaus
Keine Linie
```

---

### 4. Mehrfarb-Erkennung

Modul:

```text
modules/multi_color_detection.py
```

Funktion:

```text
run_multi_color_detection()
```

Beschreibung:

- erkennt mehrere Farben gleichzeitig
- wertet Rot und Grün aus
- erzeugt einfache Zustände:

```text
ROT   -> STOP
GRUEN -> GO
KEIN SIGNAL -> WAIT
```

---

### 5. Robot-Logik

Modul:

```text
modules/robot_logic.py
```

Funktion:

```text
run_robot_logic()
```

Beschreibung:

- kombiniert Linienerkennung und Farberkennung
- Farbe hat Vorrang vor der Linie
- Rot stoppt das System
- Grün erlaubt das Folgen der Linie
- ohne Farbsignal wartet das System, zeigt aber weiterhin die erkannte Linienrichtung an

Logik:

```text
Rot erkannt   -> STOP
Gruen erkannt -> GO + Linienrichtung
Keine Farbe   -> WAIT + Linienrichtung
```

---

## Projektstruktur

```text
robot-training/
├── main.py
├── camera.py
├── README.md
├── modules/
│   ├── __init__.py
│   ├── cam_test.py
│   ├── color_detection.py
│   ├── line_detection.py
│   ├── multi_color_detection.py
│   └── robot_logic.py
└── old/
    ├── cam_test.py
    ├── color_detect.py
    ├── line_detect.py
    └── multi_color.py
```

---

## Installation auf Ubuntu / Linux Mint

### 1. Repository klonen

```bash
git clone https://github.com/AndrePflegel/robot-training.git
cd robot-training
```

### 2. Benötigte Pakete installieren

```bash
sudo apt update
sudo apt install python3 python3-opencv python3-numpy -y
```

### 3. OpenCV testen

```bash
python3 -c "import cv2; print(cv2.__version__)"
```

Wenn eine Versionsnummer erscheint, ist OpenCV korrekt installiert.

### 4. Kamera prüfen

```bash
ls /dev/video*
```

Die Kamera ist meist unter `/dev/video0` erreichbar.

---

## Start

Das Programm wird über die zentrale `main.py` gestartet:

```bash
python3 main.py
```

Im Menü kann anschließend ein Modul ausgewählt werden.

Beenden eines laufenden Kamerafensters:

```text
ESC
```

---

## Technisches Prinzip

Das Projekt folgt diesem Grundprinzip:

```text
Kamera -> Bild erfassen -> OpenCV verarbeitet Bild -> Ergebnis anzeigen -> Entscheidung treffen
```

Die Kamera wird zentral über `camera.py` geöffnet und geschlossen. Die einzelnen Erkennungen liegen getrennt im Ordner `modules`.

Dadurch kann das Projekt einfacher erweitert werden, ohne denselben Code immer wieder in mehrere Dateien zu kopieren.

---

## Hinweise

Dieses Projekt enthält aktuell:

- keine Motorsteuerung
- keine selbst trainierten KI-Modelle
- keine Anbindung an GPIO-Pins

Es dient als Trainingsprojekt für Bildverarbeitung, einfache Entscheidungslogik und Projektstruktur.

---

## Mögliche Erweiterungen

- Linienverfolgung weiter verbessern
- mehrere Farben genauer auswerten
- Zahlenerkennung integrieren
- Handgesten erkennen
- Motorsteuerung für Raspberry Pi ergänzen
- GPIO-Anbindung vorbereiten
- Klassenstruktur für Kamera, Erkennung und Steuerung einführen
