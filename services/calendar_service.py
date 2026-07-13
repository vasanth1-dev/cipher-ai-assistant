import json
import os

from core.logger import logger


class CalendarService:

    def __init__(self):

        self.file = "data/calendar.json"

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.file):
            with open(self.file, "w", encoding="utf-8") as f:
                json.dump(
                    [],
                    f,
                    indent=4,
                    ensure_ascii=False,
                )

    def load(self):

        try:

            with open(
                self.file,
                "r",
                encoding="utf-8",
            ) as f:

                return json.load(f)

        except Exception as e:

            logger.exception(e)

            return []

    def save(self, events):

        try:

            with open(
                self.file,
                "w",
                encoding="utf-8",
            ) as f:

                json.dump(
                    events,
                    f,
                    indent=4,
                    ensure_ascii=False,
                )

        except Exception as e:

            logger.exception(e)

    def add(self, title, date_time):

        if not title:
            return "Event title cannot be empty."
        
        title = title.strip()

        events = self.load()

        events.append(
            {
                "title": title,
                "datetime": date_time,
            }
        )
        events.sort(
            key=lambda event: event["datetime"]
        )

        self.save(events)

        logger.info(
            f"[CALENDAR] Added event: {title}"
        )

        return "Event added successfully. "

    def list(self):

        events = self.load()

        events.sort(
            key = lambda event: event["datetime"]
        )

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
            return "Invalid event number. "
        
        removed = events.pop(index - 1)

        self.save(events)

        logger.info(
            f"[CALENDAR] Deleted event: {removed['title']}"
        )

        return(
            f"Deleted event: "
            f"{removed['title']}"
        )


calendar_service = CalendarService()