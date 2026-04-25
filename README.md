# Robot Training

Trainingsprojekt zur Vorbereitung auf ein Robotik-/KI-Projekt mit Python, OpenCV, Kamera und einfacher Bilderkennung.

Das Projekt zeigt Schritt für Schritt, wie ein Kamerabild verarbeitet wird. Es enthält Beispiele für Kamera-Test, Farberkennung, Linienerkennung, kombinierte Roboter-Logik und Zahlenerkennung mit einem trainierten MNIST-Modell.

---

## Aktueller Stand

Das Projekt besitzt eine modulare Struktur.

Gestartet wird zentral über:

```bash
python main.py
```

Danach kann im Konsolenmenü ein Modul ausgewählt werden.

---

## Funktionen

### 1. Kamera-Test

Modul:

```text
modules/cam_test.py
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

Beschreibung:

- erkennt rote Flächen im Kamerabild
- erstellt eine Schwarz-Weiß-Maske
- markiert das größte rote Objekt
- berechnet den Mittelpunkt
- zeigt an, ob das Objekt links, mittig oder rechts liegt

---

### 3. Linienerkennung

Modul:

```text
modules/line_detection.py
```

Beschreibung:

- wertet nur den unteren Bildbereich aus
- erkennt schwarze Linien
- filtert Störungen
- berechnet die Position der Linie
- gibt eine einfache Fahrtrichtung aus

---

### 4. Mehrfarb-Erkennung

Modul:

```text
modules/multi_color_detection.py
```

Beschreibung:

- erkennt Rot und Grün
- erzeugt einfache Zustände

```text
Rot   -> STOP
Gruen -> GO
Kein Signal -> WAIT
```

---

### 5. Robot-Logik

Modul:

```text
modules/robot_logic.py
```

Beschreibung:

- kombiniert Linienerkennung und Farberkennung
- Rot hat Vorrang und stoppt das System
- Grün erlaubt das Folgen der Linie
- ohne Farbsignal wartet das System

---

### 6. Zahlenerkennung vorbereiten

Modul:

```text
modules/digit_prepare.py
```

Beschreibung:

- schneidet einen Bereich aus dem Kamerabild aus
- wandelt ihn in Graustufen um
- erzeugt ein Schwarz-Weiß-Bild
- skaliert das Ergebnis auf 28x28 Pixel
- bereitet das Bild für ein MNIST-Modell vor

---

### 7. Zahlenerkennung

Modul:

```text
modules/digit_recognition.py
```

Beschreibung:

- lädt ein trainiertes MNIST-Modell
- verarbeitet den Kamerabereich auf 28x28 Pixel
- erkennt Zahlen von 0 bis 9
- zeigt die erkannte Zahl und die Sicherheit an

---

## Projektstruktur

```text
robot-training/
├── main.py
├── camera.py
├── train_digit_model.py
├── requirements.txt
├── README.md
├── models/
│   └── digit_model.keras
├── modules/
│   ├── __init__.py
│   ├── cam_test.py
│   ├── color_detection.py
│   ├── line_detection.py
│   ├── multi_color_detection.py
│   ├── robot_logic.py
│   ├── digit_prepare.py
│   └── digit_recognition.py
├── docs/
│   ├── 01_kamera.md
│   ├── 02_farberkennung.md
│   ├── 03_linienerkennung.md
│   ├── 04_mehrfarb.md
│   ├── 05_robot_logic.md
│   ├── 06_main_und_struktur.md
│   ├── 07_parameter_und_tuning.md
│   └── 08_zahlenerkennung.md
└── old/
```

---

## Installation auf Ubuntu / Linux Mint

### 1. Repository klonen

```bash
git clone https://github.com/AndrePflegel/robot-training.git
cd robot-training
```

### 2. Virtuelle Umgebung erstellen

```bash
python3 -m venv venv
```

### 3. Virtuelle Umgebung aktivieren

```bash
source venv/bin/activate
```

Danach sollte im Terminal vorne stehen:

```text
(venv)
```

### 4. Pakete installieren

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Installation testen

```bash
python -c "import cv2; print(cv2.__version__)"
python -c "import tensorflow as tf; print(tf.__version__)"
```

Wenn Versionsnummern erscheinen, sind OpenCV und TensorFlow korrekt installiert.

---

## Start

```bash
source venv/bin/activate
python main.py
```

Im Menü kann anschließend ein Modul ausgewählt werden.

Ein laufendes Kamerafenster wird mit ESC beendet.

---

## MNIST-Modell neu trainieren

Das trainierte Modell liegt unter:

```text
models/digit_model.keras
```

Falls es neu erzeugt werden soll:

```bash
source venv/bin/activate
python train_digit_model.py
```

Danach wird das Modell erneut gespeichert.

---

## Technisches Prinzip

Das Projekt folgt diesem Grundprinzip:

```text
Kamera -> Bild erfassen -> OpenCV verarbeitet Bild -> Ergebnis anzeigen -> Entscheidung treffen
```

Bei der Zahlenerkennung kommt zusätzlich ein trainiertes Modell dazu:

```text
Kamera -> Bild vorbereiten -> 28x28 Pixel -> Modell -> erkannte Zahl
```

---

## Hinweise

Dieses Projekt enthält aktuell:

- keine Motorsteuerung
- keine GPIO-Anbindung
- keine echte Roboter-Hardware-Steuerung

Es dient als Trainingsprojekt für Bildverarbeitung, einfache Entscheidungslogik, Projektstruktur und erste Nutzung eines trainierten Modells.

---

## Mögliche Erweiterungen

- Zahlenerkennung stabilisieren
- Buchstabenerkennung ergänzen
- Handgesten erkennen
- Motorsteuerung für Raspberry Pi ergänzen
- GPIO-Anbindung vorbereiten
- Klassenstruktur für Kamera, Erkennung und Steuerung einführen
