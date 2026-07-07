import json
import os


class CalendarService:

    def __init__(self):

        self.file = "data/calendar.json"

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.file):
            with open(self.file, "w") as f:
                json.dump([], f)

    def load(self):

        with open(self.file, "r") as f:
            return json.load(f)

    def save(self, events):

        with open(self.file, "w") as f:
            json.dump(events, f, indent=4)

    def add(self, title, date_time):

        events = self.load()

        events.append(
            {
                "title": title,
                "datetime": date_time,
            }
        )

        self.save(events)

        return "Event added successfully."

    def list(self):

        events = self.load()

        if not events:
            return "Your calendar is empty."

        result = []

        for i, event in enumerate(events, 1):

            result.append(
                f"{i}. {event['title']} - {event['datetime']}"
            )

        return "\n".join(result)

    def delete(self, index):

        events = self.load()

        if index < 1 or index > len(events):
            return "Invalid event number."

        events.pop(index - 1)

        self.save(events)

        return "Event deleted."


calendar_service = CalendarService()