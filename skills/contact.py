from services.contact_service import contact_service


def handle(command: str):

    command = command.strip()

    # -----------------------------
    # Add Contact
    # Example:
    # add contact arun,+919876543210,arun@gmail.com
    # -----------------------------

    if command.lower().startswith("add contact"):

        try:

            text = command[len("add contact"):].strip()

            parts = [p.strip() for p in text.split(",")]

            name = parts[0]
            phone = parts[1] if len(parts) > 1 else None
            email = parts[2] if len(parts) > 2 else None

            return contact_service.add(
                name,
                phone,
                email,
            )

        except Exception:

            return (
                "Usage:\n"
                "Add contact Arun,+919876543210,arun@gmail.com"
            )

    # -----------------------------
    # Show Contacts
    # -----------------------------

    if command.lower() in (
        "show contacts",
        "list contacts",
        "contacts",
    ):

        return contact_service.list()

    # -----------------------------
    # Find Contact
    # -----------------------------

    if command.lower().startswith("find contact"):

        name = command[len("find contact"):].strip()

        contact = contact_service.get(name)

        if not contact:
            return "Contact not found."

        return (
            f"{name.title()}\n"
            f"Phone : {contact.get('phone','-')}\n"
            f"Email : {contact.get('email','-')}"
        )

    # -----------------------------
    # Delete Contact
    # -----------------------------

    if command.lower().startswith("delete contact"):

        name = command[len("delete contact"):].strip()

        return contact_service.delete(name)

    return None