import cv2
from pathlib import Path


class VisionService:

    def __init__(self):
        self.output_dir = Path("data/images")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def capture(self, filename="capture.jpg"):

        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            return None

        success, frame = camera.read()

        camera.release()

        if not success:
            return None

        image_path = self.output_dir / filename

        cv2.imwrite(str(image_path), frame)

        return str(image_path)


vision_service = VisionService()