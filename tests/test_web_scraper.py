import unittest

from selenium import webdriver

from src.modules.web_scraper import open_page, check_header_present


class TestWebScraper(unittest.TestCase):

    def setUp(self):
        self.driver = open_page("https://www.example.com", True)

    def tearDown(self):
        self.driver.quit()

    def test_scrape_page(self):
        title = self.driver.title
        self.assertEqual(title, "Example Domain")

    def test_check_header_present(self):
        actual = check_header_present(self.driver, "Example Domain")
        self.assertEqual(actual, "Yes")

    def test_check_header_no(self):
        actual = check_header_present(self.driver, "fail")
        self.assertEqual(actual, "No")

    def test_check_header_non_header(self):
        actual = check_header_present(self.driver, "This domain is")
        self.assertEqual(actual, "No")