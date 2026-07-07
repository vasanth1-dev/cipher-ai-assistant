import json
import os


class ContactService:

    def __init__(self):

        self.file = "data/contacts.json"

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.file):
            with open(self.file, "w") as f:
                json.dump({}, f, indent=4)

    def load(self):

        with open(self.file, "r") as f:
            return json.load(f)

    def save(self, contacts):

        with open(self.file, "w") as f:
            json.dump(contacts, f, indent=4)

    def add(self, name, phone=None, email=None):

        contacts = self.load()

        contacts[name.lower()] = {
            "phone": phone,
            "email": email,
        }

        self.save(contacts)

        return f"{name} saved successfully."

    def get(self, name):

        contacts = self.load()

        return contacts.get(name.lower())

    def delete(self, name):

        contacts = self.load()

        if name.lower() not in contacts:
            return "Contact not found."

        del contacts[name.lower()]

        self.save(contacts)

        return "Contact deleted."

    def list(self):

        contacts = self.load()

        if not contacts:
            return "No contacts found."

        result = []

        for name, info in contacts.items():

            phone = info.get("phone") or "-"
            email = info.get("email") or "-"

            result.append(
                f"{name.title()} | {phone} | {email}"
            )

        return "\n".join(result)


contact_service = ContactService()