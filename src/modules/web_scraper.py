import re

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from src.modules.constant_values import partially_compliant_format, fully_compliant_format, non_compliance_format
from src.modules.date_parser import extract_date_from_text

from datetime import datetime

date_tested = ""

def open_page(url, is_headless):
    options = webdriver.ChromeOptions()
    if is_headless:
        options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    return driver

def check_header_present(driver, header_text):
    try:
        header = driver.find_element(By.XPATH, f"//*[contains(text(), '{header_text}')]")
        return "Yes" if header else "No"
    except NoSuchElementException:
        return "No"

def get_prepared_date(driver):
    return get_date_by_keywords(driver,"prepared on")

def get_last_reviewed_date(driver):
    return get_date_by_keywords(driver, "last reviewed on")

def get_last_tested_date(driver):
    global date_tested
    date_tested = get_date_by_keywords(driver, "last tested on")
    return date_tested

def days_since_last_tested():
    return (datetime.now() - datetime.strptime(date_tested, "%d/%m/%Y")).days

def extract_sentences_from_page(driver):
    page_content = driver.find_element("tag name", "body").text
    return re.split(r'(?<=[.!?])\s+|\n', page_content)


def get_sentence_by_keyword(driver, text):
    sentences = extract_sentences_from_page(driver)
    for sentence in sentences:
        if text in sentence:
            return sentence
    return "Not Found"

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
    selector = f"//h2[normalize-space()='{header_text}']/following-sibling::p[1]"
    try:
        element = driver.find_element("xpath", selector)
        return element.text
    except NoSuchElementException:
        return None


def extract_who_carried_out(who_tested_sentence):
    # needs refinement, currently a bit of a placeholder
    pattern = r"carried out(?: internally)? by (.+)"

    match = re.search(pattern, who_tested_sentence)
    if match:
        return match.group(1).strip()
    return None


def who_tested_by(driver):
    who_tested_sentence = get_sentence_by_keyword(driver, "carried out")
    return extract_who_carried_out(who_tested_sentence)
