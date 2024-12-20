import csv
from pathlib import Path
from src.modules.constant_values import root_dir

def read_input_csv(input_path):
    path = Path(root_dir, input_path)
    with open(path, newline='') as csv_file:
        return list(csv.DictReader(csv_file))

def write_output_csv(output_path, data, output_columns):
    path = Path(root_dir, output_path)
    with open(path, 'w', newline='', encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=output_columns)
        writer.writeheader()
        writer.writerows(data)
    return "Results written to: " + str(path)
