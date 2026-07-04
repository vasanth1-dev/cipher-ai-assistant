from services.screen_service import screen_service
from services.ocr_service import ocr_service


class ScreenAIService:

    def read_screen(self):

        image = screen_service.capture()

        if not image:
            return "Unable to capture the screen."

        text = ocr_service.read(image)

        if not text or text == "No text found.":
            return "I couldn't find any readable text on your screen."

        return text


screen_ai_service = ScreenAIService()