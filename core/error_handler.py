import logging
from pathlib import Path


class ErrorHandler:

    def __init__(self):

        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        logging.basicConfig(
            filename=log_dir / "error.log",
            level=logging.ERROR,
            format="%(asctime)s | %(levelname)s | %(message)s",
        )

    def handle(self, error, context=""):

        logging.exception(f"{context} : {error}")

        return "Sorry, something went wrong."


error_handler = ErrorHandler()