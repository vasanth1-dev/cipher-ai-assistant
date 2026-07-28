import smtplib
from email.message import EmailMessage
import os


class EmailService:

    def __init__(
       self,
    ) -> None:

        self.sender = os.getenv("EMAIL_ADDRESS")
        self.password = os.getenv("EMAIL_PASSWORD")

    def send(self, receiver, subject, body):

        if not self.sender or not self.password:
            return "Email is not configured."

        try:

            msg = EmailMessage()

            msg["Subject"] = subject
            msg["From"] = self.sender
            msg["To"] = receiver

            msg.set_content(body)

            with smtplib.SMTP_SSL(
                "smtp.gmail.com",
                465,
            ) as smtp:

                smtp.login(
                    self.sender,
                    self.password,
                )

                smtp.send_message(msg)

            return "Email sent successfully."

        except Exception as e:

            return f"Email Error: {e}"


email_service = EmailService()