from accessibility_scraper.src.modules.constant_values import input_path, output_path
from accessibility_scraper.src.modules.data_handler import read_input_csv, write_output_csv
from accessibility_scraper.src.modules.ollama_chat import OllamaConversation
from accessibility_scraper.src.modules.scraper_config import ScraperConfig
from accessibility_scraper.src.modules.web_scraper import get_prepared_date, get_last_reviewed_date, \
    get_last_tested_date, days_since_last_tested, who_tested_by, check_header_present, list_non_compliant_headings, \
    check_legal_compliance, compliance_status, wcag_version, feedback_contact_email, feedback_contact_phone, \
    reporting_contact_email, reporting_contact_phone, non_accessible_content, open_page, extract_non_accessible_text

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
        "Feedback header - wording": check_header_present(driver, 'Feedback and contact information'),
        "Reporting Problems - wording": check_header_present(driver, 'Reporting accessibility problems with this website'),
        "Enforcement Procedure - wording": check_header_present(driver, 'Enforcement procedure'),
    }
    legal_wording.update({"Legal compliance - wording": check_legal_compliance(legal_wording)})
    legal_wording.update({"Legal wording not present": list_non_compliant_headings(legal_wording)})

    data.update(legal_wording)

    data.update({
        "Compliance Status": compliance_status(driver),
        "WCAG": wcag_version(driver),
    })

    data.update({
        "Feedback contact email": feedback_contact_email(driver),
        "Feedback contact phone": feedback_contact_phone(driver),
        "Reporting problems contact email": reporting_contact_email(driver),
        "Reporting problems contact phone": reporting_contact_phone(driver),
    })

    data.update({"Non-accessible content": non_accessible_content(driver, product_name)})
    return data

def main():
    config = ScraperConfig(input_path, output_path, False)
    run_logic(config)

def run_logic(config):
    input_data = read_input_csv(config.input_file)
    for row in input_data:
        url = "No URL found"
        for key, value in row.items():
            if 'URL' in key:
                url = value
        try:
            driver = open_page(url, config.headless_mode)
            product_name = row.get("Product name", "Product name not found")
            data = {
                "Product name": product_name,
            }
            data.update(scrape_page(driver, product_name))
            if config.ollama_config is not None:
                conversation = OllamaConversation(config.ollama_config.model_name, config.ollama_config.system_prompt)
                conversation.add_user_message(extract_non_accessible_text(driver))
                data.update({"RAG rating(AI generated)": conversation.get_model_response()})
            driver.quit()
            output_data.append(data)
        except Exception as e:
            print(f"Row {row.get('Product name', 'not found')}: Failed to scrape {url}. Error: {e}")
    headers = output_data[0].keys()
    return write_output_csv(config.output_file, output_data, headers)

if __name__ == "__main__":
    main()
