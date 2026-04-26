# Parameter und Tuning

Dieses Dokument erklärt wichtige Zahlenwerte im Projekt.

Viele Werte in der Bildverarbeitung sind nicht fest vorgegeben. Sie werden ausprobiert, angepasst und an Kamera, Licht und Umgebung angepasst.

---

## Warum gibt es so viele Zahlenwerte?

Bildverarbeitung hängt stark ab von:

- Licht
- Kameraqualität
- Abstand zum Objekt
- Hintergrund
- Farbe des Materials
- Dicke der Linie
- Schatten

Deshalb gibt es Werte, die man testen und anpassen muss.

---

## Kameraindex

```python
cv2.VideoCapture(0)
```

Bedeutung:

```text
0 = erste Kamera
1 = zweite Kamera
2 = dritte Kamera
```

Wenn die falsche Kamera geöffnet wird, kann man den Wert ändern.

---

## ROI-Wert

```python
roi_start = int(height * 0.6)
```

ROI bedeutet:

```text
Region of Interest
```

Also der Bildbereich, der wirklich ausgewertet wird.

```text
0.6 bedeutet:
Die oberen 60 Prozent werden ignoriert.
Die unteren 40 Prozent werden benutzt.
```

Warum?

Bei einem Roboter ist für die Linienverfolgung meist der Boden direkt vor dem Roboter wichtig.

### Wert kleiner machen

```text
0.4
```

Mehr Bild wird benutzt.

Vorteil:

```text
Linie wird früher gesehen.
```

Nachteil:

```text
Mehr Störungen im Bild.
```

### Wert größer machen

```text
0.8
```

Nur der sehr untere Bereich wird benutzt.

Vorteil:

```text
Weniger Störungen.
```

Nachteil:

```text
Linie wird sehr spät erkannt.
```

---

## Threshold für Linien

```python
_, mask_line = cv2.threshold(blur, 80, 255, cv2.THRESH_BINARY_INV)
```

Der Wert `80` entscheidet, welche Bildbereiche als dunkel gelten.

### Kleiner Wert

```text
50
```

Nur sehr dunkle Bereiche werden erkannt.

### Größerer Wert

```text
120
```

Auch mittel-dunkle Bereiche werden erkannt.

### Problem

Zu klein:

```text
Linie wird eventuell nicht erkannt.
```

Zu groß:

```text
Schatten oder dunkle Gegenstände werden als Linie erkannt.
```

---

## Maximalwert 255

```python
cv2.threshold(blur, 80, 255, ...)
```

`255` bedeutet weiß im Graustufenbild.

Graustufen gehen von:

```text
0   = schwarz
255 = weiß
```

Die Maske besteht danach nur noch aus:

```text
0   = ignoriert
255 = erkannt
```

---

## THRESH_BINARY_INV

```python
cv2.THRESH_BINARY_INV
```

INV bedeutet invertiert.

Normal wäre:

```text
hell -> weiß
dunkel -> schwarz
```

Invertiert bedeutet:

```text
dunkel -> weiß
hell -> schwarz
```

Warum?

Die schwarze Linie soll in der Maske weiß erscheinen, damit OpenCV sie leichter als Objekt finden kann.

---

## GaussianBlur

```python
blur = cv2.GaussianBlur(gray, (5, 5), 0)
```

Der Wert `(5, 5)` ist die Größe des Filters.

### Kleinere Werte

```text
(3, 3)
```

Weniger Glättung, mehr Details.

### Größere Werte

```text
(7, 7)
(9, 9)
```

Mehr Glättung, weniger Störungen.

### Wichtig

Die Werte müssen ungerade sein:

```text
3, 5, 7, 9
```

---

## Kernel für Erosion und Dilatation

```python
kernel = np.ones((5, 5), np.uint8)
```

Der Kernel ist ein kleines Raster, mit dem die Maske bearbeitet wird.

### Erosion

```python
mask_line = cv2.erode(mask_line, kernel, iterations=1)
```

Erosion entfernt kleine weiße Punkte.

### Dilatation

```python
mask_line = cv2.dilate(mask_line, kernel, iterations=2)
```

Dilatation vergrößert weiße Bereiche wieder.

Warum?

```text
erst Störungen entfernen
dann Linie wieder stabil machen
```

### Kernel kleiner

```text
(3, 3)
```

Weniger aggressive Bereinigung.

### Kernel größer

```text
(7, 7)
```

Stärkere Bereinigung, aber kleine Linien können verschwinden.

---

## Mindestfläche für Linien

```python
if area > 800:
```

Dieser Wert legt fest, wie groß eine erkannte Fläche mindestens sein muss.

### Kleiner Wert

```text
300
```

Auch kleine Objekte werden erkannt.

Nachteil:

```text
Mehr Fehlalarme.
```

### Größerer Wert

```text
1500
```

Nur große Linien werden erkannt.

Nachteil:

```text
Dünne oder entfernte Linien werden ignoriert.
```

---

## HSV-Werte für Rot

```python
lower_red1 = np.array([0, 120, 70])
upper_red1 = np.array([10, 255, 255])

lower_red2 = np.array([170, 120, 70])
upper_red2 = np.array([180, 255, 255])
```

HSV besteht aus:

```text
H = Hue/Farbton
S = Saturation/Sättigung
V = Value/Helligkeit
```

Rot braucht zwei Bereiche, weil Rot am Anfang und Ende des HSV-Farbkreises liegt.

---

## HSV-Werte für Gruen

```python
lower_green = np.array([40, 70, 70])
upper_green = np.array([80, 255, 255])
```

Dieser Bereich erkennt viele grüne Objekte.

Wenn Grün nicht erkannt wird:

```text
Bereich vergrößern
Beleuchtung verbessern
anderen Grünton testen
```

---

## Pixel-Schwelle für Farben

```python
if red_pixels > 2000:
```

Dieser Wert entscheidet, ab wann eine Farbe als erkannt gilt.

### Kleiner Wert

```text
500
```

Farbe wird schnell erkannt, aber auch kleine Störungen zählen.

### Größerer Wert

```text
5000
```

Farbe muss deutlich sichtbar sein.

---

## Bildbereiche für Links, Mitte, Rechts

```python
if cx < width // 3:
    direction = "Links lenken"
elif cx > 2 * width // 3:
    direction = "Rechts lenken"
else:
    direction = "Geradeaus"
```

Das Bild wird in drei Bereiche geteilt:

```text
0 Prozent bis 33 Prozent     -> links
33 Prozent bis 66 Prozent    -> mitte
66 Prozent bis 100 Prozent   -> rechts
```

Warum?

Das ist einfach, verständlich und reicht für eine erste Roboterlogik.

---

## Warum Werte nicht perfekt sind

Die Werte sind Startwerte.

Sie funktionieren ungefähr, aber nicht überall gleich.

Andere Umgebung bedeutet:

```text
andere Kamera
anderes Licht
anderer Boden
andere Linie
andere Entfernung
```

Dann müssen Werte angepasst werden.

---

## Wie man sinnvoll testet

Nicht alle Werte gleichzeitig ändern.

Besser:

```text
1. Nur Threshold ändern
2. Ergebnis prüfen
3. Dann Kernel ändern
4. Ergebnis prüfen
5. Dann Mindestfläche ändern
```

So versteht man, welcher Wert welchen Effekt hat.

---

## Gute Testmethode

Für jede Änderung notieren:

```text
Datum
Wert vorher
Wert nachher
Ergebnis
Bemerkung
```

Beispiel:

```text
Threshold 80 -> 100
Ergebnis: Linie wird besser erkannt, aber Schatten stören mehr.
```

---

## Zusammenfassung

Die wichtigsten Werte sind:

```text
Kameraindex          -> welche Kamera benutzt wird
ROI-Wert             -> welcher Bildbereich ausgewertet wird
Threshold            -> was als dunkel gilt
Kernel               -> wie stark bereinigt wird
Mindestfläche        -> was als echtes Objekt gilt
HSV-Grenzen          -> welche Farben erkannt werden
Pixel-Schwelle       -> ab wann Farbe zählt
Bilddrittel          -> links, mitte oder rechts
```

Diese Werte machen das System anpassbar.

---

## Parameter für Zahlenerkennung

### Confidence

```python
DIGIT_MIN_CONFIDENCE

Bedeutung: wie sicher muss das Modell sein

Kleiner Wert:
-mehr Ergebnisse
-aber mehr Fehler

Größerer Wert:
-weniger Fehler
-aber öfter "unsicher"

###Bildgröße 
28x28 Pixel

Warum?
-entspricht MNIST
-Modell erwartet genau dieses Format

###Trainingsdaten
Wichtigster Faktor:
mehr Daten = besseres Modell

Empfehlung:
20-50 Bilder pro Zahl
besser 100+

Dual-Modus
Custom - wenn sicher
sonst - MNIST

Dieser Modus ist am stabilsten

---

