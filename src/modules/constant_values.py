from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent

input_path = "tests/data/input.csv"
output_path = "src/data/output.csv"
output_path_dir = "src/data/"
text_dir = "src/data/text/"

output_date_format = "%d/%m/%Y" #DD/MM/YYYY

partially_compliant_format = "Partially compliant"
fully_compliant_format = "Fully compliant"
non_compliance_format = "Non-compliant"