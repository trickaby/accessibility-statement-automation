import csv

def read_input_csv(input_path):
    with open(input_path, newline='') as csvfile:
        return list(csv.DictReader(csvfile))

def write_output_csv(output_path, data, output_columns):
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=output_columns)
        writer.writeheader()
        writer.writerows(data)
