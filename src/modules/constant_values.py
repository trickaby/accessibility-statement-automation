from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent

input_path = "tests/data/input.csv"
output_path = "src/data/output.csv"

output_columns = [
    "URL", "Date Prepared By", "Date Last Reviewed", "Date Last Tested",
    "Days Since Last Tested", "Who Tested By", "Feedback Header Present",
    "Reporting Problems Header Present", "Enforcement Procedure Header Present",
    "Compliance Status"
]

output_date_format = "%d/%m/%Y" #DD/MM/YYYY

partially_compliant_format = "Partial"
fully_compliant_format = "Full"
non_compliance_format = "None"