import os

from google import genai
from config import AI_PERSONALITY


class GeminiService:

    def __init__(
       self,
    ) -> None:

        self.client = None

        api_key = os.getenv("GEMINI_API_KEY")

        if api_key:
            self.client = genai.Client(api_key=api_key)

    def available(self):

        return self.client is not None

    def ask(self, prompt: str):

        if not self.available():
            return None

        try:

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"""
                you are Cipher, a voice assistant

                Rule:
                - Reply naturally.
                - Maximum 3 short sentences.
                - Don't write article-style content.
                - Be coversational
                

                {AI_PERSONALITY}\n\nUser: {prompt}
                """
            )

            return response.text.strip()

        except Exception as e:

            if "RESOURCE_EXHAUSTED" in str(e):
                return None


gemini_service = GeminiService()