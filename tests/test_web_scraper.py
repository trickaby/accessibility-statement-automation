import unittest

from src.modules.web_scraper import scrape_page

class TestWebScraper(unittest.TestCase):

    def scrape_page_test(self):
        driver = scrape_page("www.google.com")
        self.assertEqual(driver.title, "Google")

    def scrape_page_null_test(self):
        driver = scrape_page("")
