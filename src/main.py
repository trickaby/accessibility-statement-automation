from src.modules.constant_values import input_path, output_path
from src.modules.data_handler import read_input_csv, write_output_csv
from src.modules.web_scraper import open_page, check_header_present, get_prepared_date, get_last_reviewed_date, \
    get_last_tested_date, compliance_status, who_tested_by, days_since_last_tested, wcag_version, \
    check_legal_compliance, list_non_compliant_headings, non_accessible_content

output_data = []

def scrape_page(driver, product_name):
    data = {}
    dates = {
        "Prepared by date": get_prepared_date(driver),
        "Last reviewed date": get_last_reviewed_date(driver),
    }
    date_last_tested = get_last_tested_date(driver)
    dates.update({"Last tested date": date_last_tested})
    data.update(dates)

    data.update({"Days Since Last Tested": days_since_last_tested(date_last_tested)})

    data.update({"Who Tested By": who_tested_by(driver)})

    legal_wording = {
        "Feedback wording": check_header_present(driver, 'Feedback and contact information'),
        "Reporting Problems wording": check_header_present(driver, 'Reporting accessibility problems'),
        "Enforcement Procedure wording": check_header_present(driver, 'Enforcement procedure'),
    }
    legal_wording.update({"Legal compliance wording": check_legal_compliance(legal_wording)})
    legal_wording.update({"Legal wording not present": list_non_compliant_headings(legal_wording)})

    data.update(legal_wording)

    data.update({
        "Compliance Status": compliance_status(driver),
        "WCAG": wcag_version(driver),
    })

    data.update({"Non-accessible content": non_accessible_content(driver, product_name)})
    return data

def main():
    run_logic(input_path, output_path, False)

def run_logic(input_file,output_file_path, is_headless):
    input_data = read_input_csv(input_file)
    for row in input_data:
        url = "No URL found"
        for key, value in row.items():
            if 'URL' in key:
                url = value
        try:
            driver = open_page(url, is_headless)
            product_name = row.get("Product name", "Product name not found")
            data = {
                "Product name": product_name,
            }
            data.update(scrape_page(driver, product_name))
            driver.quit()
            output_data.append(data)
        except Exception as e:
            print(f"Row {row.get('Product name', 'not found')}: Failed to scrape {url}. Error: {e}")
    headers = output_data[0].keys()
    return write_output_csv(output_file_path, output_data, headers)

if __name__ == "__main__":
    main()
