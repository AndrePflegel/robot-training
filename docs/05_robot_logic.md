# Robot-Logik: Linie und Farbe kombinieren

Dieses Modul kombiniert zwei Erkennungen:

- Linienerkennung
- Farberkennung

Ziel ist es, ein einfaches Verhalten zu simulieren, wie es später bei einem Roboter genutzt werden kann.

---

## Grundidee

Die Linie gibt die Richtung vor.

Die Farbe gibt den Zustand vor.

```text
Schwarze Linie links  -> links lenken
Schwarze Linie mitte  -> geradeaus fahren
Schwarze Linie rechts -> rechts lenken

Rot   -> STOP
Gruen -> GO
Keine Farbe -> WAIT
```

---

## Warum wird kombiniert?

Ein Roboter muss nicht nur etwas erkennen, sondern daraus eine Entscheidung ableiten.

Beispiel:

```text
Linie sagt: Geradeaus
Farbe sagt: STOP

Ergebnis: STOP
```

Die Farbe hat Vorrang, weil ein Stop-Signal wichtiger ist als die normale Fahrtrichtung.

---

## Ablauf im Modul

Das Modul arbeitet in dieser Reihenfolge:

1. Kamerabild lesen
2. Rot erkennen
3. Gruen erkennen
4. Linie im unteren Bildbereich erkennen
5. Richtung der Linie bestimmen
6. Aktion ableiten
7. Ergebnis anzeigen

---

## Farberkennung

Das Bild wird zuerst in HSV umgewandelt:

```python
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
```

HSV ist für Farberkennung besser geeignet als RGB/BGR, weil Farbe, Sättigung und Helligkeit getrennt betrachtet werden.

---

## Rot erkennen

Rot liegt im HSV-Farbraum an zwei Stellen. Deshalb gibt es zwei Bereiche:

```python
lower_red1 = np.array([0, 120, 70])
upper_red1 = np.array([10, 255, 255])

lower_red2 = np.array([170, 120, 70])
upper_red2 = np.array([180, 255, 255])
```

Beide Masken werden kombiniert:

```python
mask_red = cv2.inRange(hsv, lower_red1, upper_red1) + cv2.inRange(hsv, lower_red2, upper_red2)
```

---

## Gruen erkennen

Gruen liegt ungefähr in diesem HSV-Bereich:

```python
lower_green = np.array([40, 70, 70])
upper_green = np.array([80, 255, 255])
```

Die Maske entsteht so:

```python
mask_green = cv2.inRange(hsv, lower_green, upper_green)
```

---

## Pixel zählen

```python
red_pixels = cv2.countNonZero(mask_red)
green_pixels = cv2.countNonZero(mask_green)
```

Damit wird gezählt, wie viele Pixel in der jeweiligen Farbe erkannt wurden.

Warum?

- einzelne kleine Farbpunkte sollen nicht sofort eine Aktion auslösen
- erst ab einer bestimmten Menge wird die Farbe ernst genommen

---

## Linienerkennung

Für die Linie wird nur der untere Teil des Bildes betrachtet:

```python
roi_start = int(height * 0.6)
roi = frame[roi_start:height, 0:width]
```

Warum?

- die Linie befindet sich vor dem Roboter auf dem Boden
- der obere Bildbereich enthält oft unnötige Störungen
- der Code wird schneller und stabiler

---

## Graustufen und Glättung

```python
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
```

Warum?

- Linienerkennung braucht keine Farbe
- Graustufen reichen aus
- Blur reduziert Bildrauschen

---

## Schwarze Linie isolieren

```python
_, mask_line = cv2.threshold(blur, 80, 255, cv2.THRESH_BINARY_INV)
```

Bedeutung:

- dunkle Bereiche werden weiß
- helle Bereiche werden schwarz

Dadurch wird die schwarze Linie als weißer Bereich in der Maske sichtbar.

---

## Störungen entfernen

```python
kernel = np.ones((5, 5), np.uint8)
mask_line = cv2.erode(mask_line, kernel, iterations=1)
mask_line = cv2.dilate(mask_line, kernel, iterations=2)
```

Warum?

- kleine Störungen werden entfernt
- Lücken in der Linie werden geschlossen
- das Ergebnis wird ruhiger

---

## Konturen finden

```python
contours, _ = cv2.findContours(
    mask_line,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)
```

OpenCV sucht zusammenhängende weiße Bereiche.

Diese Bereiche können mögliche Linien sein.

---

## Größte Kontur auswählen

```python
biggest = max(contours, key=cv2.contourArea)
area = cv2.contourArea(biggest)
```

Warum?

- die größte dunkle Fläche ist meistens die Linie
- kleine Flecken werden ignoriert

---

## Mindestfläche

```python
if area > 800:
```

Dieser Wert verhindert, dass kleine Störungen als Linie erkannt werden.

Wenn der Wert zu klein ist:

```text
Viele falsche Erkennungen
```

Wenn der Wert zu groß ist:

```text
Linie wird eventuell nicht erkannt
```

---

## Mittelpunkt der Linie

```python
cx = x + w // 2
cy = y + h // 2
```

Der Mittelpunkt sagt, wo die Linie im Bild liegt.

Diese Information wird für die Lenkentscheidung verwendet.

---

## Richtungsentscheidung

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
Links | Mitte | Rechts
```

Dadurch entsteht eine einfache Fahrentscheidung.

---

## Farbentscheidung hat Vorrang

Der wichtigste Teil ist die Zusammenführung:

```python
if red_pixels > 2000:
    action = "STOP"
elif green_pixels > 2000:
    action = "GO: " + direction
else:
    action = "WAIT: " + direction
```

Bedeutung:

```text
Rot erkannt   -> Stoppen
Gruen erkannt -> Linie folgen
Keine Farbe   -> Warten, aber Richtung anzeigen
```

Warum hat Rot Vorrang?

Ein Stop-Signal ist sicherheitsrelevant. Deshalb wird es vor der Linienrichtung ausgewertet.

---

## Warum GO und WAIT trotzdem die Richtung anzeigen

Auch wenn noch kein Startsignal vorhanden ist, kann das System die Linie weiter erkennen.

Das ist nützlich, weil man sieht:

- ob die Kamera die Linie korrekt erkennt
- welche Richtung später gefahren würde
- ob die Linienlogik stabil funktioniert

---

## Visualisierung

Das Modul zeigt mehrere Fenster:

```text
Robot Logic
Line Mask
Red Mask
Green Mask
```

Diese Fenster helfen beim Verstehen und Debuggen.

---

## Typische Probleme

### Rot oder Gruen wird nicht erkannt

Mögliche Gründe:

- Farbe liegt außerhalb der HSV-Grenzen
- Beleuchtung ist schlecht
- Objekt ist zu klein
- Kamera sieht zu wenig Farbe

### Linie wird nicht erkannt

Mögliche Gründe:

- Linie ist zu dünn
- Threshold-Wert passt nicht
- Kamera sieht den Bodenbereich nicht gut
- Hintergrund ist zu dunkel

### Falsche Aktion

Mögliche Gründe:

- Farbschwelle `2000` ist zu niedrig
- Linie wird gleichzeitig falsch erkannt
- mehrere Objekte im Bild stören die Auswertung

---

## Wichtige Werte im Code

### Farbschwelle

```python
red_pixels > 2000
green_pixels > 2000
```

Kleiner Wert:

```text
Farbe wird schneller erkannt, aber auch mehr Fehler
```

Größerer Wert:

```text
Farbe wird stabiler erkannt, aber kleine Objekte zählen nicht
```

### Linien-Threshold

```python
cv2.threshold(blur, 80, 255, cv2.THRESH_BINARY_INV)
```

Kleiner Wert:

```text
Nur sehr dunkle Bereiche werden erkannt
```

Größerer Wert:

```text
Mehr dunkle Bereiche werden erkannt
```

### ROI

```python
int(height * 0.6)
```

Kleiner Wert:

```text
Mehr Bildbereich wird genutzt
```

Größerer Wert:

```text
Nur der sehr nahe untere Bereich wird genutzt
```

---

## Warum das noch keine echte Motorsteuerung ist

Das Modul entscheidet nur als Text:

```text
STOP
GO
WAIT
Links lenken
Rechts lenken
Geradeaus
```

Ein echter Roboter müsste diese Entscheidung später an Motorfunktionen weitergeben:

```python
motor.stop()
motor.forward()
motor.left()
motor.right()
```

Aktuell wird das Verhalten nur simuliert und angezeigt.

---

## Zusammenfassung

Dieses Modul verbindet Wahrnehmung und Entscheidung.

Es macht:

```text
Kamera -> Farbe erkennen -> Linie erkennen -> Zustand bestimmen -> Aktion anzeigen
```

Damit entsteht ein erstes einfaches Roboterverhalten.

Das ist eine wichtige Grundlage für:

- Linienfolger
- Ampel- oder Farbsignale
- Zustandsmaschinen
- spätere Motorsteuerung
