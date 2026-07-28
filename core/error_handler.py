import logging
from pathlib import Path


class ErrorHandler:

    def __init__(
       self,
    ) -> None:

        log_dir = Path("logs")
        log_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.logger = logging.getLogger("CipherError")

        if not self.logger.handlers:

            handler = logging.FileHandler(
                log_dir / "error.log",
                encoding="utf-8",
            )

            handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s | %(levelname)s | %(message)s"
                )
            )

            self.logger.setLevel(logging.ERROR)
            self.logger.addHandler(handler)

    def handle(
        self, 
        error: Exception, 
        context: str = "",
    ) ->str:

        self.logger.exception(
            "%s: %s",
            context,
            error,
        )

        return "Sorry, something went wrong."


error_handler = ErrorHandler()