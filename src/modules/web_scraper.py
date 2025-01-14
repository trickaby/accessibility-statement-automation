import re
from datetime import datetime

from selenium import webdriver
from selenium.common import NoSuchElementException

from src.modules.constant_values import partially_compliant_format, fully_compliant_format, non_compliance_format, \
    output_date_format
from src.modules.data_handler import write_text_to_file
from src.modules.date_parser import extract_date_from_text

def open_page(url, is_headless):
    options = webdriver.ChromeOptions()
    if is_headless:
        options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    return driver

def check_header_present(driver, header_text):
    header = iterate_through_headers(driver, f"[contains(text(), '{header_text}')]")
    return "Yes" if header else "No"

def get_prepared_date(driver):
    return get_date_by_keywords(driver,"prepared on")

def get_last_reviewed_date(driver):
    return get_date_by_keywords(driver, "last reviewed on")

def get_last_tested_date(driver):
    return get_date_by_keywords(driver, "last tested on")

def days_since_last_tested(date_tested):
    return (datetime.now() - datetime.strptime(date_tested, output_date_format)).days

def extract_sentences_from_page(driver):
    page_content = driver.find_element("tag name", "body").text
    return re.split(r'(?<=[.!?])\s+|\n', page_content)


def get_sentence_by_keyword(driver, text):
    sentences = extract_sentences_from_page(driver)
    for sentence in sentences:
        if text in sentence:
            return sentence
    return "Not found"

def get_date_by_keywords(driver, text):
    sentence = get_sentence_by_keyword(driver, text)
    return extract_date_from_text(sentence)

def compliance_status(driver):
    header = "Compliance status"
    compliance_status_paragraph = get_text_under_header(driver, header)

    if "partially" in compliance_status_paragraph:
        return partially_compliant_format
    elif "fully" in compliance_status_paragraph:
        return fully_compliant_format
    elif "non-compliant" in compliance_status_paragraph:
        return non_compliance_format
    else:
        return "Not found"

def get_text_under_header(driver, header_text):
    return iterate_through_headers(driver, f"[contains(.,'{header_text}')]/following-sibling::p[1]")

def extract_who_carried_out(who_tested_sentence):
    pattern = r"carried out(?: [\w\s]+)? by ([\w\s]+)"

    match = re.search(pattern, who_tested_sentence)
    if match:
        return match.group(1).strip()
    return None


def who_tested_by(driver):
    who_tested_sentence = get_sentence_by_keyword(driver, "carried out")
    if "Home Office" in who_tested_sentence :
        return "Home Office"
    else : return extract_who_carried_out(who_tested_sentence).capitalize()

def iterate_through_headers(driver, xpath_filter):
    result = None
    for i in range(1, 7):
        xpath = f"//h{i}" + xpath_filter
        try:
            element = driver.find_element("xpath", xpath)
            result = element.text
        except NoSuchElementException:
            continue
    return result

def wcag_version(driver):
    header = "Compliance status"
    compliance_status_paragraph = get_text_under_header(driver, header)

    if "2.1" in compliance_status_paragraph:
        return "2.1"
    elif "2.2" in compliance_status_paragraph:
      return "2.2"
    return "Not found"

def check_legal_compliance(headings):
    return "No" if "No" in headings.values() else "Yes"

def list_non_compliant_headings(headings):
    non_compliant_list = []
    for heading, compliance in headings.items():
        if compliance == "No" :
            non_compliant_list.append(heading)
    if not non_compliant_list:
        return "N/A"
    return ", ".join(non_compliant_list)

def non_accessible_content(driver, product_name):
    elements = driver.find_elements("xpath", "//h3/following-sibling::*[not(self::h1 or self::h2 or self::h4 or self::h5 or self::h6)]")
    text = ""
    for element in elements :
        if "h" in element.tag_name:
            break
        text += element.text + "\n"

    text_file_uri = write_text_to_file(product_name + " - Non-accessible content.txt", text)
    return f"=HYPERLINK(\"{text_file_uri}\", \"Link to text\")"


def extract_phone_from_text(text):
    if text is None:
        return "N/A"
    phone_pattern = r'\b(?:\+44|0)(?:\s?\d\s?|\d{2,4}\s?)(?:\d\s?){6,10}\b'
    match = re.search(phone_pattern, text)
    return match.group(0).replace(" ", "") if match else "N/A"


def extract_email_from_text(text):
    if text is None:
        return "N/A"
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(email_pattern, text)
    return match.group(0).replace(" ", "") if match else "N/A"



def feedback_contact_email(driver):
    text = get_text_under_header(driver, "Feedback and contact information")
    return extract_email_from_text(text)


def feedback_contact_phone(driver):
    text = get_text_under_header(driver, "Feedback and contact information")
    return extract_phone_from_text(text)

def reporting_contact_email(driver):
    text = get_text_under_header(driver, "Reporting accessibility problems")
    return extract_email_from_text(text)

def reporting_contact_phone(driver):
    text = get_text_under_header(driver, "Reporting accessibility problems")
    return extract_phone_from_text(text)