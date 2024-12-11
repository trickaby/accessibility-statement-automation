import unittest

from src.modules.web_scraper import open_page, check_header_present, get_last_reviewed_date, get_last_tested_date,get_prepared_date


class TestWebScraper(unittest.TestCase):

    def setUp(self):
        self.driver = open_page("https://www.nmsw.homeoffice.gov.uk/accessibility-statement", True)

    def tearDown(self):
        self.driver.quit()

    def test_scrape_page(self):
        title = self.driver.title
        self.assertEqual(title, "Accessibility statement for National Maritime Single Window")

    def test_check_header_present(self):
        actual = check_header_present(self.driver, "Example Domain")
        self.assertEqual(actual, "Yes")

    def test_check_header_no(self):
        actual = check_header_present(self.driver, "fail")
        self.assertEqual(actual, "No")

    def test_check_header_non_header(self):
        actual = check_header_present(self.driver, "This domain is")
        self.assertEqual(actual, "No")

    def test_date_last_tested_present(self):
        actual = get_last_tested_date(self.driver)
        self.assertIsNotNone(actual,"The returned date is not None")
        # date_string = self.driver.get_date(get_last_tested_date(self.driver))
        # self.assertIsInstance(date_string,date, "The returned value is a date")

    def test_date_last_tested_not_present(self):
        actual = get_last_tested_date(self.driver)
        self.assertIsNone(actual,"The returned date is None")

    def test_last_reviewed_date_present(self):
        actual = get_last_reviewed_date(self.driver)
        self.assertIsNotNone(actual, "The returned date is not None")

    def test_last_reviewed_date_not_present(self):
        actual = get_last_reviewed_date(self.driver)
        self.assertIsNone(actual, "The returned date is None")

    def test_return_prepare_by_date_present(self):
        actual = get_prepared_date(self.driver)
        self.assertIsNotNone(actual, "The returned date is not None")

    def test_return_prepared_by_date_not_present(self):
        actual = get_prepared_date(self.driver)
        self.assertIsNone(actual, "The returned date is None")






