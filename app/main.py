import logging

from fastapi import FastAPI, Depends, HTTPException

from app.dependencies import get_email_sender
from app.models import EmailSendRequest, EmailSendResponse
from app.sender import SmtpEmailSender

app = FastAPI()


@app.post("/send_email")
async def send_email(request: EmailSendRequest,
                     sender: SmtpEmailSender = Depends(get_email_sender)) -> EmailSendResponse:
    logging.info(f"Sending email to {request.to} with subject {request.subject}")

    try:
        sender.send_mail(to=request.to, subject=request.subject, message=request.message)
    except Exception as e:
        logging.error(f"Couldn't send mail: {e}")
        raise HTTPException(status_code=200, detail="Email could not be sent")

    return EmailSendResponse(
        message="Email sent successfully"
    )
