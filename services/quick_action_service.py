import subprocess

from core.logger import logger


class QuickActionService:

    # ------------------------------------------

    def terminal(self):

        return self._launch(
            ["gnome-terminal"],
            "Opening Terminal.",
        )

    # ------------------------------------------

    def browser(self):

        return self._launch(
            ["firefox"],
            "Opening Browser.",
        )

    # ------------------------------------------

    def files(self):

        return self._launch(
            ["nautilus"],
            "Opening Files.",
        )

    # ------------------------------------------

    def settings(self):

        return self._launch(
            ["gnome-control-center"],
            "Opening Settings.",
        )

    # ------------------------------------------

    def _launch(
        self,
        command,
        success_message,
    ):

        try:

            subprocess.Popen(command)

            return success_message

        except Exception as e:

            logger.exception(e)

            return "Unable to launch application."


quick_action_service = QuickActionService()