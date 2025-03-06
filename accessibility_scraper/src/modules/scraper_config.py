from typing import Optional

from accessibility_scraper.src.modules.ollama_config import OllamaConfig


class ScraperConfig:
    def __init__(self, input_file, output_file, headless_mode=False, ollama_config: Optional[OllamaConfig]=None):
        self.input_file = input_file
        self.output_file = output_file
        self.headless_mode = headless_mode
        self.ollama_config = ollama_config

