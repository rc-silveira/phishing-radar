from pydantic import BaseModel


class EmailInput(BaseModel):
    email: str
    subject: str
    body: str
