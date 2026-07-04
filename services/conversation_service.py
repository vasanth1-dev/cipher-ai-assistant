from collections import deque


class ConversationService:

    def __init__(self, max_history=10):
        self.messages = deque(maxlen=max_history)

    def add_user(self, message: str):

        if message:
            self.messages.append(
                {
                    "role": "user",
                    "content": message.strip(),
                }
            )

    def add_assistant(self, message: str):

        if message:
            self.messages.append(
                {
                    "role": "assistant",
                    "content": message.strip(),
                }
            )

    def build_prompt(self, current_prompt: str):

        prompt = ""

        for msg in self.messages:
            prompt += f"{msg['role']}: {msg['content']}\n"

        prompt += f"user: {current_prompt}\nassistant:"

        return prompt

    def clear(self):
        self.messages.clear()


conversation_service = ConversationService()