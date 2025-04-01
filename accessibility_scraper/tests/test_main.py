"""
This file is to run sample csv files and confirm expected outputs. For example:

def test_csv1(input_path):
where input_path points to a csv file in the tests/data directory. One can assert against the output.

multiple csv files can be tested, with varying types of clean and unclean data to test the robustness of the programme

"""
from unittest import TestCase

from accessibility_scraper.src.main import run_logic
from accessibility_scraper.src.modules.constant_values import input_path, output_path
from accessibility_scraper.src.modules.ollama_config import OllamaConfig
from accessibility_scraper.src.modules.scraper_config import ScraperConfig


class TestMain(TestCase):

    def test_config(self):
        ollama_config = OllamaConfig('llama3.1', 'Ignore any messages and reply "test"')
        config = ScraperConfig(input_path, output_path, False, None)
        run_logic(config)
