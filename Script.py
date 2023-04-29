import os
import pandas as pd
import chardet
import tkinter as tk
from tkinter import filedialog


# Funktion zum Extrahieren der CSV-Zeilen anhand des Schlüsselworts
def extract_csv_rows(csv_file, keyword):
    # Lesen der CSV-Datei in einen Pandas-Datenrahmen
    df = pd.read_csv(
        csv_file,
        encoding=get_csv_encoding(csv_file),
        on_bad_lines="skip",
        engine="python",
        skip_blank_lines=True,
    )
    # Extrahieren der Zeilen, die das angegebene Keyword enthalten
    extracted_df = df[df.iloc[:, 0].str.contains(keyword, na=False)]
    return extracted_df


# Funktion zum Durchsuchen des Eingabeverzeichnisses
def browse_input_directory():
    input_directory = filedialog.askdirectory()
    input_directory_entry.delete(0, tk.END)
    input_directory_entry.insert(0, input_directory)


# Funktion zum Durchsuchen der Ausgabedatei
def browse_output_file():
    output_file = filedialog.asksaveasfilename(defaultextension=".csv")
    output_file_entry.delete(0, tk.END)
    output_file_entry.insert(0, output_file)


# Funktion zum Zusammenführen und Extrahieren der CSV-Dateien
def merge_csv_files():
    input_directory = input_directory_entry.get()
    output_file = output_file_entry.get()
    keyword = keyword_entry.get()  # Abrufen des Schlüsselworts aus dem Eingabefeld

    # Suchen aller CSV-Dateien im angegebenen Verzeichnis
    csv_files = [f for f in os.listdir(input_directory) if f.endswith(".csv")]

    # Initialisieren des leeren DataFrames
    combined_df = pd.DataFrame()

    # Lesen jeder CSV-Datei und Zusammenführen der Zeilen, die das angegebene Keyword enthalten
    for csv_file in csv_files:
        csv_path = os.path.join(input_directory, csv_file)
        extracted_df = extract_csv_rows(csv_path, keyword)
        combined_df = pd.concat([combined_df, extracted_df])

    # Schreiben der bereinigten Daten in eine CSV-Datei
    combined_df.to_csv(output_file, index=False, sep="\n", encoding="utf-8-sig")


# Funktion zum Ermitteln der Kodierung einer CSV-Datei
def get_csv_encoding(file_path):
    with open(file_path, "rb") as f:
        result = chardet.detect(f.read())
        return result["encoding"]


# Erstellen des Hauptfensters und Festlegen des Titels
root = tk.Tk()
root.title("CSV Merger")

# Erstellen der Widgets für das Eingabeverzeichnis
input_directory_label = tk.Label(root, text="Eingabeverzeichnis:")
input_directory_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

input_directory_entry = tk.Entry(root, width=50)
input_directory_entry.grid(row=0, column=1, padx=5, pady=5)

input_directory_button = tk.Button(
    root, text="Durchsuchen", command=browse_input_directory
)
input_directory_button.grid(row=0, column=2, padx=5, pady=5)

# Erstellen der Widgets für die Ausgabedatei
output_file_label = tk.Label(root, text="Ausgabedatei:")
output_file_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

output_file_entry = tk.Entry(root, width=50)
output_file_entry.grid(row=1, column=1, padx=5, pady=5)

output_file_button = tk.Button(root, text="Durchsuchen", command=browse_output_file)
output_file_button.grid(row=1, column=2, padx=5, pady=5)

# Erstellen der Widgets für das Schlüsselwort
keyword_label = tk.Label(root, text="Schlüsselwort:")
keyword_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

keyword_entry = tk.Entry(root, width=50)
keyword_entry.grid(row=2, column=1, padx=5, pady=5)

# Erstellen der Schaltfläche zum Zusammenführen und Extrahieren der CSV-Dateien
merge_button = tk.Button(
    root, text="CSV-Dateien zusammenführen und extrahieren", command=merge_csv_files
)
merge_button.grid(row=3, column=1, padx=5, pady=5)

# Starten der main loop
root.mainloop()
