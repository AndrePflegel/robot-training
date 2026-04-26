# Projektstruktur und main.py

Dieses Dokument erklärt den Aufbau des Projekts.

---

## Ziel der Struktur

Vermeiden von:

- mehrfach geschriebenem Code
- unübersichtlichen Dateien
- schwer wartbarem Projekt

Stattdessen:

- klare Trennung
- wiederverwendbare Module
- zentrale Steuerung

---

## Projektaufbau

```text
robot-training/
├── main.py
├── camera.py
├── modules/
├── docs/
└── old/
```

---

## main.py

Die Datei `main.py` ist der Einstiegspunkt.

Sie:

- zeigt ein Menü
- nimmt Eingaben entgegen
- startet Module

---

## Beispiel

```python
from modules.color_detection import run_color_detection
```

Bedeutung:

- importiert Funktion aus anderem Modul

---

## Menü

```python
choice = input("Auswahl: ")
```

Der Benutzer entscheidet, was ausgeführt wird.

---

## Module

Jedes Modul hat eine Funktion:

```python
def run_color_detection():
```

Warum?

- klare Struktur
- einfach aufzurufen
- leicht erweiterbar

---

## camera.py

Diese Datei kümmert sich nur um:

- Kamera öffnen
- Kamera schließen

Warum?

- kein doppelter Code
- zentrale Kontrolle

---

## modules/

Hier liegt die eigentliche Logik:

- Farberkennung
- Linienerkennung
- Robot-Logik

---

## old/

Alte Dateien bleiben erhalten:

- zum Vergleich
- zum Lernen
- zur Sicherheit

---

## Vorteile der Struktur

```text
- weniger Code-Duplikate
- bessere Übersicht
- einfache Erweiterung
- klarer Einstiegspunkt
```

---

## Erweiterung

Neue Funktion:

1. neue Datei in modules/
2. Funktion schreiben
3. in main.py importieren
4. Menü erweitern

---

## Zusammenfassung

Das Projekt besteht aus:

```text
main.py steuert alles
camera.py liefert Bilder
modules enthalten Logik
docs erklären den Code
```

---

##Neue Komponenten

Das Projekt enthält jetzt zusätzlich:

-ML-Modelle (models/)
-Trainingsdaten (data/)
-Tests (tests/)
-Konfiguration (config/settings.py)

Diese Struktur erlaubt:

-Erweiterung
-Training
-Testbarkeit
