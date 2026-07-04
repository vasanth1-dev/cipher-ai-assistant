import subprocess


class BrowserService:

    def open(self, url: str):

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


browser_service = BrowserService()