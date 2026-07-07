from services.whatsapp_service import whatsapp_service


def handle(command):

    command = command.lower().strip()

    if not command.startswith("send whatsapp"):
        return None

    try:

        text = command.replace(
            "send whatsapp",
            "",
            1,
        ).strip()

        phone, message = text.split(",", 1)

        return whatsapp_service.send(
            phone.strip(),
            message.strip(),
        )

    except Exception:

        return (
            "Use:\n"
            "Send WhatsApp +916380905096, Hello"
        )