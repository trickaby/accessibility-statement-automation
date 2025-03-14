import ollama


class OllamaConversation:
  def __init__(
          self,
          model_name: str,
          system_prompt: str = None,
          options: dict = None
  ):
    self.model_name = model_name
    self.system_prompt = system_prompt
    self.options = options

    self.conversation_history = []

    if system_prompt:
      self.conversation_history.append({
        "role": "system",
        "content": system_prompt
      })

  def add_user_message(self, message: str):
    self.conversation_history.append({
      "role": "user",
      "content": message
      })

  def get_model_response(self) -> str:
    response = ollama.chat(
      model=self.model_name,
      messages=self.conversation_history,
      keep_alive=0,
      options=self.options
    )
    model_message = response['message']['content']

    self.conversation_history.append({"role": "assistant", "content": model_message})

    return model_message

  def get_conversation_history(self) -> list:
    return self.conversation_history

  def reset_conversation(self):
    self.conversation_history = []

