from services.vision_service import vision_service


def handle(command: str):

    if not command:
        return None

    command = command.lower().strip()

    if command in (
        "open camera",
        "take photo",
        "take picture",
        "capture image",
        "capture photo",
    ):

        image = vision_service.capture()

        if image:
            return f"Photo captured successfully. Saved to {image}"

        return "Unable to access the camera."

    return None