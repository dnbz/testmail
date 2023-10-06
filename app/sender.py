import logging
import smtplib
from email.message import EmailMessage


class EmailSendException(Exception):
    pass


class SmtpEmailSender:
    def __init__(self, server: str, user: str, password: str, port: int, sender_email: str,
                 use_starttls: bool):
        self.server = server
        self.user = user
        self.password = password
        self.port = port
        self.sender_email = sender_email
        self.use_starttls = use_starttls

    def send_mail(self, to: str, subject: str, message: str):
        msg = EmailMessage()
        msg.set_content(message)
        msg['Subject'] = subject
        msg['From'] = self.sender_email
        msg['To'] = to

        # Send the email
        try:
            with smtplib.SMTP(self.server, self.port) as server:
                # Upgrade the connection to a secure encrypted SSL/TLS connection
                if self.use_starttls:
                    server.starttls()

                server.login(self.user, self.password)
                logging.debug(f"Logged in to server {self.server}")
                server.send_message(msg)

        except Exception as e:
            raise EmailSendException(f"Error sending email: {e}")
