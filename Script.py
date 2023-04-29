import os  # Importieren der os-Bibliothek für Dateioperationen
import pandas as pd  # Importieren der Pandas-Bibliothek für die Datenverarbeitung
import chardet  # Importieren der chardet-Bibliothek zur automatischen Bestimmung der Kodierung von CSV-Dateien
import tkinter as tk  # Importieren der Tkinter-Bibliothek für GUI-Entwicklung
from tkinter import (
    filedialog,
)  # Importieren des filedialog-Moduls aus Tkinter für die Arbeit mit Dateidialogen


def get_csv_encoding(file_path):
    """
    Diese Funktion gibt die Kodierung einer CSV-Datei zurück.
    """
    with open(
        file_path, "rb"
    ) as f:  # Öffnen der Datei im binären Modus, um auch Nicht-Text-Dateien zu lesen
        result = chardet.detect(
            f.read()
        )  # Lesen des Dateiinhalts und Bestimmung der Kodierung durch die chardet-Bibliothek
        return result["encoding"]  # Rückgabe der Kodierung


def merge_csv_files(input_directory, output_file):
    csv_files = [
        f for f in os.listdir(input_directory) if f.endswith(".csv")
    ]  # Suchen aller CSV-Dateien im angegebenen Verzeichnis
    combined_csv = pd.concat(
        [
            pd.read_csv(
                os.path.join(input_directory, f),
                encoding=get_csv_encoding(os.path.join(input_directory, f)),
                on_bad_lines="skip",
                engine="python",
                skip_blank_lines=True,
            )
            for f in csv_files
        ],
        ignore_index=True,
    )  # Lesen aller CSV-Dateien und Zusammenführen zu einer einzigen Datenrahmen-Datei
    cleaned_csv = combined_csv[
        combined_csv.iloc[:, 0].str.startswith("BEST", na=False)
    ]  # Extrahieren der Datensätze, die mit 'BEST' beginnen
    cleaned_csv.to_csv(
        output_file, index=False, sep="\n", encoding="utf-8-sig"
    )  # Schreiben der bereinigten Daten in eine CSV-Datei


# Erstellen der Funktion zur Auswahl des Eingabeverzeichnisses über einen Dateidialog
def browse_input_directory():
    input_directory = filedialog.askdirectory()
    input_directory_entry.delete(0, tk.END)
    input_directory_entry.insert(0, input_directory)


# Erstellen der Funktion zur Auswahl des Ausgabepfads über einen Dateidialog
def browse_output_file():
    output_file = filedialog.asksaveasfilename(defaultextension=".csv")
    output_file_entry.delete(0, tk.END)
    output_file_entry.insert(0, output_file)


# Erstellen der Funktion zur Zusammenführung der CSV-Dateien und Bereinigung der Daten
def merge_csv_files():
    input_directory = input_directory_entry.get()
    output_file = output_file_entry.get()

    csv_files = [f for f in os.listdir(input_directory) if f.endswith(".csv")]

    combined_csv = pd.concat(
        [
            pd.read_csv(
                os.path.join(input_directory, f),
                encoding=get_csv_encoding(os.path.join(input_directory, f)),
                on_bad_lines="skip",
                engine="python",
                skip_blank_lines=True,
            )
            for f in csv_files
        ],
        ignore_index=True,
    )

    cleaned_csv = combined_csv[combined_csv.iloc[:, 0].str.startswith("BEST", na=False)]

    cleaned_csv.to_csv(output_file, index=False, sep="\n", encoding="utf-8-sig")


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

# Erstellen der Schaltfläche zum Zusammenführen der CSV-Dateien
merge_button = tk.Button(
    root, text="CSV-Dateien zusammenführen", command=merge_csv_files
)
merge_button.grid(row=2, column=1, padx=5, pady=5)

# Starten der main loop
root.mainloop()
