import subprocess
from urllib.parse import quote_plus

from core.logger import logger

from config import (
    GOOGLE_URL,
    YOUTUBE_URL,
    GITHUB_URL,
    GOOGLE_SEARCH,
    YOUTUBE_SEARCH,
)


INTENT = "browser"


def open_url(url: str):

    try:

        subprocess.Popen(
            ["xdg-open", url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )

        logger.info(f"[BROWSER] {url}")

        return True

    except Exception as e:

        logger.exception(e)

        return False


def _search(base_url, query):

    url = base_url.format(
        quote_plus(query)
    )

    return open_url(url)


def handle(command: str):

    if not command:
        return None

    command = " ".join(
        command.lower().strip().split()
    )

    # -------------------------------------------------
    # Open Websites
    # -------------------------------------------------

    websites = {

        "open google": (
            "Google",
            GOOGLE_URL,
        ),

        "open youtube": (
            "YouTube",
            YOUTUBE_URL,
        ),

        "open github": (
            "GitHub",
            GITHUB_URL,
        ),

        "open gmail": (
            "Gmail",
            "https://mail.google.com",
        ),

        "open chatgpt": (
            "ChatGPT",
            "https://chatgpt.com",
        ),

        "open linkedin": (
            "LinkedIn",
            "https://linkedin.com",
        ),
    }

    if command in websites:

        name, url = websites[command]

        if open_url(url):
            return f"Opening {name}."

        return "Unable to open the browser."

    # -------------------------------------------------
    # Google Search
    # -------------------------------------------------

    prefix = "search google "

    if command.startswith(prefix):

        query = command[len(prefix):].strip()

        if not query:
            return "What should I search on Google?"

        if _search(GOOGLE_SEARCH, query):
            return f"Searching Google for {query}."

        return "Unable to open the browser."

    # -------------------------------------------------
    # YouTube Search
    # -------------------------------------------------

    prefix = "search youtube "

    if command.startswith(prefix):

        query = command[len(prefix):].strip()

        if not query:
            return "What should I search on YouTube?"

        if _search(YOUTUBE_SEARCH, query):
            return f"Searching YouTube for {query}."

        return "Unable to open the browser."

    return None