# SQLiteVSLiteDB

## Benchmark: SQLite vs. LiteDB

Dieses Projekt dient dazu, die Leistungsfähigkeit von **SQLite** und **LiteDB** unter möglichst vergleichbaren Bedingungen zu messen.

Dabei werden verschiedene Datenbankoperationen ausgeführt und miteinander verglichen.

Unter anderem werden folgende Leistungswerte erfasst:

* **Transactions per Second (TPS)** – Wie viele Transaktionen pro Sekunde verarbeitet werden können.
* **Query Rate** – Wie viele Datenbankabfragen pro Sekunde verarbeitet werden können.
* **Fehlerquote** – Wie viele Abfragen bzw. Operationen erfolgreich oder fehlerhaft waren.
* **Latenz** – Wie lange eine einzelne Datenbankoperation benötigt.
* **Ausführungszeit** – Wie lange ein kompletter Testlauf benötigt.

Zusätzlich werden grundlegende Informationen über den verwendeten Computer gespeichert, damit die Ergebnisse später nachvollziehbar sind.

Dazu gehören beispielsweise:

* Prozessor
* Anzahl der CPU-Kerne
* Anzahl der Threads
* CPU-Takt
* Arbeitsspeichergröße
* Arbeitsspeichertakt

> **Wichtig:** Die Hardwareinformationen dienen dazu, Benchmark-Ergebnisse nachvollziehbar zu machen. Der wichtigste Vergleich findet zwischen SQLite und LiteDB **auf demselben Computer unter denselben Bedingungen** statt.

---

# 1. Voraussetzungen

Bevor das Projekt gestartet werden kann, müssen einige Programme auf dem Computer vorhanden sein.

## 1.1 Python

Auf dem Computer muss **Python 3.10 oder neuer** installiert sein.

Um zu überprüfen, ob Python bereits installiert ist, öffnet man unter Windows die **Eingabeaufforderung (CMD)**.

### CMD öffnen

Drückt:

```text
Windows-Taste + R
```

Gebt anschließend ein:

```text
cmd
```

und bestätigt mit Enter.

Nun kann mit folgendem Befehl überprüft werden, ob Python vorhanden ist:

```bash
python --version
```

Beispiel:

```text
Python 3.12.4
```

Wenn eine Version ab **3.10** angezeigt wird, ist Python grundsätzlich geeignet.

Sollte stattdessen eine Meldung erscheinen, dass `python` nicht gefunden wurde, muss Python zunächst installiert werden.

---

# 2. .NET SDK

Für den LiteDB-Benchmark wird die echte **LiteDB-.NET-Bibliothek** verwendet.

Daher benötigt der Computer das **.NET SDK**.

> Das .NET SDK ist nicht dasselbe wie nur die .NET Runtime.

Für das Setup wird das SDK benötigt, weil darüber die benötigte LiteDB-Version aus NuGet heruntergeladen wird.

Nach der Installation kann mit folgendem Befehl geprüft werden, ob das .NET SDK vorhanden ist:

```bash
dotnet --version
```

Beispiel:

```text
8.0.414
```

Wenn eine Versionsnummer angezeigt wird, ist das .NET SDK verfügbar.

---

# 3. NuGet

Für LiteDB wird **NuGet** verwendet.

NuGet ist das Paketverwaltungssystem für .NET-Anwendungen.

### Wichtig

Eine separate Installation von `nuget.exe` ist für dieses Projekt **nicht erforderlich**.

Das benötigte NuGet-System wird über das installierte **.NET SDK** bereitgestellt.

Das Setup-Skript verwendet dafür die `dotnet`-Befehle.

Der Benutzer muss daher normalerweise lediglich sicherstellen, dass:

```bash
dotnet --version
```

funktioniert.

---

# 4. Projekt herunterladen

Ladet das Projekt vollständig herunter bzw. klont das Repository.

Nach dem Herunterladen sollte das Projektverzeichnis ungefähr so aussehen:

```text
SQLiteVSLiteDB/
│
├── setup.py
├── benchmark.py
├── requirements.txt
│
├── database/
│
├── services/
│
├── tests/
│
└── resources/
```

Die genaue Anzahl der Dateien und Unterordner kann sich im Laufe der Projektentwicklung ändern.

Wichtig ist, dass **`setup.py` im Hauptverzeichnis des Projekts** vorhanden ist.

---

# 5. Eingabeaufforderung im Projektverzeichnis öffnen

Die Befehle müssen im Hauptverzeichnis des Projekts ausgeführt werden.

Beispiel:

```text
C:\Users\Max\Desktop\SQLiteVSLiteDB
```

### Einfache Möglichkeit

Öffnet den Projektordner im Windows Explorer.

Klickt oben in die Adressleiste und gebt ein:

```text
cmd
```

Drückt anschließend Enter.

Es öffnet sich eine Eingabeaufforderung, die sich bereits im richtigen Projektverzeichnis befindet.

---

# 6. Projekt einrichten

## Wichtig: Nicht mehr jede Abhängigkeit manuell installieren

Das Projekt besitzt ein Setup-Skript.

Dadurch werden die benötigten Komponenten automatisch eingerichtet.

Führt im Projektverzeichnis folgenden Befehl aus:

```bash
python setup.py
```

Das Setup übernimmt unter anderem:

1. Überprüfung der Python-Version
2. Überprüfung des .NET SDK
3. Installation der benötigten Python-Abhängigkeiten
4. Erstellung der benötigten Verzeichnisse
5. Download der festgelegten LiteDB-Version über NuGet
6. Einrichtung der LiteDB-Bibliothek
7. Überprüfung, ob LiteDB aus Python heraus geladen werden kann

Während des Setups werden verschiedene Meldungen in der Eingabeaufforderung angezeigt.

Am Ende sollte eine Meldung erscheinen, dass das Setup erfolgreich abgeschlossen wurde.

---

# 7. Was wird installiert?

Das Setup benötigt insbesondere:

### Python-Abhängigkeiten

Unter anderem werden Bibliotheken wie:

```text
psutil
pythonnet
```

installiert.

### LiteDB

Die für den Benchmark verwendete LiteDB-Version wird **fest vorgegeben**.

Dadurch soll verhindert werden, dass sich Benchmark-Ergebnisse durch eine später automatisch verwendete neue LiteDB-Version verändern.

Die LiteDB-Bibliothek wird anschließend im Projekt abgelegt.

---

# 8. Datenbanken

Die beiden Datenbanken werden als Dateien im Projekt gespeichert.

Der relevante Ordner ist:

```text
resources/
└── DB/
```

Dort werden die Datenbankdateien abgelegt:

```text
resources/
└── DB/
    ├── sqlite.db
    └── litedb.db
```

### SQLite

Die SQLite-Datenbank wird in:

```text
resources/DB/sqlite.db
```

gespeichert.

### LiteDB

Die LiteDB-Datenbank wird in:

```text
resources/DB/litedb.db
```

gespeichert.

Die Dateien müssen normalerweise **nicht manuell erstellt werden**.

Das Benchmark-Programm kümmert sich darum.

---

# 9. Benchmark starten

Nachdem das Setup erfolgreich abgeschlossen wurde, kann der Benchmark gestartet werden.

Dazu im Projektverzeichnis:

```bash
python benchmark.py
```

eingeben.

Anschließend startet der Benchmark.

Je nach Konfiguration werden verschiedene Testfälle durchgeführt.

---

# 10. Testkürzel

Beim Start bzw. während der Vorbereitung des Benchmarks werdet ihr aufgefordert, einen **Testkürzel** einzugeben.

Beispiel:

```text
Bitte Testkürzel eingeben:
```

Hier muss der zuvor erhaltene Testkürzel eingegeben werden.

Der Testkürzel dient dazu, den jeweiligen Benchmark eindeutig zu identifizieren bzw. einem vorgesehenen Testlauf zuzuordnen.

Gebt den Kürzel **genau so ein, wie er bereitgestellt wurde**.

Achtet insbesondere auf:

* Groß- und Kleinschreibung
* Zahlen
* Sonderzeichen
* Leerzeichen

Falls ein falscher Testkürzel eingegeben wird, kann der Benchmark möglicherweise nicht gestartet werden.

---

# 11. Was wird getestet?

Der Benchmark vergleicht SQLite und LiteDB anhand verschiedener Datenbankoperationen.

Dabei werden unterschiedliche Mengen von Datensätzen bzw. Operationen verwendet.

Beispielsweise können Tests mit:

```text
10
100
1000
...
```

Operationen durchgeführt werden.

Die genaue Anzahl hängt von der jeweiligen Benchmark-Konfiguration ab.

---

# 12. INSERT

Bei einem INSERT-Test werden neue Datensätze in die Datenbank geschrieben.

Beispiel:

```text
INSERT 10 Datensätze
INSERT 100 Datensätze
INSERT 1000 Datensätze
```

Dabei wird gemessen, wie schnell die Datenbank die Datensätze verarbeiten kann.

---

# 13. SELECT

Bei SELECT-Tests werden Daten aus der Datenbank gelesen.

Hier wird beispielsweise untersucht, wie schnell die Datenbank bestimmte Datensätze finden und zurückgeben kann.

Dabei können unterschiedliche Abfragen verwendet werden.

---

# 14. UPDATE

Bei UPDATE-Tests werden bereits vorhandene Datensätze verändert.

Gemessen wird beispielsweise:

* wie schnell die Änderungen durchgeführt werden
* wie viele Änderungen erfolgreich waren
* wie viele Änderungen fehlgeschlagen sind

---

# 15. DELETE

Bei DELETE-Tests werden Datensätze aus der Datenbank entfernt.

Auch hier werden Ausführungszeit und Anzahl erfolgreicher bzw. fehlerhafter Operationen erfasst.

---

# 16. Transaktionen

Ein besonders wichtiger Bestandteil des Benchmarks sind **Transaktionen**.

Eine Transaktion fasst mehrere Datenbankoperationen zu einer logischen Einheit zusammen.

Beispielsweise:

```text
BEGIN TRANSACTION

INSERT
INSERT
UPDATE
SELECT
DELETE

COMMIT
```

Eine Transaktion kann entweder vollständig erfolgreich abgeschlossen werden oder – abhängig vom verwendeten Verhalten – zurückgerollt werden.

Dadurch kann die Performance der Datenbanken bei zusammengehörigen Datenbankoperationen verglichen werden.

---

# 17. Transactions per Second (TPS)

**TPS** steht für:

```text
Transactions Per Second
```

also:

```text
Transaktionen pro Sekunde
```

Der Wert beschreibt, wie viele Transaktionen eine Datenbank innerhalb einer Sekunde verarbeiten kann.

Ein höherer Wert bedeutet grundsätzlich, dass mehr Transaktionen pro Sekunde verarbeitet werden können.

Beispiel:

```text
SQLite:  1250 TPS
LiteDB:  980 TPS
```

In diesem Beispiel verarbeitet SQLite mehr Transaktionen pro Sekunde.

---

# 18. Query Rate

Die **Query Rate** beschreibt, wie viele Datenbankabfragen innerhalb einer bestimmten Zeit verarbeitet werden.

Beispielsweise:

```text
SQLite:  5000 Queries/s
LiteDB:  4200 Queries/s
```

Dabei ist wichtig, nicht nur die Anzahl der gestarteten Abfragen zu betrachten.

Der Benchmark berücksichtigt auch, ob eine Abfrage erfolgreich war oder einen Fehler verursacht hat.

---

# 19. Fehler

Neben der Geschwindigkeit ist auch die Anzahl der Fehler relevant.

Beispielsweise können folgende Werte erfasst werden:

```text
Queries:
    1000

Erfolgreich:
    998

Fehler:
    2
```

Dadurch kann verhindert werden, dass eine Datenbank ausschließlich aufgrund einer hohen Geschwindigkeit besser bewertet wird, obwohl dabei mehr Operationen fehlschlagen.

---

# 20. Latenz

Die **Latenz** beschreibt, wie lange eine Datenbankoperation benötigt.

Beispiel:

```text
SELECT:
    0.52 ms
```

Eine geringere Latenz bedeutet, dass eine einzelne Anfrage schneller beantwortet wurde.

Bei der späteren Auswertung können beispielsweise folgende Werte interessant sein:

* durchschnittliche Latenz
* minimale Latenz
* maximale Latenz

---

# 21. Benchmark-Ergebnisse

Die Ergebnisse werden als **JSON-Datei** gespeichert.

Dadurch können die Ergebnisse später automatisiert ausgewertet werden.

Die Datei enthält sowohl die Hardwareinformationen als auch die Ergebnisse der einzelnen Testläufe.

Eine vereinfachte Struktur sieht beispielsweise so aus:

```json
{
    "hardware": {
        "system": {},
        "cpu": {},
        "ram": {}
    },
    "results": [
        {
            "iteration": 1,
            "exec_time": {},
            "results": {}
        }
    ]
}
```

---

# 22. Dateiname des Reports

Der Ergebnisreport wird nach folgendem Schema benannt:

```text
result_{Datum}_{CPU}_{User}.json
```

Beispiel:

```text
result_2026-08-31_AMD_Ryzen_9_7950X_Max.json
```

Dadurch kann bereits anhand des Dateinamens erkannt werden:

* wann der Test durchgeführt wurde
* welcher Prozessor verwendet wurde
* welcher Benutzer den Test ausgeführt hat

Ungültige Zeichen für Dateinamen werden automatisch angepasst.

---

# 23. Hardwareinformationen

Zusätzlich zum eigentlichen Benchmark werden grundlegende Informationen über das Testsystem gespeichert.

Beispielsweise:

```json
{
    "cpu": {
        "processor": "AMD Ryzen 9 7950X",
        "cores": 16,
        "threads": 32
    },
    "ram": {
        "size_gb": 64,
        "frequency_mhz": 6000
    }
}
```

Diese Informationen sind wichtig, wenn Benchmark-Ergebnisse später analysiert werden.

---

# 24. Warum wird die Hardware gespeichert?

Datenbanken können auf unterschiedlichen Computern sehr unterschiedliche Ergebnisse liefern.

Beispielsweise können folgende Faktoren einen großen Einfluss auf die Geschwindigkeit haben:

* CPU
* Anzahl der CPU-Kerne
* CPU-Takt
* Arbeitsspeichergröße
* Arbeitsspeichertakt
* Betriebssystem
* Hintergrundprozesse
* Speichermedium

Deshalb werden die grundlegenden Hardwareinformationen zusammen mit dem Benchmark gespeichert.

---

# 25. Vergleich SQLite vs. LiteDB

Der wichtigste Vergleich dieses Projekts findet **innerhalb desselben Testsystems** statt.

Das bedeutet:

```text
Computer
    │
    ├── SQLite Benchmark
    │
    └── LiteDB Benchmark
```

Beide Datenbanken werden auf demselben Computer getestet.

Dadurch bleiben wichtige Hardwarefaktoren gleich.

Ein Ergebnis wie:

```text
SQLite:
    1500 TPS

LiteDB:
    1100 TPS
```

ist dadurch wesentlich aussagekräftiger, als wenn SQLite auf einem Computer und LiteDB auf einem komplett anderen Computer getestet worden wäre.

---

# 26. Wichtige Hinweise für einen fairen Benchmark

Für möglichst aussagekräftige Ergebnisse sollte während des Benchmarks möglichst wenig andere Software aktiv sein.

Vermeidet insbesondere:

* große Downloads
* Spiele
* Video-Encoding
* große Dateiübertragungen
* andere Benchmarks
* Programme mit hoher CPU-Auslastung

Auch automatische Updates oder andere Hintergrundprozesse können Ergebnisse beeinflussen.

---

# 27. Datenbankzustand

Für einen fairen Vergleich müssen SQLite und LiteDB mit einem vergleichbaren Datenbestand getestet werden.

Die Benchmark-Anwendung übernimmt die Vorbereitung der Datenbanken.

**Bitte verändert die Datenbankdateien während eines laufenden Benchmarks nicht manuell.**

Insbesondere sollten die Dateien:

```text
resources/DB/sqlite.db
resources/DB/litedb.db
```

während eines laufenden Tests nicht geöffnet, verschoben oder verändert werden.

---

# 28. Nach dem Benchmark

Nach Abschluss des Benchmarks befindet sich die Ergebnisdatei im dafür vorgesehenen Ergebnisverzeichnis.

Die JSON-Datei kann anschließend zur Auswertung weitergegeben werden.

**Die JSON-Datei sollte nicht manuell bearbeitet werden**, bevor sie ausgewertet wurde.

Dadurch bleibt nachvollziehbar, welche Werte tatsächlich vom Benchmark erzeugt wurden.

---

# 29. Fehler beim Setup

## `python` wurde nicht gefunden

Wenn folgende Meldung erscheint:

```text
'python' is not recognized ...
```

ist Python entweder nicht installiert oder nicht im PATH eingetragen.

Installiert Python 3.10 oder neuer und startet anschließend die Eingabeaufforderung erneut.

---

## `dotnet` wurde nicht gefunden

Wenn folgende Meldung erscheint:

```text
'dotnet' is not recognized ...
```

ist das .NET SDK nicht installiert oder nicht im PATH verfügbar.

Installiert das **.NET SDK** und startet anschließend die Eingabeaufforderung erneut.

Danach:

```bash
dotnet --version
```

ausführen.

---

## LiteDB konnte nicht installiert werden

Stellt sicher, dass:

1. eine Internetverbindung besteht
2. das .NET SDK installiert ist
3. `dotnet --version` funktioniert
4. das Setup erneut ausgeführt wird

```bash
python setup.py
```

---

## Python-Abhängigkeiten konnten nicht installiert werden

Stellt sicher, dass Python funktioniert:

```bash
python --version
```

und anschließend:

```bash
python -m pip --version
```

Danach kann das Setup erneut ausgeführt werden:

```bash
python setup.py
```

---

# 30. Setup erneut ausführen

Das Setup kann grundsätzlich erneut ausgeführt werden.

```bash
python setup.py
```

Das Setup überprüft die benötigten Komponenten erneut und richtet die benötigten Projektdateien ein.

---

# 31. Kurzfassung

Wenn Python und das .NET SDK bereits installiert sind, ist der gesamte Ablauf sehr einfach.

### Schritt 1 – Projektordner öffnen

Öffnet den Ordner:

```text
SQLiteVSLiteDB
```

### Schritt 2 – CMD öffnen

In der Explorer-Adressleiste:

```text
cmd
```

eingeben und Enter drücken.

### Schritt 3 – Setup starten

```bash
python setup.py
```

Warten, bis das Setup erfolgreich abgeschlossen wurde.

### Schritt 4 – Benchmark starten

```bash
python benchmark.py
```

### Schritt 5 – Testkürzel eingeben

Wenn das Programm danach fragt, den bereitgestellten Testkürzel eingeben.

### Schritt 6 – Warten

Der Benchmark führt die vorgesehenen Tests automatisch durch.

### Schritt 7 – Ergebnisdatei

Nach Abschluss befindet sich der Report als JSON-Datei im Ergebnisverzeichnis.

---

# 32. Der komplette Ablauf in einem Bild

```text
Projekt herunterladen
        │
        ▼
Python 3.10+ vorhanden?
        │
        ▼
.NET SDK vorhanden?
        │
        ▼
python setup.py
        │
        ├── Python-Abhängigkeiten
        │
        ├── .NET / NuGet prüfen
        │
        ├── LiteDB herunterladen
        │
        ├── Projektverzeichnisse erstellen
        │
        └── Installation testen
        │
        ▼
python benchmark.py
        │
        ▼
Testkürzel eingeben
        │
        ▼
SQLite Benchmark
        │
        ▼
LiteDB Benchmark
        │
        ▼
TPS / Queryrate / Fehler / Latenz
        │
        ▼
JSON-Report
```

---

# 33. Ziel des Projekts

Das Ziel dieses Projekts ist **kein allgemeiner Leistungstest von Computern**, sondern ein möglichst nachvollziehbarer Vergleich zwischen **SQLite und LiteDB**.

Die wichtigste Aussage entsteht dadurch, dass beide Datenbanken unter denselben Bedingungen getestet werden.

Die gespeicherten Hardwareinformationen ermöglichen zusätzlich eine spätere Einordnung der Ergebnisse.

**Bitte gebt bei der Weitergabe von Benchmark-Ergebnissen möglichst immer auch die zugehörige JSON-Datei bzw. die darin enthaltenen Hardwareinformationen mit weiter.**
