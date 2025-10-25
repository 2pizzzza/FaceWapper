# FaceWapper: AI Face Swapping Chrome Extension

## Überblick

**FaceWapper** ist ein Projekt, das die Fähigkeiten moderner generativer Modelle in Verbindung mit Browser-Erweiterungen demonstriert. Das Hauptziel ist es, Gesichter auf Bildern, die auf einer beliebigen Webseite gefunden werden, in Echtzeit durch das Gesicht eines Benutzers zu ersetzen.

Das Projekt besteht aus zwei Hauptteilen:
1.  **Browser-Erweiterung (Frontend)**: Läuft im Browser des Benutzers, findet Bilder auf der geöffneten Seite und steuert deren Austausch.
2.  **Lokaler Server (Backend)**: Nimmt Anfragen von der Erweiterung entgegen, verarbeitet die Bilder mit einem neuronalen Netzwerkmodell und gibt das Ergebnis zurück.

---

## Wie es funktioniert

Die Architektur des Projekts ist einfach und effizient:

1.  **Initiierung**: Der Benutzer klickt auf die Schaltfläche "Swap Faces" im Popup-Fenster der Erweiterung.
2.  **Bildersammlung**: Die Erweiterung (über `content/facewapper.js`) scannt die aktive Webseite, findet alle Bilder, die den Mindestanforderungen an die Größe (größer als 100x100 Pixel) entsprechen, und sammelt deren URLs.
3.  **Anfrage an das Backend**: Die gesammelten URLs werden an einen lokalen Python-Server unter `http://127.0.0.1:5000/swap-images` gesendet.
4.  **Verarbeitung auf dem Server**:
    *   Der Flask-Server lädt jedes Bild asynchron von der URL herunter.
    *   Mit Hilfe der **InsightFace**-Bibliothek findet er Gesichter auf dem heruntergeladenen Bild und auf dem Referenzfoto (`sample_faces/Prof.Grimm-1.jpg`).
    *   Das Modell `inswapper_128.onnx` führt den Gesichtsaustausch durch.
    *   Das verarbeitete Bild wird im lokalen Ordner `server/image/` gespeichert und erhält eine lokale URL.
5.  **Rückgabe des Ergebnisses**: Der Server gibt eine Liste der neuen URLs für die verarbeiteten Bilder an die Erweiterung zurück.
6.  **Aktualisierung der Seite**: Die Erweiterung ersetzt die `src`-Attribute der ursprünglichen `<img>`-Tags durch die neuen URLs, wodurch der Benutzer die Bilder mit den ausgetauschten Gesichtern auf der Seite sieht.

---

## Projektstruktur

```
/
├─── extension/         # Quellcode der Browser-Erweiterung
│    ├─── manifest.json     # Manifest, das die Erweiterung beschreibt
│    ├─── background.js     # Service Worker für Hintergrundaufgaben
│    ├─── content/
│    │    └─── facewapper.js # Skript, das in die Seite injiziert wird, um Bilder zu sammeln und zu ersetzen
│    └─── popup/
│         ├─── popup.html    # Benutzeroberfläche des Popup-Fensters
│         └─── popup.js      # Logik für die Schaltfläche im Popup-Fenster
│
└─── server/            # Quellcode des Backend-Servers
     ├─── main.py           # Hauptdatei des Flask-Servers
     ├─── requirements.txt  # Liste der Python-Abhängigkeiten
     ├─── image/            # Ordner zum Speichern der verarbeiteten Bilder
     └─── sample_faces/     # Ordner für Referenzgesichter
          └─── Prof.Grimm-1.jpg # Ausgangsgesicht für den Austausch
```

---

## Installations- und Startanleitung

### Voraussetzungen

*   Python 3.8+ und `pip`
*   Ein Chromium-basierter Webbrowser (Google Chrome, Edge usw.)

### 1. Backend-Einrichtung

Zuerst muss der lokale Server gestartet werden.

1.  **Navigieren Sie zum Server-Verzeichnis:**
    ```bash
    cd server
    ```

2.  **Installieren Sie die erforderlichen Python-Bibliotheken:**
    ```bash
    pip install -r requirements.txt
    ```
    *Hinweis: Die Installation von `insightface` und `onnxruntime` kann einige Zeit dauern.*

3.  **Stellen Sie sicher, dass das Referenzfoto vorhanden ist:**
    Im Ordner `server/sample_faces/` muss sich die Datei `Prof.Grimm-1.jpg` befinden. Sie können sie durch ein beliebiges anderes Bild mit einem klaren Gesicht ersetzen.

4.  **Starten Sie den Server:**
    ```bash
    python main.py
    ```
    Nach dem Start sollten Sie in der Konsole Meldungen über das Laden der Modelle und den Start des Servers auf Port 5000 sehen.

### 2. Frontend-Einrichtung (Browser-Erweiterung)

1.  **Öffnen Sie den Browser** und gehen Sie zur Seite für die Verwaltung der Erweiterungen: `chrome://extensions`.
2.  **Aktivieren Sie den "Entwicklermodus"** (Developer mode) in der oberen rechten Ecke.
3.  **Klicken Sie auf "Entpackte Erweiterung laden"** (Load unpacked).
4.  Wählen Sie im sich öffnenden Fenster den Ordner `extension` aus dem Stammverzeichnis des Projekts aus.

Danach erscheint das Symbol der **FaceWapper**-Erweiterung in Ihrem Browser.

---

## Anwendung

1.  Stellen Sie sicher, dass der lokale Server **läuft**.
2.  Besuchen Sie eine beliebige Webseite mit Bildern von Personen (z. B. eine Nachrichtenseite oder ein soziales Netzwerk).
3.  Klicken Sie auf das Symbol der **FaceWapper**-Erweiterung in der Symbolleiste des Browsers.
4.  Klicken Sie im Popup-Fenster auf die Schaltfläche **"Swap Faces"**.
5.  Warten Sie einige Sekunden. Die Bilder auf der Seite werden ersetzt.

---

## Modell und Danksagung

Das Projekt verwendet das vortrainierte Modell `inswapper_128.onnx` aus dem **InsightFace**-Repository.

*   **Modellquelle**: [Hugging Face - comfyflow-models](https://huggingface.co/xingren23/comfyflow-models/blob/976de8449674de379b02c144d0b3cfa2b61482f2/insightface/inswapper_128.onnx)
*   **Hauptbibliothek**: [InsightFace](https://github.com/deepinsight/insightface)

Vielen Dank an die Autoren dieser Tools für ihren Beitrag zur Open-Source-Community.

---

## Wichtige Backend-Abhängigkeiten

*   **Flask**: Web-Framework zur Erstellung der API.
*   **insightface**: Umfassendes Toolkit für 2D/3D-Gesichtsanalyse.
*   **onnxruntime**: Laufzeitumgebung für Modelle im ONNX-Format.
*   **opencv-python**: Bibliothek zur Bildverarbeitung.