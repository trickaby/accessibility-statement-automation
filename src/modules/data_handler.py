import csv
import os
import webbrowser
from pathlib import Path
from src.modules.constant_values import root_dir, text_dir


def read_input_csv(input_path):
    path = Path(root_dir, input_path)
    with open(path, newline='') as csv_file:
        return list(csv.DictReader(csv_file))

def write_output_csv(output_path, data, output_columns):
    path = Path(root_dir, output_path)
    with open(path, 'w', newline='', encoding="utf-8") as csv_file:
        csv_file.write('\ufeff')
        writer = csv.DictWriter(csv_file, fieldnames=output_columns)
        writer.writeheader()
        writer.writerows(data)
    return str(path)

def open_csv(filepath):
    if os.name == 'nt':       # Windows
        os.startfile(filepath)
    elif os.name == 'posix':  # macOS/Linux
        webbrowser.open(f"file://{filepath}")
    else:
        print(f"Cannot open file on this OS: {filepath}")

def write_text_to_file(filename, text):
    path = Path(root_dir) / text_dir
    path.mkdir(parents=True, exist_ok=True)
    file_path = path / filename
    file_path.write_text(text)


    return str(file_path.resolve().as_uri())
