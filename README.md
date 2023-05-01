# CSV Merger

CSV Merger is a Python application with a Tkinter GUI that searches through multiple CSV files in a selected directory, extracts rows containing a specified keyword, and then merges them into a single output file.

## Features

- Easy-to-use graphical interface
- Merge multiple CSV files from a selected directory
- Extract rows containing a specified keyword
- Save the merged and extracted data in a single output file
- Monitor the progress with a progress bar

## Requirements

- Python 3.6 or higher
- Tkinter
- Pandas
- Chardet

## Installation

1. Clone the repository or download the source code.
2. Install the required packages with pip:
   ```
   pip install pandas chardet
   ```

## Usage

1. Run the application by executing the main Python script:
   ```
   python csv_merger.py
   ```
2. In the GUI, click the "Browse" button next to the "Input Directory" field to select the directory containing the CSV files you want to merge and extract.
3. Click the "Browse" button next to the "Output File" field to select the file where the result should be saved.
4. Enter the keyword that must be present in the rows you want to extract from the CSV files.
5. Click the "Merge and Extract CSV Files" button to start the process.
6. Monitor the progress with the progress bar and the progress label.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
