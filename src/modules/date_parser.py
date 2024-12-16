from  dateutil.parser import parse

from src.modules.constant_values import output_date_format


def extract_date_from_text(text):
    try:
        parsed_date = parse(text, fuzzy=True)
        return parsed_date.strftime(output_date_format)
    except ValueError:
        return None
