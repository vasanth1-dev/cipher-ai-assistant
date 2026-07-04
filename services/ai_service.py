import socket

from services.ollama_service import ollama_service
from services.gemini_service import gemini_service
from services.conversation_service import conversation_service
from services.memory_service import memory_service


class AIService:

    def internet_available(self):

        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return True
        except OSError:
            return False

    def ask(self, prompt: str):

        if not prompt:
            return "Please say something."

        # Build conversation context

        memory = memory_service.memory_prompt()
        full_prompt = (
            memory +
            "\n" +
            conversation_service.build_prompt(prompt)
        )
        # ---------- Online AI (Gemini) ----------
        if self.internet_available() and gemini_service.available():

            response = gemini_service.ask(full_prompt)

            if response and not response.startswith("Gemini Error"):
                conversation_service.add_user(prompt)
                conversation_service.add_assistant(response)
                return response

        # ---------- Offline AI (Ollama) ----------
        response = ollama_service.ask(full_prompt)

        conversation_service.add_user(prompt)
        conversation_service.add_assistant(response)

        return response


ai_service = AIService()