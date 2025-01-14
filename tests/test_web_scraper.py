import unittest

from src.modules.constant_values import partially_compliant_format
from src.modules.web_scraper import open_page, check_header_present, get_last_reviewed_date, get_last_tested_date, \
    get_prepared_date, extract_sentences_from_page, get_sentence_by_keyword, compliance_status, get_text_under_header, \
    extract_who_carried_out, wcag_version, check_legal_compliance, list_non_compliant_headings, non_accessible_content, \
    extract_email_from_text, extract_phone_from_text


class TestWebScraper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = open_page("https://www.nmsw.homeoffice.gov.uk/accessibility-statement", False)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_scrape_page(self):
        title = self.driver.title
        self.assertEqual("Accessibility statement for National Maritime Single Window", title)

    def test_check_header_present(self):
        actual = check_header_present(self.driver, "Accessibility statement for National Maritime Single Window")
        self.assertEqual("Yes", actual)

    def test_check_header_no(self):
        actual = check_header_present(self.driver, "fail")
        self.assertEqual("No", actual)

    def test_check_header_non_header(self):
        actual = check_header_present(self.driver, "This website is run by Home Office.")
        self.assertEqual("No", actual)

    def test_date_last_tested_present(self):
        actual = get_last_tested_date(self.driver)
        self.assertIsNotNone("The returned date is not None", actual)

    def test_last_reviewed_date_present(self):
        actual = get_last_reviewed_date(self.driver)
        self.assertIsNotNone("The returned date is not None", actual)

    def test_return_prepare_by_date_present(self):
        actual = get_prepared_date(self.driver)
        self.assertIsNotNone("The returned date is not None", actual)

    def test_extract_sentences_from_page(self):
        actual = extract_sentences_from_page(self.driver)
        self.assertIsNotNone("List of sentences is None", actual)
        self.assertGreater(len(actual), 0, "List of sentences is empty")

    def test_get_sentence_by_keyword(self):
        test_cases = [
            ("Zoom in up to 250%", "Zoom in up to 250% without the text spilling off the screen"),
            ("We're always looking to improve the accessibility of this website",
             "We're always looking to improve the accessibility of this website."),
            ("nmsw@homeoffice.gov.uk.",
             "If you find any problems not listed on this page or think we're not meeting accessibility requirements, contact nmsw@homeoffice.gov.uk."),
            ("partially compliant",
             "This website is partially compliant with the Web Content Accessibility Guidelines version 2.1 AA standard, due to the non-compliances listed below."),
            ("No sentence!", "Not found"),
        ]
        for keyword, expected_output in test_cases:
            actual = get_sentence_by_keyword(self.driver, keyword)
            with self.subTest(input_date=keyword):
                self.assertEqual(expected_output, actual)

    def test_compliance_status(self):
        actual = compliance_status(self.driver)
        self.assertEqual(partially_compliant_format, actual)

    def test_get_text_under_header(self):
        expected_output = "At this time, we have not made any disproportionate burden claims."
        test_cases = [
            "Disproportionate burden",
            "Disproportionate",
            "burden",
        ]
        for search_term in test_cases:
            actual = get_text_under_header(self.driver, search_term)
            with self.subTest(search_term=search_term):
                self.assertEqual(expected_output, actual)

        self.assertIsNone(get_text_under_header(self.driver, "Not found"))

    def test_extract_who_carried_out(self):
        test_cases = [
            ("Testing was carried out internally by the Home Office.", "the Home Office"),
            ("The test was carried out internally by the Home Office.", "the Home Office"),
            ("incorrectly formatted string", None),
            ("This was carried by a donkey", None)
        ]
        for sentence, expected_output in test_cases:
            actual = extract_who_carried_out(sentence)
            with self.subTest(actual=actual, expected=expected_output):
                self.assertEqual(expected_output, actual)

    def test_wcag_version(self):
        actual = wcag_version(self.driver)
        self.assertEqual("2.1", actual)

    def test_legal_compliance(self):
        headings = {
            "test1": "Yes",
            "test2": "Yes"
        }
        actual = check_legal_compliance(headings)
        self.assertEqual("Yes", actual)
        headings.update({"test3": "No"})
        actual2 = check_legal_compliance(headings)
        self.assertEqual("No", actual2)

    def test_list_non_compliant_headings(self):
        test_cases = [
            ({"test1": "Yes", "test2": "No"}, "test2"),
            ({"test1": "No" , "test2": "No"}, "test1, test2"),
            ({}                             , "N/A")
        ]
        for headings, expected_output in test_cases:
            actual = list_non_compliant_headings(headings)
            with self.subTest(actual=actual, expected=expected_output):
                self.assertEqual(expected_output, actual)

    def test_non_accessible_content(self):
        actual = non_accessible_content(self.driver, "TEST")
        self.assertIsNotNone(actual)

    def test_extract_email_from_text(self):
        positive = "Test text with email@email.com included"
        negative = "Text without email"
        live = "not meeting accessibility requirements, contact nmsw@homeoffice.gov.uk."
        testcases = [
            (positive, "email@email.com"),
            (negative, "N/A"),
            (None, "N/A"),
            (live, "nmsw@homeoffice.gov.uk")
        ]
        for text_input, expected_output in testcases:
            actual = extract_email_from_text(text_input)
            with self.subTest(actual=actual, expected=expected_output):
                self.assertEqual(expected_output, actual)

    def test_extract_phone_from_text(self):
        positive = "Test text with 07123456789 included"
        negative = "Text 123 without phone"

        testcases = [
            (positive, "07123456789"),
            (negative, "N/A"),
            (None, "N/A")
        ]
        for text_input, expected_output in testcases:
            actual = extract_phone_from_text(text_input)
            with self.subTest(actual=actual, expected=expected_output):
                self.assertEqual(expected_output, actual)