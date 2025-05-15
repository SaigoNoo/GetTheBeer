from typing import Optional, Dict, Any

from pydantic import BaseModel

"""Pour les requests POST, on crée un model, qui coorespond a l'en-tête HTTP a insérer lors du POST"""


class CreateUser(BaseModel):
    f_name: str
    l_name: str
    username: str
    image: str = "https://cdn-icons-png.flaticon.com/512/149/149071.png"
    email: str
    bio: str
    password: str


class Authentification(BaseModel):
    username: str
    password: str


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
