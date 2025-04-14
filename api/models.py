from pydantic import BaseModel

"""Pour les requests POST, on crée un model, qui coorespond a l'en-tête HTTP a insérer lors du POST"""


class CreateUser(BaseModel):
    l_name: str
    f_name: str
    username: str
    mail: str
    image: bytes
    password: str
    bio: str
    desc: str


class DeleteUser(BaseModel):
    username: str
    password: str
    email: str


class Authorization(BaseModel):
    email: str
    password: str
    token: str


class ResetEmailRequest(BaseModel):
    email: str


class ResetEmailResponse(BaseModel):
    token: str
    password: str
