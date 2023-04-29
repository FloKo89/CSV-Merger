import os  # Importieren der os-Bibliothek für Dateioperationen
import pandas as pd  # Importieren der Pandas-Bibliothek für die Datenverarbeitung
import chardet  # Importieren der chardet-Bibliothek zur automatischen Bestimmung der Kodierung von CSV-Dateien


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


input_directory = "N:/EDV/Onlineshop/Statistik/Neu/CSV Shopbestellungen/Rohdaten/Warenkörbe"  # Pfad zum Verzeichnis mit den Eingabedateien
output_file = "N:/EDV/Onlineshop/Statistik/Neu/CSV Shopbestellungen/merged_cleaned.csv"  # Pfad zur Ausgabedatei
merge_csv_files(
    input_directory, output_file
)  # Aufruf der Funktion zur Zusammenführung der CSV-Dateien
