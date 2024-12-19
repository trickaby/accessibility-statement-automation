import csv

def read_input_csv(input_path):
    with open(input_path, newline='') as csv_file:
        return list(csv.DictReader(csv_file))

def write_output_csv(output_path, data, output_columns):
    with open(output_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=output_columns)
        writer.writeheader()
        writer.writerows(data)
