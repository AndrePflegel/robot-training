# Mehrfarb-Erkennung

Dieses Modul erkennt mehrere Farben gleichzeitig und erzeugt Zustände.

---

## Ziel

Aus Farben werden Zustände:

```text
Rot   -> STOP
Gruen -> GO
Keine Farbe -> WAIT
```

---

## Warum mehrere Farben?

Ein Roboter kann so Signale erkennen:

- Rot = Stoppen
- Gruen = Fahren

Das entspricht einfachen Ampel- oder Steuerlogiken.

---

## HSV-Farbraum

Das Bild wird zuerst umgewandelt:

```python
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
```

Warum HSV?

- stabiler bei Licht
- besser für Farberkennung

---

## Rot erkennen

Rot liegt an zwei Stellen im Farbraum.

Deshalb:

```python
mask_red = Bereich1 + Bereich2
```

---

## Gruen erkennen

```python
mask_green = cv2.inRange(...)
```

Ein einzelner Bereich reicht.

---

## Pixel zählen

```python
cv2.countNonZero(mask)
```

Warum?

- einzelne Pixel sind oft Fehler
- wir brauchen eine Mindestmenge

---

## Entscheidung

```python
if red_pixels > 2000:
    state = "STOP"
```

Warum 2000?

- experimentell gewählt
- verhindert Fehlentscheidungen

---

## Typische Probleme

### Farbe wird nicht erkannt

- falsche HSV-Werte
- schlechtes Licht
- Objekt zu klein

### falsche Erkennung

- zu niedrige Pixel-Schwelle
- Hintergrund hat ähnliche Farben

---

## Zusammenfassung

Das Modul macht:

```text
Bild -> Farbe filtern -> Pixel zählen -> Zustand bestimmen
```

Das ist eine einfache Form einer Zustandsmaschine.
