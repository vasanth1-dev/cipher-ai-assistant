from collections import deque


class HistoryService:

    def __init__(self, limit=50):
        self.history = deque(maxlen=limit)

    def add(self, command, response):

        self.history.append(
            {
                "command": command,
                "response": response,
            }
        )

    def last(self):

        if not self.history:
            return None

        return self.history[-1]

    def all(self):

        return list(self.history)

    def clear(self):

        self.history.clear()


history_service = HistoryService()