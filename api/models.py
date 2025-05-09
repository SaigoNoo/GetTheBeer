from typing import Optional, Dict, Any

from pydantic import BaseModel

"""Pour les requests POST, on crée un model, qui coorespond a l'en-tête HTTP a insérer lors du POST"""


class CreateUser(BaseModel):
    l_name: str
    f_name: str
    username: str
    email: str
    image: bytes
    password: str
    bio: str


class DeleteUser(BaseModel):
    username: str
    password: str
    email: str


class Authorization(BaseModel):
    email: str
    password: str
    token: str


class ResetEmailResponse(BaseModel):
    token: str
    password: str


class SendMail(BaseModel):
    email: str
    subject: str
    file: str
    extra: Optional[Dict[str, Any]] = {}


class RequestPasswordReset(BaseModel):
    username: str
