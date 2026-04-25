# Zahlenerkennung mit MNIST

Dieses Dokument erklärt die Vorbereitung und Erkennung handgeschriebener Zahlen.

Das Projekt nutzt ein trainiertes Modell, das Zahlen von 0 bis 9 erkennen kann.

---

## Ziel

Das System soll eine Zahl aus dem Kamerabild erkennen.

Der Ablauf ist:

```text
Kamera -> Ausschnitt -> Graustufen -> Schwarz-Weiß -> 28x28 Pixel -> Modell -> Zahl
```

---

## Warum 28x28 Pixel?

Der MNIST-Datensatz besteht aus Bildern mit 28x28 Pixeln.

Damit unser Kamerabild zum Modell passt, muss der erkannte Bereich ebenfalls auf 28x28 Pixel skaliert werden.

---

## MNIST

MNIST ist ein bekannter Datensatz mit handgeschriebenen Ziffern.

Er enthält viele Beispiele für die Zahlen 0 bis 9.

Das Modell lernt nicht im laufenden Programm. Es wurde vorher trainiert und wird später nur benutzt.

Diese Benutzung nennt man Inference.

---

## Modell trainieren

Das Training passiert in:

```text
train_digit_model.py
```

Das Script lädt MNIST, trainiert ein Modell und speichert es unter:

```text
models/digit_model.keras
```

---

## Modell laden

In der Erkennung wird das Modell geladen:

```python
model = tf.keras.models.load_model("models/digit_model.keras")
```

Danach kann es Zahlen vorhersagen.

---

## Kamera-Ausschnitt

Die Zahl wird nicht im ganzen Bild gesucht.

Stattdessen wird ein fester Bereich in der Mitte verwendet:

```python
box_size = 220
x1 = width // 2 - box_size // 2
y1 = height // 2 - box_size // 2
x2 = width // 2 + box_size // 2
y2 = height // 2 + box_size // 2
```

Warum?

- weniger Störungen
- klarer Bereich für den Benutzer
- einfacher zu verstehen
- schneller zu verarbeiten

---

## Graustufen

```python
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
```

Farbe ist für die Ziffer nicht wichtig.

Wichtig ist nur:

```text
hell oder dunkel
```

---

## Weichzeichnen

```python
blur = cv2.GaussianBlur(gray, (5, 5), 0)
```

Das reduziert Bildrauschen.

Dadurch wird die Zahl ruhiger und klarer verarbeitet.

---

## Schwarz-Weiß-Bild erzeugen

```python
_, threshold = cv2.threshold(
    blur,
    100,
    255,
    cv2.THRESH_BINARY_INV
)
```

Bedeutung:

- dunkle Bereiche werden weiß
- helle Bereiche werden schwarz

Warum invertiert?

MNIST arbeitet typischerweise mit heller Ziffer auf dunklem Hintergrund.

---

## Auf 28x28 verkleinern

```python
resized = cv2.resize(threshold, (28, 28))
```

Das Kamerabild wird auf die gleiche Größe gebracht, die das Modell erwartet.

---

## Normalisierung

```python
normalized = resized / 255.0
```

Pixelwerte liegen ursprünglich zwischen 0 und 255.

Das Modell arbeitet besser mit Werten zwischen 0 und 1.

---

## Eingabeform für das Modell

```python
input_image = normalized.reshape(1, 28, 28)
```

Das Modell erwartet eine Sammlung von Bildern.

Auch wenn wir nur ein einzelnes Bild haben, muss es als Sammlung mit einem Bild übergeben werden.

---

## Vorhersage

```python
prediction = model.predict(input_image, verbose=0)
```

Das Modell gibt Wahrscheinlichkeiten für alle Zahlen aus.

Beispiel:

```text
0 -> 0.01
1 -> 0.02
2 -> 0.90
3 -> 0.03
...
```

---

## Ergebnis bestimmen

```python
digit = int(np.argmax(prediction))
confidence = float(np.max(prediction))
```

`np.argmax` liefert die Zahl mit der höchsten Wahrscheinlichkeit.

`np.max` liefert die Sicherheit dieser Entscheidung.

---

## Unsicherheit

```python
if confidence < 0.70:
    text = "Unsicher"
```

Wenn das Modell zu unsicher ist, wird keine Zahl als sicher akzeptiert.

Warum?

- verhindert falsche Entscheidungen
- wichtig für spätere Roboterlogik
- besser stoppen oder warten als falsch reagieren

---

## Typische Probleme

### Zahl wird falsch erkannt

Mögliche Gründe:

- Zahl ist nicht mittig
- zu wenig Kontrast
- zu viel Hintergrund
- Handschrift unterscheidet sich stark von MNIST
- Bild ist unscharf

### Sicherheit ist niedrig

Mögliche Gründe:

- Zahl ist zu klein
- Zahl ist zu schräg
- Licht ist schlecht
- Hintergrund stört

### Modell erkennt immer dieselbe Zahl

Mögliche Gründe:

- Threshold falsch
- Bild ist zu dunkel
- Bild ist zu hell
- 28x28-Vorschau sieht nicht wie eine Zahl aus

---

## Was kann man verbessern?

Mögliche Verbesserungen:

- Zahl automatisch zentrieren
- größte Kontur ausschneiden
- Hintergrund besser entfernen
- Threshold an Licht anpassen
- mehrere Bilder auswerten
- nur Ergebnis akzeptieren, wenn mehrere Frames gleich sind

---

## Wichtiger Unterschied

Das System lernt nicht während der Nutzung.

Es nutzt ein fertig trainiertes Modell.

```text
Training    -> Modell lernt aus Beispielen
Inference   -> Modell wird benutzt
```

In diesem Projekt findet das Training in `train_digit_model.py` statt.

Die Erkennung findet in `modules/digit_recognition.py` statt.

---

## Zusammenfassung

Die Zahlenerkennung besteht aus zwei Teilen:

```text
1. Modell trainieren
2. Modell benutzen
```

Das Kamerabild muss passend vorbereitet werden, damit es ähnlich aussieht wie die MNIST-Trainingsdaten.

Nur dann kann das Modell sinnvoll arbeiten.
