import subprocess

from config import (
    GOOGLE_URL,
    YOUTUBE_URL,
    GITHUB_URL,
    GOOGLE_SEARCH,
    YOUTUBE_SEARCH,
)


def open_url(url: str):

    try:

        subprocess.Popen(
            ["xdg-open", url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )

        return True

    except Exception:
        return False


def handle(command: str):

    if not command:
        return None

    command = command.lower().strip()

    # ----------------------------------
    # Open Websites
    # ----------------------------------

    websites = {
        "open google": GOOGLE_URL,
        "open youtube": YOUTUBE_URL,
        "open github": GITHUB_URL,
        "open gmail": "https://mail.google.com",
        "open chatgpt": "https://chatgpt.com",
        "open linkedin": "https://linkedin.com",
    }

    if command in websites:

        if open_url(websites[command]):
            return f"Opening {command.replace('open ', '').title()}."

        return "Unable to open browser."

    # ----------------------------------
    # Google Search
    # ----------------------------------

    if command.startswith("search google "):

        query = command.replace("search google ", "", 1).strip()

        if not query:
            return "What should I search on Google?"

        url = GOOGLE_SEARCH.format(query.replace(" ", "+"))

        if open_url(url):
            return f"Searching Google for {query}."

        return "Unable to open browser."

    # ----------------------------------
    # YouTube Search
    # ----------------------------------

    if command.startswith("search youtube "):

        query = command.replace("search youtube ", "", 1).strip()

        if not query:
            return "What should I search on YouTube?"

        url = YOUTUBE_SEARCH.format(query.replace(" ", "+"))

        if open_url(url):
            return f"Searching YouTube for {query}."

        return "Unable to open browser."

    return None