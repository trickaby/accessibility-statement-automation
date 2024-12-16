import unittest

from src.modules.date_parser import extract_date_from_text


class TestDateParser(unittest.TestCase):
    def test_sample_test(self):
        formatted_date = extract_date_from_text("21 December 2023")
        formatted_date = extract_date_from_text("21 Sept 2023")
        formatted_date = extract_date_from_text("21 Sep 2023")
        self.assertEqual("21/12/2023", formatted_date)


