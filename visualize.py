import pandas as pd
import matplotlib.pyplot as plt
import csv

# 1. Wir suchen exakt die Zeile, wo die echten Daten anfangen (wie in deiner API)
csv_path = "data/zeitverlauf.csv"
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = list(csv.reader(f))

start_line = 0
for i, row in enumerate(reader):
    if row and any(key in row[0] for key in ["Woche", "Monat", "Zeit", "Time"]):
        start_line = i
        break

# 2. Daten laden, ab der gefundenen Startzeile
df = pd.read_csv(csv_path, skiprows=start_line)

# 3. Spaltennamen bereinigen (schneidet ": (Deutschland)" ab, falls Google das ergänzt hat)
df.columns = [str(c).split(':')[0].strip() for c in df.columns]

# Zeit-Spalte als Index setzen
df.set_index(df.columns[0], inplace=True)

# "<1" Werte durch 0 ersetzen und in Zahlen umwandeln
df = df.replace('<1', 0).astype(int)

# --- Visualisierung 1: Zeitverlauf (Line Chart) ---
plt.figure(figsize=(12, 6))
for column in df.columns:
    plt.plot(df.index, df[column], marker='o', label=column)

plt.title('Google Trends: Suchinteresse über den Zeitverlauf', fontsize=14)
plt.xlabel('Zeitraum')
plt.ylabel('Interesse (0-100)')
# Damit sich die Datumsangaben unten nicht überschneiden, zeigen wir nur jedes 3. Datum an
plt.xticks(df.index[::3], rotation=45, ha='right')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('zeitverlauf_chart.png')
print("✅ Zeitverlauf-Diagramm repariert und gespeichert.")

# --- Visualisierung 2: Durchschnitts-Vergleich (Bar Chart) ---
plt.figure(figsize=(10, 6))
means = df.mean().sort_values(ascending=False)
colors = ['#4CAF50', '#2196F3', '#FF9800', '#F44336', '#9C27B0']

# Das Diagramm zeichnen
ax = means.plot(kind='bar', color=colors[:len(means)])
plt.title('Durchschnittliches Suchinteresse pro Supplement', fontsize=14)
plt.ylabel('Durchschnittswert (Mean)')

# Jetzt stehen die Namen unten richtig und gut lesbar!
plt.xticks(rotation=45, ha='right')

# Als Bonus: Wir schreiben die genaue Zahl oben auf den Balken
for i, v in enumerate(means):
    ax.text(i, v + 1, str(round(v, 1)), ha='center', fontweight='bold')

plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('vergleich_durchschnitt_chart.png')
print("✅ Durchschnitt-Diagramm repariert und gespeichert.")

plt.show()