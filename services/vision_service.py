from pathlib import Path

import cv2

from core.logger import logger


class VisionService:

    def __init__(self):

        self.output_dir = Path("data/images")

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    # --------------------------------------------------
    # Capture Image
    # --------------------------------------------------

    def capture(
        self,
        filename="capture.jpg",
    ):

        filename = str(filename).strip()

        if not filename:
            filename = "capture.jpg"

        image_path = self.output_dir / filename

        camera = None

        try:

            camera = cv2.VideoCapture(0)

            if not camera.isOpened():

                logger.warning(
                    "[VISION] Camera could not be opened."
                )

                return None

            success, frame = camera.read()

            if not success:

                logger.warning(
                    "[VISION] Failed to capture image."
                )

                return None

            cv2.imwrite(
                str(image_path),
                frame,
            )

            logger.info(
                f"[VISION] Image saved: {image_path}"
            )

            return str(image_path)

        except Exception as e:

            logger.exception(e)

            return None

        finally:

            if camera is not None:

                camera.release()


vision_service = VisionService()