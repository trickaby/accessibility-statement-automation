from unittest import TestCase

from accessibility_scraper.src.modules.ollama_chat import OllamaConversation


class TestOllamaConversation(TestCase):

    def test_add_user_message(self):
        test_conversation = OllamaConversation('llama3.1', 'Remember the word "September"')
        test_conversation.add_user_message('What is the word I said to remember?')
        conversation_history = test_conversation.get_conversation_history()
        self.assertEqual(
            [
                {'role': 'system', 'content': 'Remember the word "September"'},
                {'role': 'user', 'content': 'What is the word I said to remember?'}
            ],
            conversation_history)

    def test_get_conversation_history(self):
        test_conversation = OllamaConversation('llama3.1', 'Remember the word "September"')
        test_conversation.add_user_message('What is the word I said to remember?')
        conversation_history = test_conversation.get_conversation_history()
        print(conversation_history)
        self.assertEqual(
            [
                {'role': 'system', 'content': 'Remember the word "September"'},
                {'role': 'user', 'content': 'What is the word I said to remember?'}
            ],
        conversation_history)


    def test_get_model_response(self):
        test_conversation = OllamaConversation('llama3.1', 'Remember the word "September"')
        test_conversation.add_user_message('What is the word I said to remember?')
        message = test_conversation.get_model_response()
        print(message)
        self.assertIn('september', message.lower())


    def test_reset_conversation(self):
        test_conversation = OllamaConversation('llama3.1', 'Remember the word "September"')
        test_conversation.reset_conversation()
        test_conversation.add_user_message('What is the word I said to remember?')
        message = test_conversation.get_model_response()
        print(message)
        self.assertNotIn('september', message.lower())

    def test_start_a_conversation_with_llama(self):
        test_conversation = OllamaConversation('llama3.1', 'Remember the word "September"')
        test_conversation.add_user_message('What is the word I said to remember?')
        message = test_conversation.get_model_response()
        print(message)
        self.assertIn('september', message.lower())
        test_conversation.add_user_message('forget the previous word. Now repeat the word October')
        message2 = test_conversation.get_model_response()
        print(message2)
        self.assertIn('october', message2.lower())