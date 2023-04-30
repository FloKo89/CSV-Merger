import os # Importieren der os-Bibliothek zum Durchsuchen von Verzeichnissen
import pandas as pd # Importieren der pandas-Bibliothek zum Lesen und Schreiben von CSV-Dateien
import chardet # Importieren der chardet-Bibliothek zum Ermitteln der Kodierung einer CSV-Datei
import tkinter as tk # Importieren der tkinter-Bibliothek zum Erstellen der Benutzeroberfläche
from tkinter import filedialog, ttk # Importieren der filedialog- und ttk-Bibliotheken zum Durchsuchen von Verzeichnissen und zum Erstellen von Widgets

background_color = "#e0f0ff" # Hintergrundfarbe des Hauptfensters
foreground_color = "#000033" # Vordergrundfarbe des Hauptfensters
button_color = "#4d79ff" # Farbe der Schaltflächen

class CSV_Merger(tk.Tk):
    def __init__(self):
        super().__init__()

        self.iconbitmap("icon.ico")
        self.title("CSV Merger")
        self.resizable(False, False)
        self.columnconfigure(1, weight=1)
        self.geometry("550x220")
        self.configure(background=background_color)
        self.eval('tk::PlaceWindow . center')


        self.input_directory_label = tk.Label(self, background=background_color, foreground=foreground_color, text="Eingabeverzeichnis:", font=("Helvetica", 12))
        self.input_directory_label.grid(row=0, column=0, padx=(15, 5), pady=(15, 5), sticky=tk.W)

        self.input_directory_entry = tk.Entry(self, bg="white", fg=foreground_color, insertbackground=foreground_color, width=50, font=("Helvetica", 12))
        self.input_directory_entry.grid(row=0, column=1, padx=5, pady=(15, 5))

        self.input_directory_button = tk.Button(
            self, text="Durchsuchen", command=self.browse_input_directory, bg=button_color, fg="white", font=("Helvetica", 9)
        )
        self.input_directory_button.grid(row=0, column=2, padx=(5, 15), pady=(15, 5))
        self.create_tooltip(self.input_directory_button, "Wählen Sie das Verzeichnis aus, in dem sich die CSV-Dateien befinden, die Sie zusammenführen möchten.")

        self.output_file_label = tk.Label(self, background=background_color, foreground=foreground_color, text="Ausgabedatei:", font=("Helvetica", 12))
        self.output_file_label.grid(row=1, column=0, padx=(15, 5), pady=5, sticky=tk.W)

        self.output_file_entry = tk.Entry(self, bg="white", fg=foreground_color, insertbackground=foreground_color, width=50, font=("Helvetica", 12))
        self.output_file_entry.grid(row=1, column=1, padx=5, pady=5)

        self.output_file_button = tk.Button(self, bg=button_color, fg="white", text="Durchsuchen", command=self.browse_output_file, font=("Helvetica", 9))
        self.output_file_button.grid(row=1, column=2, padx=(5, 15), pady=5)
        self.create_tooltip(self.output_file_button, "Wählen Sie die Datei aus, in der das Ergebnis gespeichert werden soll.")

        self.keyword_label = tk.Label(self, background=background_color, foreground=foreground_color, text="Schlüsselwort:", font=("Helvetica", 12))
        self.keyword_label.grid(row=2, column=0, padx=(15, 5), pady=5, sticky=tk.W)
        self.keyword_var = tk.StringVar()
        self.keyword_var.trace("w", self.update_merge_button_state)

        self.keyword_entry = tk.Entry(self, bg="white", fg=foreground_color, insertbackground=foreground_color, width=50, textvariable=self.keyword_var, font=("Helvetica", 12))
        self.keyword_entry.grid(row=2, column=1, padx=5, pady=5)
        self.create_tooltip(self.keyword_entry, "Geben Sie das Schlüsselwort ein, das in den Zeilen vorhanden sein muss, die Sie aus den CSV-Dateien extrahieren möchten.")

        self.merge_button = tk.Button(
        self, bg=button_color, fg="white", text="CSV-Dateien zusammenführen und extrahieren", command=self.merge_csv_files, state="disabled", font=("Helvetica", 9)
        )
        self.merge_button.grid(row=3, column=1, padx=5, pady=5)

        self.progress_bar = ttk.Progressbar(
        self, orient="horizontal", length=300, mode="determinate"
        )
        self.progress_bar.grid(row=4, column=1, padx=5, pady=5)

        self.progress_label = tk.Label(self, background=background_color, foreground=foreground_color, text="Fortschritt: 0%", font=("Helvetica", 12))
        self.progress_label.grid(row=5, column=1, padx=5, pady=5)

    # Funktion zum Extrahieren der CSV-Zeilen anhand des Schlüsselworts
    def extract_csv_rows(self, csv_file, keyword):
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
    def browse_input_directory(self):
        input_directory = filedialog.askdirectory(title="Eingabeverzeichnis auswählen")
        if input_directory:  # Stellen Sie sicher, dass der Benutzer ein Verzeichnis ausgewählt hat
            self.input_directory_entry.delete(0, tk.END)
            self.input_directory_entry.insert(0, input_directory)

    # Funktion zum Durchsuchen der Ausgabedatei
    def browse_output_file(self):
        output_file = filedialog.asksaveasfilename(defaultextension=".csv", title="Ausgabedatei auswählen")
        if output_file:  # Stellen Sie sicher, dass der Benutzer eine Datei ausgewählt hat
            self.output_file_entry.delete(0, tk.END)
            self.output_file_entry.insert(0, output_file)

    # Funktion zum Ermitteln der Kodierung einer CSV-Datei
    def get_csv_encoding(self, file_path):
        with open(file_path, "rb") as f:
            result = chardet.detect(f.read())
            return result["encoding"]

    # Funktion zum Zusammenführen und Extrahieren der CSV-Dateien
    def merge_csv_files(self):
        input_directory = self.input_directory_entry.get()
        output_file = self.output_file_entry.get()
        keyword = self.keyword_entry.get()  # Abrufen des Schlüsselworts aus dem Eingabefeld

        # Suchen aller CSV-Dateien im angegebenen Verzeichnis
        csv_files = [f for f in os.listdir(input_directory) if f.endswith(".csv")]

        # Initialisieren des leeren DataFrames
        combined_df = pd.DataFrame()

        # Fortschrittsanzeige
        self.progress_bar["maximum"] = len(csv_files)
        self.progress_bar["value"] = 0

        # Lesen jeder CSV-Datei und Zusammenführen der Zeilen, die das angegebene Keyword enthalten
        for i, csv_file in enumerate(csv_files):
            csv_path = os.path.join(input_directory, csv_file)
            extracted_df = self.extract_csv_rows(csv_path, keyword)
            combined_df = pd.concat([combined_df, extracted_df])
            # Fortschrittsanzeige aktualisieren
            self.progress_bar["value"] = i + 1
            percentage = round((i + 1) / len(csv_files) * 100, 2)
            self.progress_label["text"] = f"Fortschritt: {percentage}%"
            self.update_idletasks()

        # Schreiben der bereinigten Daten in eine CSV-Datei
        combined_df.to_csv(output_file, index=False, header=False, sep=';', line_terminator='\n')
    
    # Funktion zum Aktualisieren des Status der Schaltfläche "Zusammenführen"
    def update_merge_button_state(self, *args):
        if self.input_directory_entry.get() and self.output_file_entry.get() and self.keyword_var.get():
            self.merge_button.config(state="normal")
        else:
            self.merge_button.config(state="disabled")

    # Funktion zum Erstellen eines Tooltipps für ein Widget
    def create_tooltip(self, widget, text):
        def enter(event):
            x = y = 0
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
            tooltip_window = tk.Toplevel(widget)
            tooltip_window.wm_overrideredirect(True)
            tooltip_window.wm_geometry(f"+{x}+{y}")
            label = tk.Label(tooltip_window, text=text, background="#ffffe0", relief="solid", borderwidth=1, font=("tahoma", "8", "normal"))
            label.pack()
            widget.tooltip_window = tooltip_window

        # Funktion zum schließen des Tooltipps
        def leave(event):
            if hasattr(widget, 'tooltip_window'):
                widget.tooltip_window.destroy()
        # Binden der Ereignisse "Enter" und "Leave" an das Widget    
        widget.bind("<Enter>", enter) 
        widget.bind("<Leave>", leave)

# Starten der Anwendung
if __name__ == "__main__": 
    app = CSV_Merger()
    app.mainloop()
