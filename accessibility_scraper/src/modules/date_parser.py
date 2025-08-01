from  dateutil.parser import parse

from accessibility_scraper.src.modules.constant_values import output_date_format


def extract_date_from_text(text):
    try:
        parsed_date = parse(text, fuzzy=True)
        return parsed_date.date()
    except ValueError:
        return None
