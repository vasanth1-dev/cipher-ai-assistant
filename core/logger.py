import logging
from pathlib import Path


class CipherLogger:

    def __init__(self):

        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        self.logger = logging.getLogger("Cipher")

        if self.logger.handlers:
            return

        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        file_handler = logging.FileHandler(
            log_dir / "app.log",
            encoding="utf-8"
        )

        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def info(self, message, *args):
        self.logger.info(message, *args)

    def warning(self, message, *args):
        self.logger.warning(message, *args)

    def error(self, message, *args):
        self.logger.error(message, *args)

    def debug(self, message, *args):
        self.logger.debug(message, *args)

    def critical(self, message, *args):
        self.logger.critical(message, *args)

    def exception(self, message, *args):
        self.logger.exception(message, *args)

logger = CipherLogger()