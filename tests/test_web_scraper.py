import re
import unittest
from datetime import datetime

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
        actual = check_header_present(self.driver, "Accessibility statement for National Maritime Single Window ")
        self.assertEqual(actual, "Yes")

    def test_check_header_no(self):
        actual = check_header_present(self.driver, "fail")
        self.assertEqual(actual, "No")

    def test_check_header_non_header(self):
        actual = check_header_present(self.driver, "Accessibility statement for National Maritime Single Window")
        self.assertEqual(actual, "No")

    def test_date_last_tested_present(self):
        actual = get_last_tested_date(self.driver)
        self.assertIsNotNone(actual,"The returned date is not None")

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

    def date_format(self, date_text):
        # the date_text can be updated with any returned date such as reviewed, tested, prepared
        date_text = get_last_tested_date(self.driver)

        # Define generic patterns for dates
        date_patterns = [
            (r"(\d{1,2})[ /](\d{1,2})[ /](\d{2,4})", "%d/%m/%Y"),  # e.g., 31/3/2023, 3/31/2023
            (r"(\d{1,2})[ /]([A-Za-z]+)[ /](\d{2,4})", "%d/%B/%Y"),  # e.g., 31/March/2023
            (r"([A-Za-z]+)[ /](\d{1,2})[ /](\d{2,4})", "%B/%d/%Y"),  # e.g., March/31/2023
            (r"(\d{1,2})[ ]([A-Za-z]+)[ ](\d{4})", "%d %B %Y"),  # e.g., 31 March 2023
            (r"([A-Za-z]+)[ ](\d{1,2})[ ](\d{4})", "%B %d %Y"),  # e.g., March 31 2023
        ]
        for pattern, date_format in date_patterns:
            match = re.match(pattern, date_text)
            if match:
                try:
                    # Parse the date using the matched format
                    parsed_date = datetime.strptime(date_text, date_format)
                    # Return the normalized format
                    return parsed_date.strftime("%d %B %Y")
                except ValueError:
                    continue

            # If no pattern matches, raise an error
        raise ValueError(f"Date format '{date_text}' is not valid!")

    def test_date_normalization(self):
            """Verify the date is normalized to '31 March 2023'."""
            date_text = get_last_tested_date(self.driver)

            # Normalize the date
            try:
                normalized_date = self.date_format(date_text)
            except ValueError as e:
                self.fail(str(e))  # Fail the test if the date format is invalid

            # Check the normalized date
            self.assertEqual(normalized_date, "31 March 2023",
                             f"Normalized date is '{normalized_date}' but expected '31 March 2023'!")

