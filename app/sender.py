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

        # nested try-except for logging purposes
        with smtplib.SMTP(self.server, self.port) as server:
            # Upgrade the connection to a secure encrypted SSL/TLS connection
            if self.use_starttls:
                server.starttls()
                logging.debug("Upgraded connection to STARTTLS")

            try:
                server.login(self.user, self.password)
            except smtplib.SMTPAuthenticationError:
                logging.error(f"Could not login to server {self.server}")
                raise EmailSendException("Could not login to SMTP server")

            logging.debug(f"Logged in to server {self.server}")

            try:
                server.send_message(msg)
            except smtplib.SMTPRecipientsRefused:
                logging.error(f"Could not send email to {to}. Invalid recipient")
                raise EmailSendException("Invalid recipient")
            except smtplib.SMTPException:
                logging.error(f"Could not send email to {to}. Error sending email")
                raise EmailSendException("Could not send email")

            logging.debug(f"Sent email to {to}")
