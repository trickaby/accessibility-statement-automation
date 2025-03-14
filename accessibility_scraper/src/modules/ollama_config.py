
class OllamaConfig:
    def __init__(
            self,
            model_name: str,
            system_prompt: str = None,
            options: dict = None
    ):
        self.model_name = model_name
        self.system_prompt = system_prompt
        if options is not None:
            self.options = {k: v for k, v in options.items() if v is not None and v != ""}