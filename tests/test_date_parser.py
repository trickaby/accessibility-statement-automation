import unittest

from src.modules.date_parser import extract_date_from_text


class TestDateParser(unittest.TestCase):

    def test_sample_test(self):
        test_cases = [
            ("16 December 2024", "16/12/2024"),
            ("16 Dec 2024", "16/12/2024"),
            ("December 16 2024", "16/12/2024"),
            ("16/12/2024", "16/12/2024"),
            ("", None),
            ("No date here!", None),
        ]

        for input_date, expected_output in test_cases:
            with self.subTest(input_date=input_date, expected_output=expected_output):
                result = extract_date_from_text(input_date)
                self.assertEqual(result, expected_output)
