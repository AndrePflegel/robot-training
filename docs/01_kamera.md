# Kamera-Grundlagen mit OpenCV

Dieses Modul zeigt, wie die Kamera geöffnet und ein Bild gelesen wird.

Es ist die Basis für alle weiteren Module.

---

## Grundprinzip

Die Kamera liefert kontinuierlich Bilder.

Das Programm:

1. öffnet die Kamera
2. liest Bild für Bild
3. zeigt das Bild an
4. beendet sich bei Tastendruck

---

## Kamera öffnen

```python
cap = cv2.VideoCapture(0)
```

Bedeutung:

- 0 = erste Kamera im System
- bei mehreren Kameras:
  - 1 = zweite Kamera
  - 2 = dritte Kamera

---

## Prüfen ob Kamera funktioniert

```python
if not cap.isOpened():
    print("Kamera konnte nicht geöffnet werden.")
```

Warum wichtig?

- verhindert Abstürze
- zeigt Fehler früh an

---

## Bild lesen

```python
ret, frame = cap.read()
```

Bedeutung:

- ret = True oder False
- frame = aktuelles Bild

Wenn `ret` False ist:

```text
kein Bild verfügbar
```

---

## Bild anzeigen

```python
cv2.imshow("Kamera", frame)
```

- öffnet ein Fenster
- zeigt das aktuelle Bild

---

## Tasteneingabe

```python
if cv2.waitKey(1) == 27:
    break
```

- 27 = ESC-Taste
- beendet die Schleife

---

## Kamera schließen

```python
cap.release()
cv2.destroyAllWindows()
```

Warum wichtig?

- gibt Kamera frei
- verhindert Probleme bei erneutem Start

---

## Zusammenfassung

Das Modul macht:

```text
Kamera öffnen -> Bild lesen -> anzeigen -> wiederholen -> beenden
```

Alle anderen Module bauen darauf auf.
