import json
import os
from threading import Lock

from core.logger import logger


class ContactService:

    def __init__(
       self,
    ) -> None:

        self.file = "data/contacts.json"
        self.lock = Lock()

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.file):

            with open(
                self.file,
                "w",
                encoding="utf-8",
            ) as f:

                json.dump(
                    {},
                    f,
                    indent=4,
                    ensure_ascii=False,
                )

    # --------------------------------------------------
    # Internal
    # --------------------------------------------------

    def load(self):

        with self.lock:

            try:

                with open(
                    self.file,
                    "r",
                    encoding="utf-8",
                ) as f:

                    data = json.load(f)

                    if isinstance(data, dict):
                        return data

            except Exception as e:

                logger.exception(e)

            return {}

    def save(self, contacts):

        with self.lock:

            try:

                with open(
                    self.file,
                    "w",
                    encoding="utf-8",
                ) as f:

                    json.dump(
                        contacts,
                        f,
                        indent=4,
                        ensure_ascii=False,
                        sort_keys=True,
                    )

                logger.info("[CONTACT] Saved.")

            except Exception as e:

                logger.exception(e)

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def add(
        self,
        name,
        phone=None,
        email=None,
    ):

        name = str(name).strip()

        if not name:
            return "Contact name cannot be empty."

        key = name.lower()

        contacts = self.load()

        if key in contacts:
            return f"{name} already exists."

        if phone and not phone.replace("+", "").isdigit():
            return "Invalid phone number."

        if email:
            email = str(email).strip().lower()

        contacts[key] = {
            "phone": phone,
            "email": email,
        }

        self.save(contacts)

        logger.info(
            f"[CONTACT] Added: {name}"
        )

        return f"{name} saved successfully."

    def get(self, name):

        if not name:
            return None

        contacts = self.load()

        return contacts.get(
            str(name).strip().lower()
        )

    def delete(self, name):

        if not name:
            return "Contact name cannot be empty."

        contacts = self.load()

        key = str(name).strip().lower()

        if key not in contacts:
            return "Contact not found."

        contacts.pop(key)

        self.save(contacts)

        logger.info(
            f"[CONTACT] Deleted: {name}"
        )

        return f"Deleted contact: {name}"

    def list(self):

        contacts = self.load()

        if not contacts:
            return "No contacts found."

        result = []

        for name in sorted(contacts):

            info = contacts[name]

            phone = info.get("phone") or "-"
            email = info.get("email") or "-"

            result.append(
                f"{name.title()} | {phone} | {email}"
            )

        return "\n".join(result)

    # --------------------------------------------------
    # Utilities
    # --------------------------------------------------

    def exists(self, name):

        if not name:
            return False

        return (
            str(name).strip().lower()
            in self.load()
        )

    def count(self):

        return len(self.load())

    def clear(self):

        self.save({})

        logger.info("[CONTACT] Cleared.")


contact_service = ContactService()