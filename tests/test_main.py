# test_main.py
from smtplib import SMTPAuthenticationError, SMTPRecipientsRefused, SMTPException
from unittest.mock import patch, Mock

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# Create a mock that can be used with the 'with' statement
class MockSMTP:
    def __init__(self, *args, **kwargs):
        self.instance = Mock()

    def __call__(self, *args, **kwargs):
        return self

    def __enter__(self):
        return self.instance

    def __exit__(self, exc_type, exc_value, traceback):
        pass


def mock_send_mail_success(*args, **kwargs):
    return None  # Just mock a success without doing anything


def mock_send_mail_failure(*args, **kwargs):
    raise Exception("Some error occurred")


@patch("app.sender.SmtpEmailSender.send_mail", side_effect=mock_send_mail_success)
def test_send_email_success(mocked_send_mail):
    response = client.post(
        "/send_email",
        json={
            "to": "test@example.com",
            "subject": "Test subject",
            "message": "Test message"
        }
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Email sent successfully"}


@patch("app.sender.SmtpEmailSender.send_mail", side_effect=mock_send_mail_failure)
def test_send_email_validation_failure(mocked_send_mail):
    response = client.post(
        "/send_email",
        json={
            "to": "test#example",
            "subject": "Test subject",
            "message": "Test message"
        }
    )
    assert response.status_code == 422


def mock_raise_smtp_auth_error(*args, **kwargs):
    raise SMTPAuthenticationError(535, "Authentication failed")


def mock_raise_smtp_recipients_refused(*args, **kwargs):
    raise SMTPRecipientsRefused({"test@example.com": (550, "User unknown")}) # noqa


def mock_raise_smtp_exception(*args, **kwargs):
    raise SMTPException()


@patch("smtplib.SMTP", new_callable=MockSMTP)
def test_send_email_smtp_auth_error(mocked_smtp):
    mocked_smtp.instance.login.side_effect = mock_raise_smtp_auth_error

    response = client.post(
        "/send_email",
        json={
            "to": "test@example.com",
            "subject": "Test subject",
            "message": "Test message"
        }
    )
    assert response.status_code == 400
    assert "Could not login to SMTP server" in response.json().get("detail")


@patch("smtplib.SMTP", new_callable=MockSMTP)
def test_send_email_recipients_refused(mocked_smtp):
    mocked_smtp.instance.send_message.side_effect = mock_raise_smtp_recipients_refused

    response = client.post(
        "/send_email",
        json={
            "to": "test@example.com",
            "subject": "Test subject",
            "message": "Test message"
        }
    )
    assert response.status_code == 400
    assert "Invalid recipient" in response.json().get("detail")


@patch("smtplib.SMTP", new_callable=MockSMTP)
def test_send_email_smtp_exception(mocked_smtp):
    mocked_smtp.instance.send_message.side_effect = mock_raise_smtp_exception

    response = client.post(
        "/send_email",
        json={
            "to": "test@example.com",
            "subject": "Test subject",
            "message": "Test message"
        }
    )
    assert response.status_code == 400
    assert "Could not send email" in response.json().get("detail")
