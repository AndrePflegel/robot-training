# Farberkennung mit OpenCV

Dieses Modul erkennt mehrere Farben (z.B Rot und Grün) im Kamerabild.

## Grundprinzip

Das System arbeitet in mehreren Schritten:

1. Kamera liefert Bild
2. Bild wird in HSV-Farbraum umgewandelt
3. Farbfilter wird angewendet
4. Bereiche werden erkannt
5. größtes Objekt wird ausgewählt
6. Position wird bestimmt

---

## Warum HSV statt RGB?

RGB beschreibt Farben über Rot, Grün, Blau.

Problem:
- Licht verändert RGB stark
- gleiche Farbe kann unterschiedliche Werte haben

HSV trennt:

- H (Hue) = Farbe
- S (Saturation) = Sättigung
- V (Value) = Helligkeit

Dadurch ist Farberkennung stabiler.

---

## Erklärung wichtiger Code-Teile

### Kamera öffnen

```python
cap = cv2.VideoCapture(0)
```

0 bedeutet: erste Kamera im System

---

### Bild holen

```python
ret, frame = cap.read()
```

ret:
- True = Bild erfolgreich
- False = Fehler

frame:
- aktuelles Kamerabild

---

### Umwandlung in HSV

```python
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
```

OpenCV arbeitet intern mit BGR, nicht RGB.

---

### Farbfilter definieren

```python
lower_red = np.array([0, 120, 70])
upper_red = np.array([10, 255, 255])
```

Das sind Grenzwerte für:

- Farbton
- Sättigung
- Helligkeit

Diese Werte sind experimentell gewählt.

---

### Warum zwei Rot-Bereiche?

Rot liegt im HSV-Kreis an zwei Stellen:

```text
0° und 180°
```

Deshalb braucht man zwei Bereiche.

---

### Maske erstellen

```python
mask = cv2.inRange(hsv, lower_red, upper_red)
```

Ergebnis:

- weiß = erkannt
- schwarz = ignoriert

---

### Konturen finden

```python
contours, _ = cv2.findContours(...)
```

Hier sucht OpenCV zusammenhängende Bereiche.

---

### Größtes Objekt wählen

```python
biggest = max(contours, key=cv2.contourArea)
```

Warum?

- kleine Punkte sind oft Rauschen
- wir wollen das Hauptobjekt

---

### Position bestimmen

```python
cx = x + w // 2
```

Das ist der Mittelpunkt des Objekts.

---

### Entscheidung treffen

```python
if cx < width // 3:
    print("Links")
```

Das Bild wird in drei Bereiche geteilt:

- links
- mitte
- rechts

---

## Warum nur der größte Bereich?

Ohne Filter:

- viele kleine Objekte
- unruhiges Verhalten

Mit Filter:

- stabil
- roboterfreundlich

---

## Was passiert wenn man Werte ändert?

### Farbgrenzen

- zu eng → Objekt wird nicht erkannt
- zu weit → falsche Objekte werden erkannt

### Mindestfläche

```python
if area > 1000
```

- kleiner Wert → viele Störungen
- großer Wert → kleine Objekte verschwinden

---

## Zusammenfassung

Das System macht:

Kamera → Farbe filtern → Objekt finden → Position bestimmen → Entscheidung treffen

Das ist die Grundlage für:

- Linienverfolgung
- Objekterkennung
- Robotik
