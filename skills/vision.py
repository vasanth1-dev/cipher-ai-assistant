from services.vision_service import vision_service

INTENT = "camera"
def handle(command: str):

    if not command:
        return None

    command = command.lower().strip()

    if command in (
        "open camera",
        "camera",
        "take photo",
        "take picture",
        "capture image",
        "capture photo",
        "capture",
        "take selfie",
        "click photo",
        "click picture",
    ):

        image = vision_service.capture()

        if image:
            return (
                "Photo captured successfully.\n"
                 f"Saved to:\n{image}"
            )

        return "Unable to access the camera."

    return None