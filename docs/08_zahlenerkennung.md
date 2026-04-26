# Zahlenerkennung (MNIST + Custom + Dual)

Dieses Modul erkennt Zahlen im Kamerabild und kombiniert mehrere Modelle.

---

## Ziel

Das System soll eine Zahl zuverlässig erkennen – auch unter realen Bedingungen:

* unterschiedliche Beleuchtung
* gedruckte oder handgeschriebene Zahlen
* Kamera-Rauschen

---

## Gesamtpipeline

```text
Kamera
→ ROI (Bildbereich)
→ Threshold (Schwarz/Weiß)
→ größte Kontur
→ Zentrierung
→ 28x28 Bild
→ Modell(e)
→ Entscheidung
```

---

## Modelle im System

Es gibt drei Betriebsarten:

```text
MNIST   → Standardmodell
Custom  → eigenes, nachtrainiertes Modell
Dual    → Kombination beider Modelle
```

---

## MNIST-Modell

* basiert auf dem MNIST-Datensatz
* kennt viele handgeschriebene Zahlen
* sehr stabil, aber nicht perfekt für Kamera-Bilder

---

## Custom-Modell

* basiert auf deinen eigenen Kamerabildern
* wird mit `train_custom_model.py` trainiert
* passt sich deiner Umgebung an

Speicherort:

```text
models/digit_model_custom.keras
```

---

## Dual-Modus (wichtig)

Im Dual-Modus:

```text
Custom wird zuerst verwendet
wenn unsicher → MNIST übernimmt
```

Warum?

* Custom kennt deine Umgebung
* MNIST ist allgemeiner
  → Kombination = bessere Ergebnisse

---

## Datensammlung (Lernen)

Während das Programm läuft:

```text
Taste 0–9 drücken
→ aktuelles Bild wird gespeichert
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

## Training (Fine-Tuning)

```bash
python train_custom_model.py
```

Dabei:

```text
MNIST-Modell wird geladen
+ deine Bilder werden ergänzt
→ neues Modell wird gespeichert
```

---

## Bildvorbereitung

Damit das Modell funktioniert, wird das Bild vorbereitet:

### 1. ROI (Ausschnitt)

Nur der mittlere Bereich wird verwendet:

```text
weniger Störungen
klarer Fokus
```

---

### 2. Threshold

```text
Graustufen → Schwarz/Weiß
```

Ziel:

```text
Zahl = weiß
Hintergrund = schwarz
```

---

### 3. Kontur

```text
größte Form im Bild wird genommen
```

Warum?

* entfernt Störungen
* isoliert die Zahl

---

### 4. Zentrierung

Die Zahl wird in die Mitte gesetzt.

Warum?

MNIST erwartet:

```text
zentrierte Ziffern
```

---

### 5. Skalierung

```text
28x28 Pixel
```

Das ist das Format des Modells.

---

## Modellentscheidung

Jedes Modell liefert:

```text
Zahl + Confidence
```

Beispiel:

```text
MNIST: 3 (0.91)
CUSTOM: 7 (0.42)
```

Final:

```text
3 (MNIST)
```

---

## Stabilisierung

Das System speichert mehrere Ergebnisse:

```python
deque(maxlen=10)
```

Nur wenn mehrere Frames gleich sind:

```text
Ergebnis wird stabil angezeigt
```

---

## Typische Probleme

### Zahl wird nicht erkannt

* Threshold falsch
* zu wenig Kontrast
* Zahl zu klein

---

### falsche Zahl

* ungewöhnliche Handschrift
* schlechte Zentrierung
* Hintergrund stört

---

### niedrige Confidence

* Bild unscharf
* Licht schlecht
* zu wenig Trainingsdaten

---

## Wichtig

Das System lernt NICHT automatisch.

```text
Du musst Daten sammeln + Modell neu trainieren
```

---

## Zusammenfassung

```text
Kamera → Bild vorbereiten → Modelle → Entscheidung
```

Mit:

```text
MNIST = Basiswissen
Custom = Umgebung
Dual = Kombination
```

