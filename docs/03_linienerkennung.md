# Linienerkennung mit OpenCV

Dieses Modul erkennt eine schwarze Linie im Kamerabild und bestimmt deren Position.

Ziel ist es, später einen Roboter entlang dieser Linie steuern zu können.

---

## Grundprinzip

Das System arbeitet in mehreren Schritten:

1. Kamera liefert ein Bild
2. Nur der untere Bereich wird betrachtet (ROI)
3. Bild wird in Graustufen umgewandelt
4. Bild wird geglättet (Rauschen reduzieren)
5. Schwarze Bereiche werden herausgefiltert
6. Störungen werden entfernt
7. Konturen werden erkannt
8. Größte Linie wird ausgewählt
9. Position wird bestimmt
10. Richtung wird berechnet

---

## Warum nur der untere Bereich?

```python
roi = frame[int(height * 0.6):height, 0:width]
```

Das bedeutet:
- wir ignorieren den oberen Teil des Bildes
- wir betrachten nur die unteren 40 Prozent

Warum?

- die Linie liegt meist vor dem Roboter auf dem Boden
- der obere Bildbereich enthält oft Störungen (Wände, Möbel)
- weniger Daten = schneller und stabiler

---

## Graustufen

```python
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
```

Warum?

- Farbe ist für Linien nicht wichtig
- Schwarz = niedriger Wert
- Weiß = hoher Wert
- einfacher zu verarbeiten

---

## Glättung (Blur)

```python
blur = cv2.GaussianBlur(gray, (5, 5), 0)
```

Warum?

- entfernt kleine Bildstörungen
- reduziert Kamerarauschen
- verhindert flackernde Ergebnisse

Was passiert?

- Pixel werden gemittelt
- kleine Details verschwinden

---

## Schwellenwert (Threshold)

```python
_, mask = cv2.threshold(blur, 80, 255, cv2.THRESH_BINARY_INV)
```

Erklärung:

- Werte unter 80 → weiß (Linie)
- Werte über 80 → schwarz (Hintergrund)
- `INV` bedeutet: umgekehrt

Warum?

- schwarze Linie soll sichtbar werden
- Hintergrund wird ausgeblendet

---

## Störungen entfernen (Morphologie)

```python
kernel = np.ones((5, 5), np.uint8)
mask = cv2.erode(mask, kernel, iterations=1)
mask = cv2.dilate(mask, kernel, iterations=2)
```

### Erosion

- entfernt kleine weiße Punkte
- macht Objekte kleiner

### Dilatation

- macht Objekte wieder größer
- schließt Lücken

Warum beides?

- erst säubern
- dann stabilisieren

---

## Konturen finden

```python
contours, _ = cv2.findContours(mask, ...)
```

Was passiert?

- OpenCV sucht zusammenhängende weiße Bereiche
- jeder Bereich = mögliche Linie

---

## Größte Linie auswählen

```python
biggest = max(contours, key=cv2.contourArea)
```

Warum?

- kleine Punkte sind oft Fehler
- größte Fläche ist meist die echte Linie

---

## Mindestfläche

```python
if area > 800:
```

Warum?

- ignoriert kleine Störungen
- sorgt für stabile Erkennung

Wenn der Wert zu klein ist:
- viele falsche Erkennungen

Wenn der Wert zu groß ist:
- Linie wird evtl. nicht erkannt

---

## Mittelpunkt berechnen

```python
cx = x + w // 2
```

Das ist die wichtigste Information:

- Mittelpunkt der Linie im Bild
- wird für die Steuerung verwendet

---

## Richtungsentscheidung

```python
if cx < width // 3:
    direction = "Links"
elif cx > 2 * width // 3:
    direction = "Rechts"
else:
    direction = "Geradeaus"
```

Das Bild wird in drei Bereiche geteilt:

```text
| Links | Mitte | Rechts |
```

Warum?

- einfacher als genaue Winkelberechnung
- reicht für einfache Robotersteuerung

---

## Warum wird die letzte Richtung gespeichert?

```python
last_direction = direction
```

Wenn die Linie kurz verschwindet:

- Roboter bleibt stabil
- keine plötzlichen Richtungswechsel

---

## Visualisierung

### Rechteck

```python
cv2.rectangle(...)
```

zeigt erkannte Linie

### Punkt

```python
cv2.circle(...)
```

zeigt Mittelpunkt

### Linien

```python
cv2.line(...)
```

zeigt Entscheidungsbereiche

---

## Typische Probleme

### Linie wird nicht erkannt

- Threshold-Wert falsch
- Lichtverhältnisse schlecht
- Linie zu dünn

### Zu viele Störungen

- Mindestfläche erhöhen
- Kernel größer machen

### Flackern

- Blur erhöhen
- ROI anpassen

---

## Was passiert wenn man Werte ändert?

### Threshold (80)

- kleiner → mehr wird erkannt
- größer → weniger wird erkannt

### Kernel (5x5)

- größer → mehr Glättung
- kleiner → mehr Details

### ROI (0.6)

- kleiner Wert → mehr Bild wird genutzt
- größer Wert → nur sehr naher Bereich

---

## Zusammenfassung

Das System macht:

Kamera → Bild → Linie isolieren → größte Linie finden → Position bestimmen → Richtung berechnen

Das ist die Grundlage für:

- Linienfolger-Roboter
- autonome Navigation
- Fahrentscheidungen
