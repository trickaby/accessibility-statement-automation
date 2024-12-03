import re

from selenium import webdriver
from selenium.webdriver.common.by import By

from src.modules.date_parser import extract_date_from_text


def scrape_page(url):
    driver = webdriver.Chrome()
    driver.get(url)
    return driver

def check_header_present(driver, header_text):
    try:
        header = driver.find_element(By.XPATH, f"//*[contains(text(), '{header_text}')]")
        return "Yes" if header else "No"
    except:
        return "No"


def get_prepared_date(driver):
    return get_date_by_keywords(driver,"prepared on")

def get_last_reviewed_date(driver):
    return get_date_by_keywords(driver, "last reviewed on")

def get_last_tested_date(driver):
    return get_date_by_keywords(driver, "last tested on")



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