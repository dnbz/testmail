from pydantic import BaseModel, EmailStr


class EmailSendRequest(BaseModel):
    # use pydantic email validator
    to: EmailStr
    subject: str
    message: str


class EmailSendResponse(BaseModel):
    message: str
