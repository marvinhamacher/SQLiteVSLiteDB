# Optimierungsanleitung

Das Benchmarking wird im Rahmen eines **Feldexperimentes mit 30 Teilnehmenden** durchgeführt. Das bereitgestellte Benchmark-Skript definiert den eigentlichen Testablauf und ist daher **vor der Durchführung vollständig zu lesen**.

Diese Anleitung dient ausschließlich dazu, offensichtliche und vermeidbare Einflussfaktoren zu reduzieren. Es wird **keine vollständig kontrollierte Laborumgebung** angestrebt. Normale Unterschiede zwischen den Computern der Teilnehmenden bleiben bestehen und sind Bestandteil des Feldexperimentes.

## 1. Energiesparplan und Leistungsprofil

Da die Prozessorleistung einen direkten Einfluss auf die Ausführungszeit der Datenbankoperationen haben kann, soll für die Durchführung des Benchmarks das Leistungsprofil **„Höchstleistung“** ausgewählt werden.

Unter Windows kann dies über die Energie- bzw. Energiesparplaneinstellungen vorgenommen werden.

### Vorgehensweise

1. Öffne die **Windows-Einstellungen** bzw. die Systemsteuerung für die Energieoptionen.
2. Öffne die Einstellungen für **Energie & Akku** bzw. **Energieoptionen**.
3. Wähle beim Energiemodus bzw. Energiesparplan die Option **„Höchstleistung“** aus.
4. Falls „Höchstleistung“ nicht direkt angezeigt wird, kann der entsprechende Energiesparplan über die erweiterten Energieoptionen ausgewählt werden.

Bei einem Notebook sollte das Gerät zusätzlich **am Netzteil betrieben werden**, damit das System nicht aufgrund des Akkubetriebs automatisch die Prozessorleistung reduziert.

Die Einstellung soll **vor dem Start des Benchmark-Skripts** vorgenommen werden und während der Durchführung nicht verändert werden.

Es ist nicht notwendig, weitere CPU-Einstellungen manuell zu verändern oder die Prozessortaktung zu überwachen. Das Ziel dieser Maßnahme ist lediglich, einen unnötigen Einfluss von aggressiven Energiesparmechanismen auf die Messergebnisse zu vermeiden.

## 2. Benchmark-Skript vollständig lesen

Das Benchmark-Skript enthält die verbindlichen Vorgaben für die eigentliche Durchführung des Tests.

Vor dem Start:

* Skript vollständig lesen.
* Vorgegebenen Ablauf verstehen.
* Keine Änderungen am Skript vornehmen.
* Keine eigenen Testparameter hinzufügen oder entfernen.

Das Skript hat bei der Durchführung Vorrang vor allgemeinen Empfehlungen dieser Anleitung.

## 3. Unnötige Hintergrundprogramme

Ein normaler Computer verfügt über zahlreiche Hintergrundprozesse. Diese müssen **nicht vollständig deaktiviert** werden.

Programme, die während des Benchmarks unnötig Rechenleistung oder andere Ressourcen beanspruchen, sollten jedoch geschlossen werden.

Beispiele:

* Razer Chroma
* RGB-Software
* Game Launcher
* unnötige Browseranwendungen
* Cloud-Synchronisationsprogramme
* automatische Updater
* Overlay- oder Monitoring-Software

Es geht ausdrücklich **nicht darum, jeden Hintergrundprozess zu beenden**. Normale Systemprozesse dürfen weiterhin ausgeführt werden.

## 4. Normale Nutzung des Computers

Der Computer muss für das Feldexperiment nicht vollständig isoliert werden.

Während der eigentlichen Messung sollten jedoch keine bewusst gestarteten, rechenintensiven Anwendungen parallel ausgeführt werden.

Dazu gehören beispielsweise:

* Spiele
* Videorendering
* große Downloads
* umfangreiche Dateiübertragungen
* große Kompiliervorgänge
* andere Benchmarks

Normale Hintergrundaktivitäten des Betriebssystems müssen hingegen nicht verhindert werden.

## 5. Auffällige Belastungen

Sollte während des Benchmarks eine ungewöhnlich hohe Systembelastung auftreten, beispielsweise durch ein Windows-Update, einen Virenscan oder einen großen Download, sollte die Messung nach Möglichkeit zu einem späteren Zeitpunkt wiederholt werden.

Kleine und normale Schwankungen des Systems sind hingegen kein Grund, den Benchmark abzubrechen.

## 6. Keine eigenständigen Optimierungen

Die Teilnehmenden sollten keine zusätzlichen Optimierungen durchführen, die nicht in dieser Anleitung oder im Benchmark-Skript vorgesehen sind.

Insbesondere sollten nicht eigenständig:

* Datenbankeinstellungen verändert,
* Testparameter angepasst,
* Systemdienste deaktiviert,
* Testdaten verändert,
* Teile des Skripts verändert,
* zusätzliche Optimierungen vorgenommen

werden.

Dadurch soll sichergestellt werden, dass die 30 Teilnehmenden den vorgesehenen Benchmark möglichst einheitlich durchführen.

## 7. Was nicht erforderlich ist

Es ist **nicht erforderlich**, den Computer vollständig für das Benchmarking zu optimieren.

Beispielsweise müssen nicht:

* alle Hintergrundprozesse beendet werden,
* sämtliche Systemdienste deaktiviert werden,
* der Arbeitsspeicher manuell geleert werden,
* CPU-Takt oder Temperatur überwacht werden,
* das Betriebssystem neu installiert werden,
* die Internetverbindung getrennt werden.

Das Feldexperiment soll weiterhin eine realistische Nutzungssituation abbilden.

## 8. Grundprinzip

Die wichtigste Regel lautet:

> **Das Skript definiert den Benchmark – diese Anleitung sorgt für eine möglichst saubere Durchführung.**

Das Ziel besteht nicht darin, bei allen 30 Teilnehmenden eine identische Laborumgebung herzustellen. Stattdessen sollen offensichtliche und vermeidbare Störfaktoren reduziert werden, während die natürlichen Unterschiede der verwendeten Computersysteme bestehen bleiben.

Dadurch können die Ergebnisse anschließend im Rahmen des Feldexperimentes ausgewertet und interpretiert werden.
