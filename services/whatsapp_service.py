import re

from core.logger import logger


class WhatsAppService:

    # --------------------------------------------------
    # Send WhatsApp Message
    # --------------------------------------------------

    def send(
        self,
        phone,
        message,
    ):

        phone = str(phone).strip()
        message = str(message).strip()

        if not phone:
            return "Phone number cannot be empty."

        if not message:
            return "Message cannot be empty."

        phone = phone.replace(" ", "")

        if not re.fullmatch(r"\+\d{8,15}", phone):
            return (
                "Invalid phone number. "
                "Use international format "
                "like +919876543210."
            )

        try:

            import pywhatkit

            pywhatkit.sendwhatmsg_instantly(
                phone_no=phone,
                message=message,
                wait_time=15,
                tab_close=True,
                close_time=3,
            )

            logger.info(
                f"[WHATSAPP] Message sent to {phone}"
            )

            return "WhatsApp message sent."

        except Exception as e:

            logger.exception(e)

            return (
                "Unable to send the WhatsApp message."
            )


whatsapp_service = WhatsAppService()