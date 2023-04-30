import os
import pandas as pd
import chardet
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

# Funktion zum Extrahieren der CSV-Zeilen anhand des Schlüsselworts
def extract_csv_rows(csv_file, keyword):
    # Lesen der CSV-Datei in einen Pandas-Datenrahmen
    df = pd.read_csv(
        csv_file,
        encoding=get_csv_encoding(csv_file),
        on_bad_lines="skip",
        engine="python",
        skip_blank_lines=True,
        sep=";",
        header=None,
        na_filter=False
    )
    # Extrahieren der Zeilen, die das angegebene Keyword enthalten
    df = df.applymap(str)  # alle Zellen in Strings umwandeln
    extracted_df = df[df.apply(lambda row: row.astype(str).str.contains(keyword).any(), axis=1)]
    return extracted_df

# Funktion zum Durchsuchen des Eingabeverzeichnisses
def browse_input_directory():
    input_directory = filedialog.askdirectory(title="Eingabeverzeichnis auswählen")
    if input_directory:  # Stellen Sie sicher, dass der Benutzer ein Verzeichnis ausgewählt hat
        input_directory_entry.delete(0, tk.END)
        input_directory_entry.insert(0, input_directory)


# Funktion zum Durchsuchen der Ausgabedatei
def browse_output_file():
    output_file = filedialog.asksaveasfilename(defaultextension=".csv", title="Ausgabedatei auswählen")
    if output_file:  # Stellen Sie sicher, dass der Benutzer eine Datei ausgewählt hat
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

    # Fortschrittsanzeige
    progress_bar["maximum"] = len(csv_files)
    progress_bar["value"] = 0

    # Lesen jeder CSV-Datei und Zusammenführen der Zeilen, die das angegebene Keyword enthalten
    for i, csv_file in enumerate(csv_files):
        csv_path = os.path.join(input_directory, csv_file)
        extracted_df = extract_csv_rows(csv_path, keyword)
        combined_df = pd.concat([combined_df, extracted_df])
        # Fortschrittsanzeige aktualisieren
        progress_bar["value"] = i + 1
        percentage = round((i + 1) / len(csv_files) * 100, 2)
        progress_label["text"] = f"Fortschritt: {percentage}%"
        root.update_idletasks()

    # Schreiben der bereinigten Daten in eine CSV-Datei
    combined_df.to_csv(output_file, index=False, header=False, sep=';', line_terminator='\n')

# Funktion zum Ermitteln der Kodierung einer CSV-Datei
def get_csv_encoding(file_path):
    with open(file_path, "rb") as f:
        result = chardet.detect(f.read())
        return result["encoding"]
    
def update_merge_button_state(*args):
    if input_directory_entry.get() and output_file_entry.get() and keyword_var.get():
        merge_button.config(state="normal")
    else:
        merge_button.config(state="disabled")



root = tk.Tk() # Erstellen des Hauptfensters 
root.iconbitmap("icon.ico") # Hinzufügen eines Programmsymbols
root.title("CSV Merger") # Titel des Hauptfensters
root.resizable(False, False)# Festlegen, dass die Größe des Hauptfensters nicht geändert werden kann
root.columnconfigure(1, weight=1)  # Festlegen, dass die Spalte 1 des Hauptfensters beim Ändern der Fenstergröße gestreckt wird
root.geometry("550x220")  # Festlegen der Fenstergröße
root.eval('tk::PlaceWindow . center')  # Zentrieren des Hauptfensters
root.configure(background="white")  # Festlegen der Hintergrundfarbe des Hauptfensters

# Erstellen und platzieren der Widgets für das Eingabeverzeichnis
input_directory_label = tk.Label(root, text="Eingabeverzeichnis:", font=("Helvetica", 12))
input_directory_label.grid(row=0, column=0, padx=(15, 5), pady=(15, 5), sticky=tk.W)

input_directory_entry = tk.Entry(root, width=50, font=("Helvetica", 12))
input_directory_entry.grid(row=0, column=1, padx=5, pady=(15, 5))

input_directory_button = tk.Button(
    root, text="Durchsuchen", command=browse_input_directory, font=("Helvetica", 9)
)
input_directory_button.grid(row=0, column=2, padx=(5, 15), pady=(15, 5))

# Erstellen und platzieren der Widgets für das Ausgabeverzeichnis
output_file_label = tk.Label(root, text="Ausgabedatei:", font=("Helvetica", 12))
output_file_label.grid(row=1, column=0, padx=(15, 5), pady=5, sticky=tk.W)

output_file_entry = tk.Entry(root, width=50, font=("Helvetica", 12))
output_file_entry.grid(row=1, column=1, padx=5, pady=5)

output_file_button = tk.Button(root, text="Durchsuchen", command=browse_output_file, font=("Helvetica", 9))
output_file_button.grid(row=1, column=2, padx=(5, 15), pady=5)

# Erstellen und platzieren der Widgets für das Schlüsselwort
keyword_label = tk.Label(root, text="Schlüsselwort:", font=("Helvetica", 12))
keyword_label.grid(row=2, column=0, padx=(15, 5), pady=5, sticky=tk.W)
keyword_var = tk.StringVar()
keyword_var.trace("w", update_merge_button_state)

keyword_entry = tk.Entry(root, width=50, textvariable=keyword_var, font=("Helvetica", 12))
keyword_entry.grid(row=2, column=1, padx=5, pady=5)

# Erstellen und platzieren der Widgets für den Merge-Button
merge_button = tk.Button(
    root, text="CSV-Dateien zusammenführen und extrahieren", command=merge_csv_files, state="disabled", font=("Helvetica", 9)
)
merge_button.grid(row=3, column=1, padx=5, pady=5)

# Erstellen und platzieren der Widgets für die Fortschrittsanzeige
progress_bar = ttk.Progressbar(
    root, orient="horizontal", length=300, mode="determinate"
)
progress_bar.grid(row=4, column=1, padx=5, pady=5)

progress_label = tk.Label(root, text="Fortschritt: 0%", font=("Helvetica", 12))
progress_label.grid(row=5, column=1, padx=5, pady=5)

# Starten der Mainloop
root.mainloop()

