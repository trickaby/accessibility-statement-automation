from modules.web_scraper import scrape_page, check_header_present, get_prepared_date, get_last_reviewed_date, \
    get_last_tested_date
from src.modules.constant_values import input_path, output_path, output_columns
from modules.data_handler import read_input_csv, write_output_csv

output_data = []

def main():
    print("pls")
    input_data = read_input_csv(input_path)

    for row in input_data:
        url = row.get('Statement URL', 'No URL found')
        driver = scrape_page(url)
        data = {
            "URL": url,
              "Date Prepared By": get_prepared_date(driver),
              "Date Last Reviewed": get_last_reviewed_date(driver),
              "Date Last Tested": get_last_tested_date(driver),
            # "Days Since Last Tested": days_since_last_tested(),
            # "Who Tested By": who_tested_by(),
            "Feedback Header Present": check_header_present(driver, 'Feedback and contact information'),
            "Reporting Problems Header Present": check_header_present(driver, 'Reporting accessibility problems'),
            "Enforcement Procedure Header Present": check_header_present(driver, 'Enforcement procedure'),
            # "Compliance Status": compliance_status(),
        }
        driver.quit()
        output_data.append(data)
    write_output_csv(output_path, output_data, output_columns)

if __name__ == "__main__":
    main()
