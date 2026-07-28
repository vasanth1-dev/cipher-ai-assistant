import mss
from PIL import Image
from pathlib import Path


class ScreenService:

    def __init__(
       self,
    ) -> None:

        self.output_dir = Path("data/screens")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def capture(self, filename="screen.png"):

        path = self.output_dir / filename

        with mss.mss() as sct:

            monitor = sct.monitors[1]

            screenshot = sct.grab(monitor)

            image = Image.frombytes(
                "RGB",
                screenshot.size,
                screenshot.rgb,
            )

            image.save(path)

        return str(path)


screen_service = ScreenService()