"""
This file is to run sample csv files and confirm expected outputs. For example:

def test_csv1(input_path):
where input_path points to a csv file in the tests/data directory. One can assert against the output.

multiple csv files can be tested, with varying types of clean and unclean data to test the robustness of the programme

"""
from unittest import TestCase

from ui.apps import ScraperConfig


class TestMain(TestCase):

    def test_config(self):
        ScraperConfig('file_path', 'output_file_path', True)
