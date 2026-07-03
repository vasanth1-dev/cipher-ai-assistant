import requests


def get_weather(city="auto"):

    try:

        url = f"https://wttr.in/{city}?format=3"

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Cipher"
            },
        )

        if response.status_code == 200:
            return response.text.strip()

        return "Unable to fetch weather."

    except Exception:
        return "Internet connection is unavailable."


def handle(command: str):

    if not command:
        return None

    command = command.lower().strip()

    # -------------------------
    # Current Weather
    # -------------------------

    if command in (
        "weather",
        "current weather",
        "today weather",
        "weather today",
    ):
        return get_weather()

    # -------------------------
    # City Weather
    # -------------------------

    if command.startswith("weather in "):

        city = command.replace("weather in ", "", 1).strip()

        if not city:
            return "Which city?"

        return get_weather(city)

    return None