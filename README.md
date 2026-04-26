# Robot Training

Trainingsprojekt zur Vorbereitung auf ein Robotik-/KI-Projekt mit Python, OpenCV, Kamera und Bilderkennung.

Das Projekt zeigt Schritt für Schritt, wie ein Kamerabild verarbeitet wird – von einfacher Farberkennung bis hin zu einer lernfähigen Zahlenerkennung mit mehreren Modellen.

---

## Aktueller Stand

Das Projekt ist modular aufgebaut und wird über ein Menü gestartet:

```bash
python main.py
```

Danach kann ein Modul im Konsolenmenü ausgewählt werden.

---

## Funktionen

### 1. Kamera-Test

* öffnet die Webcam
* zeigt das Livebild
* ESC beendet das Fenster

---

### 2. Farberkennung (Rot + Grün)

* erkennt mehrere Farben (konfigurierbar)
* zeigt Masken
* berechnet Position im Bild
* nutzt Parameter aus `config/settings.py`

---

### 3. Linienerkennung

* analysiert unteren Bildbereich
* erkennt schwarze Linien
* filtert Störungen
* bestimmt Fahrtrichtung

---

### 4. Farbzustände (STOP / GO / WAIT)

* Rot → STOP
* Grün → GO
* kein Signal → WAIT

---

### 5. Robot-Logik

* kombiniert Farbe + Linie
* priorisiert STOP über Bewegung
* einfache Entscheidungslogik

---

### 6. Zahl vorbereiten

* ROI aus Bild schneiden
* Thresholding
* größte Kontur extrahieren
* Zentrierung (MNIST-ähnlich)
* Ausgabe als 28x28 Bild

---

### 7. Zahlenerkennung

Pipeline:

```text
Bild → Threshold → Kontur → Zentrierung → Modell → Ergebnis
```

Features:

* MNIST-Modell (Basis)
* eigenes Custom-Modell (Fine-Tuning)
* Dual-Modus (Custom → fallback MNIST)
* Stabilisierung über mehrere Frames
* Confidence-Auswertung
* Debug-Anzeige

Beispiel:

```text
MNIST: 3 (0.91)
CUSTOM: 7 (0.42)
Final: 3 (MNIST)
```

---

## Lernfähiges System

Während der Laufzeit:

```text
Taste 0–9 drücken → aktuelles Bild speichern
```

Speicherort:

```text
data/corrections/<Zahl>/
```

Beispiel:

```text
data/corrections/1/20260426_193012.png
```

---

## Eigenes Modell trainieren

```bash
python train_custom_model.py
```

Dabei passiert:

```text
MNIST-Modell wird geladen
+ eigene Daten werden ergänzt
→ neues Modell wird gespeichert
```

Output:

```text
models/digit_model_custom.keras
```

---

## Modell-Auswahl

Im Menü:

```text
1 → MNIST
2 → Custom
3 → Dual (empfohlen)
```

Dual-Modus:

```text
Custom wird zuerst genutzt
wenn unsicher → MNIST übernimmt
```

---

## Projektstruktur

```text
robot-training/
├── main.py
├── camera.py
├── train_digit_model.py
├── train_custom_model.py
├── requirements.txt
├── README.md
├── config/
│   └── settings.py
├── data/
│   └── corrections/
├── models/
│   ├── digit_model.keras
│   └── digit_model_custom.keras
├── modules/
│   ├── cam_test.py
│   ├── color_detection.py
│   ├── line_detection.py
│   ├── multi_color_detection.py
│   ├── robot_logic.py
│   ├── digit_prepare.py
│   ├── digit_recognition.py
│   ├── digit_dataset_utils.py
│   ├── digit_preprocess_utils.py
│   ├── digit_result_utils.py
│   ├── digit_stability_utils.py
│   ├── line_utils.py
│   ├── line_contour_utils.py
│   ├── color_state_utils.py
│   └── model_loader.py
├── tests/
└── docs/
```

---

## Installation (Ubuntu / Linux Mint)

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

### 4. Pakete installieren

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. GUI Voraussetzung

```bash
sudo apt install python3-tk
```

---

## Start

```bash
source venv/bin/activate
python main.py
```

ESC beendet Kamerafenster.

---

## Tests

```bash
pytest
```

---

## Technisches Prinzip

```text
Kamera
→ Bildverarbeitung (OpenCV)
→ Feature-Extraktion
→ Modell (TensorFlow)
→ Entscheidung
```

Zahlenerkennung:

```text
ROI → Threshold → Kontur → Zentrierung → 28x28 → Modell
```

---

## Hinweise

Aktuell KEINE:

* Motorsteuerung
* GPIO
* Hardware-Anbindung

Projekt dient als Trainingsbasis für:

* Bildverarbeitung
* ML-Grundlagen
* Softwarestruktur
* Debugging & Testing

---

## Mögliche Erweiterungen

* besseres Modell (CNN)
* Buchstabenerkennung
* Objekterkennung
* erweitertes Tuning-Panel
* Raspberry Pi Integration
* echte Robotersteuerung

