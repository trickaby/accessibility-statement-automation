from src.modules.web_scraper import open_page, check_header_present, get_prepared_date, get_last_reviewed_date, \
    get_last_tested_date, compliance_status, who_tested_by, days_since_last_tested
from src.modules.constant_values import input_path, output_path, output_columns
from src.modules.data_handler import read_input_csv, write_output_csv

output_data = []

def scrape_page(driver, url):
    return {
        "URL": url,
        "Date Prepared By": get_prepared_date(driver),
        "Date Last Reviewed": get_last_reviewed_date(driver),
        "Date Last Tested": get_last_tested_date(driver),
        "Days Since Last Tested": days_since_last_tested(),
        "Who Tested By": who_tested_by(driver),
        "Feedback Header Present": check_header_present(driver, 'Feedback and contact information'),
        "Reporting Problems Header Present": check_header_present(driver, 'Reporting accessibility problems'),
        "Enforcement Procedure Header Present": check_header_present(driver, 'Enforcement procedure'),
        "Compliance Status": compliance_status(driver),
    }

def main():
    run_logic(input_path, False)

def run_logic(input_file, is_headless):
    input_data = read_input_csv(input_file)
    for row in input_data:
        url = row.get('Statement URL', 'No URL found')
        try:
            driver = open_page(url, is_headless)
            data = scrape_page(driver, url)
            driver.quit()
            output_data.append(data)
        except Exception as e:
            print(f"Row {row.get('Product name', 'not found')}: Failed to scrape {url}. Error: {e}")
    return write_output_csv(output_path, output_data, output_columns)

if __name__ == "__main__":
    main()
