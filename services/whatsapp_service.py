import pywhatkit


class WhatsAppService:

    def send(self, phone, message):

        try:

            pywhatkit.sendwhatmsg_instantly(
                phone_no=phone,
                message=message,
                wait_time=15,
                tab_close=True,
                close_time=3,
            )

            return "WhatsApp message sent."

        except Exception as e:

            return f"WhatsApp Error: {e}"


whatsapp_service = WhatsAppService()