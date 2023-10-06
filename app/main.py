import logging

from fastapi import FastAPI, Depends, HTTPException

from app.dependencies import get_email_sender
from app.models import EmailSendRequest, EmailSendResponse
from app.sender import SmtpEmailSender, EmailSendException

app = FastAPI()


@app.post("/send_email")
async def send_email(request: EmailSendRequest,
                     sender: SmtpEmailSender = Depends(get_email_sender)) -> EmailSendResponse:
    logging.info(f"Sending email to {request.to} with subject {request.subject}")

    try:
        sender.send_mail(to=request.to, subject=request.subject, message=request.message)
    except EmailSendException as e:
        logging.error(f"Error sending mail: {e}")
        raise HTTPException(status_code=400, detail=f"Email could not be sent: {e}")
    # Catch all other exceptions but don't expose them to the user
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

    return EmailSendResponse(
        message="Email sent successfully"
    )
