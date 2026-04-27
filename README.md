# Supplements Trends Analyse – Google Trends Dashboard

## 1. Executive Summary

Dieses Projekt analysiert die aktuellen Google Trends Suchdaten für die Kategorie Supplements
in Deutschland über den Zeitraum der letzten dreißig Tage.
Das Hauptziel der Analyse bestand darin, das relative Suchinteresse an klassischen
Sport-Nahrungsergänzungsmitteln wie Proteinpulver, Whey Protein und Kreatin mit allgemeinen
Gesundheits-Supplements wie Vitamin D und Magnesium zu vergleichen.
Die zentralen Erkenntnisse zeigen eine deutliche Verschiebung des Interesses hin zu Mikronährstoffen.
Insbesondere Magnesium weist den stärksten steigenden Trend sowie das höchste Suchvolumen auf.
Im Gegensatz dazu verzeichnen Whey Protein und Vitamin D einen eher rückläufigen Trend,
obwohl Vitamin D kurzfristig sehr hohe Such-Peaks erreichte.

## 2. Ziele des Projekts

Das vorrangige Ziel dieses Projekts ist es, datenbasierte Erkenntnisse über das aktuelle
Konsum- und Suchverhalten im Bereich der Nahrungsergänzungsmittel zu gewinnen.
Im Kontext von Google Trends wird untersucht, ob das Interesse an Sport-Supplements
zugunsten von präventiven Gesundheits-Supplements abnimmt.
Oftmals basieren Marketingentscheidungen in der Fitnessbranche auf reinen Bauchgefühlen
oder veralteten Erfahrungswerten.
Durch die automatisierte Erfassung, Bereinigung und KI-gestützte Interpretation der
Zeitreihendaten löst dieses Projekt das Problem der manuellen und fehleranfälligen Marktanalyse.
Es liefert Unternehmen oder Content-Erstellern eine fundierte, objektive Datengrundlage,
um Trends frühzeitig zu erkennen und Werbekampagnen präzise anzupassen.

## 3. Anwendung und Nutzung

Die Anwendung wurde so konzipiert, dass sie mit minimalem Konfigurationsaufwand
direkt in einer containerisierten Umgebung gestartet werden kann.
Zunächst wird das GitHub-Repository auf den lokalen Rechner geklont und eine
`.env` Datei im Root-Ordner mit dem API-Key angelegt.
Anschließend wird die gesamte Architektur mit folgendem Befehl hochgefahren:

\`\`\`bash
docker compose up --build -d
\`\`\`

Alternativ kann das System über den `k8s/` Ordner in Kubernetes deployt werden:

\`\`\`bash
kubectl apply -f k8s/
kubectl port-forward service/ai-service 8001:8000
\`\`\`

Nach dem Start sind die Ergebnisse unter `http://localhost:8001/analyze` abrufbar.
Potenzielle Nutzer sind Analysten, Fitness-Shop-Betreiber und Marketing-Agenturen,
die datengetriebene Empfehlungen für ihr Sortiment benötigen.

## 4. Datenanalyse und Ergebnisse

Die Auswertung der Zeitreihendaten offenbarte überraschend deutliche Muster im Suchverhalten.
Magnesium dominiert mit einem Durchschnittswert von über 88 und einem Peak von 100.
Vitamin D erreichte zwar signifikante Peaks von bis zu 78, verzeichnete jedoch einen fallenden Trend,
was auf saisonale Effekte und das beginnende Frühjahr hindeuten könnte.
Die Sport-Begriffe Kreatin, Proteinpulver und Whey Protein bewegen sich auf niedrigerem Niveau.
Besonders auffällig ist der Kontrast zwischen Whey Protein (sinkend) und Proteinpulver (steigend),
was auf eine Veränderung in der Suchsprache der Konsumenten hindeutet.
Der steigende Trend bei Kreatin und Proteinpulver deutet auf wachsendes Fitness-Interesse hin.

## 5. Visualisierung

Um die Daten greifbarer zu machen, wurden zwei spezifische Visualisierungsformen gewählt.
Zum einen wurde ein Liniendiagramm erstellt, das den zeitlichen Verlauf aller fünf Suchbegriffe
über dreißig Tage auf einer gemeinsamen Zeitachse darstellt.
Diese Darstellung ist essenziell, um kurzfristige Peaks und saisonale Einbrüche zu identifizieren.
Zum anderen wurde ein Balkendiagramm für das durchschnittliche Suchinteresse generiert,
das die Hierarchie der Begriffe klar und vergleichbar strukturiert.
Beide Visualisierungen helfen dabei, die KI-Aussagen visuell zu validieren
und auch Personen ohne Datenexpertise die Marktsituation sofort verständlich zu machen.

## 6. Herausforderungen und Learnings

Während der Entwicklung traten insbesondere bei der Datenbereinigung technische Hürden auf.
Die von Google Trends exportierten CSV-Dateien enthielten Metadaten sowie nicht-numerische
Zeichenketten wie `<1`, welche zunächst zu Programmabbrüchen beim Parsen führten.
Dieses Problem wurde durch eine robuste Python-Logik gelöst, die Sonderzeichen in Nullen konvertiert.
Fachlich herausfordernd war die reibungslose Kommunikation der Docker-Container untereinander,
gelöst durch Service-Namen statt localhost in der Docker-Compose-Konfiguration.
In Kubernetes musste verstanden werden, dass Pods flüchtig sind und Kommunikation
ausschließlich über stabile Service-Namen und internes DNS erfolgt.
Das wichtigste Learning war die strikte Trennung der Services für Wartbarkeit und Skalierbarkeit.

## 7. Zukunftsvision

In einer zukünftigen Version könnte der statische CSV-Import durch eine Live-Schnittstelle
zu Trend-Datenbanken ersetzt werden, um Analysen in echter Echtzeit zu ermöglichen.
Die Datenbasis könnte um demografische Merkmale oder geografische Unterschiede
auf Bundeslandebene erweitert werden.
Ein benutzerfreundliches Frontend mit React oder Streamlit würde interaktive Dashboards
ermöglichen, sodass Nutzer nicht mehr rohe JSON-Ausgaben lesen müssen.
Im Bereich KI könnten spezialisierte Modelle nicht nur deskriptive Analysen liefern,
sondern direkt umsetzbare Social-Media-Beiträge für Trend-Produkte generieren.
Eine CI/CD-Pipeline mit GitHub Actions könnte den gesamten Deployment-Prozess automatisieren
und den manuellen Aufwand vollständig eliminieren.
