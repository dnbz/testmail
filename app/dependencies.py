from app.sender import SmtpEmailSender
from app.settings import SMTP_SERVER, SMTP_SENDER_EMAIL, SMTP_ENABLE_STARTTLS, SMTP_PASSWORD, \
    SMTP_USER, SMTP_PORT


async def get_email_sender() -> SmtpEmailSender:
    return SmtpEmailSender(
        server=SMTP_SERVER,
        port=SMTP_PORT,
        user=SMTP_USER,
        password=SMTP_PASSWORD,
        use_starttls=SMTP_ENABLE_STARTTLS,
        sender_email=SMTP_SENDER_EMAIL)
