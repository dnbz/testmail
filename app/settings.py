import os

SMTP_SERVER = os.environ.get("SMTP_SERVER")
SMTP_PORT = os.environ.get("SMTP_PORT")
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_ENABLE_STARTTLS = os.environ.get("SMTP_ENABLE_STARTTLS")
SMTP_SENDER_EMAIL = os.environ.get("SMTP_SENDER_EMAIL")
