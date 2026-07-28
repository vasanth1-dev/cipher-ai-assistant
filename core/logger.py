import logging
from pathlib import Path


class CipherLogger:

    def __init__(
       self,
    ) -> None:

        log_dir = Path("logs")
        log_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.logger = logging.getLogger("Cipher")

        if self.logger.handlers:
            return

        self.logger.setLevel(logging.DEBUG)

        self.logger.propagate = False

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        file_handler = logging.FileHandler(
            log_dir / "app.log",
            encoding="utf-8"
        )

        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)

        self.logger.addHandler(file_handler)

    def info(
        self, 
        message: str, 
        *args,
    ) -> None:
        self.logger.info(message, *args)

    def warning(
        self, 
        message: str, 
        *args,
    ) -> None:
        self.logger.warning(message, *args)

    def error(
        self, 
        message: str, 
        *args,
    ) -> None:
        self.logger.error(message, *args)

    def debug(
        self, 
        message: str, 
        *args,
    ) -> None:
        self.logger.debug(message, *args)

    def critical(
        self, 
        message: str, 
        *args,
    ) -> None:
        self.logger.critical(message, *args)

    def exception(
            
        self, 
        message: str, 
        *args,
    ) -> None:
        self.logger.exception(message, *args)

logger = CipherLogger()