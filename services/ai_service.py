import socket

from services.ollama_service import ollama_service


class AIService:

    def __init__(self):
        pass

    def internet_available(self):

        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return True
        except OSError:
            return False

    def ask(self, prompt: str):

        if not prompt:
            return "Please say something."

        # Currently use Ollama.
        # Later we'll automatically switch
        # between Offline AI and Online AI.

        return ollama_service.ask(prompt)


ai_service = AIService()