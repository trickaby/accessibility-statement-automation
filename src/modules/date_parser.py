import re
from datetime import datetime

from src.modules.constant_values import output_date_format

date_patterns = [
    r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b",                  # e.g., 31/03/2023 or 31-03-23
    r"\b(\d{1,2}\s\w+\s\d{2,4})\b",                          # e.g., 31 March 2023
    r"\b(\w+\s\d{1,2},\s\d{2,4})\b",                         # e.g., March 31, 2023
    r"\b(\d{4}[/-]\d{1,2}[/-]\d{1,2})\b",                    # e.g., 2023-03-31
]

#         date_formats (list of str, optional): List of date formats to normalize the date.
#                                               Defaults to common formats.
date_formats = [
    "%d/%m/%Y", "%d-%m-%Y", "%d %B %Y", "%B %d, %Y", "%Y-%m-%d",
    "%d/%m/%y", "%d-%m-%y"
]

def extract_date_from_text(text):
    """
    Extracts a date from a given string using regex and returns it in a normalized format.

    Args:
        text (str): The input string containing the date.


    Returns:
        str or None: The normalized date in 'DD/MM/YYYY' format, or None if no valid date is found.
    """

    # Combine regex patterns
    combined_pattern = "|".join(date_patterns)

    # Search for dates in the text
    matches = re.finditer(combined_pattern, text, re.IGNORECASE)

    # Normalize dates
    for match in matches:
        matched_date = match.group()
        for fmt in date_formats:
            try:
                return datetime.strptime(matched_date, fmt).strftime(output_date_format)
            except ValueError:
                continue

    # Return None if no date is found or valid
    return None




