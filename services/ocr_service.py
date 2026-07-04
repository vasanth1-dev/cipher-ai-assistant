import pytesseract
from PIL import Image


class OCRService:

    def read(self, image_path):

        try:

            image = Image.open(image_path)

            text = pytesseract.image_to_string(image)

            text = text.strip()

            if text:
                return text

            return "No text found."

        except Exception as e:
            return f"OCR Error: {e}"


ocr_service = OCRService()