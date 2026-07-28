import re
from datetime import datetime, timedelta


class TimeParser:

    def parse(self, text: str):

        text = text.lower().strip()
        now = datetime.now()

        # ---------------------------------
        # In X minutes
        # ---------------------------------

        match = re.search(r"in (\d+) minute(s)?", text)

        if match:
            minutes = int(match.group(1))
            return (now + timedelta(minutes=minutes)).isoformat(timespec="seconds")

        # ---------------------------------
        # In X hours
        # ---------------------------------

        match = re.search(r"in (\d+) hour(s)?", text)

        if match:
            hours = int(match.group(1))
            return (now + timedelta(hours=hours)).isoformat(timespec="seconds")

        # ---------------------------------
        # In X days
        # ---------------------------------

        match = re.search(r"in (\d+) day(s)?", text)

        if match:
            days = int(match.group(1))
            return (now + timedelta(days=days)).isoformat(timespec="seconds")

        # ---------------------------------
        # Tomorrow HH:MM
        # ---------------------------------

        match = re.search(r"tomorrow\s+(\d{1,2}):(\d{2})", text)

        if match:

            hour = int(match.group(1))
            minute = int(match.group(2))

            dt = now + timedelta(days=1)
            dt = dt.replace(
                hour=hour,
                minute=minute,
                second=0,
                microsecond=0,
            )

            return dt.isoformat(timespec="seconds")

        # ---------------------------------
        # Today HH:MM
        # ---------------------------------

        match = re.search(r"today\s+(\d{1,2}):(\d{2})", text)

        if match:

            hour = int(match.group(1))
            minute = int(match.group(2))

            dt = now.replace(
                hour=hour,
                minute=minute,
                second=0,
                microsecond=0,
            )

            if dt < now:
                dt += timedelta(days=1)

            return dt.isoformat(timespec="seconds")
        

        # ---------------------------------
        # HH AM/PM
        # ---------------------------------

        match = re.fullmatch(
            r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)",
            text,
        )

        if match:

            hour = int(match.group(1))
            minute = int(match.group(2) or 0)
            period = match.group(3)

            if period == "pm" and hour != 12:
                hour += 12

            elif period == "am" and hour == 12:
                hour = 0

            dt = now.replace(
                hour=hour,
                minute=minute,
                second=0,
                microsecond=0,
            )

            if dt < now:
                dt += timedelta(days=1)

            return dt.isoformat(timespec="seconds")

        # ---------------------------------
        # HH:MM (today or tomorrow)
        # ---------------------------------

        match = re.fullmatch(r"(\d{1,2}):(\d{2})", text)

        if match:

            hour = int(match.group(1))
            minute = int(match.group(2))

            dt = now.replace(
                hour=hour,
                minute=minute,
                second=0,
                microsecond=0,
            )

            if dt < now:
                dt += timedelta(days=1)

            return dt.isoformat(timespec="seconds")

        # ---------------------------------
        # Unable to parse
        # ---------------------------------

        return None


time_parser = TimeParser()