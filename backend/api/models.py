from pydantic import BaseModel

"""Pour les requests POST, on crée un model, qui coorespond a l'en-tête HTTP a insérer lors du POST"""


class CreateUser(BaseModel):
    username: str
    password: str
    url_avatar: str
    last_name: str
    first_name: str
    email: str
    is_admin: bool = False


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
    email: str
    new_password: str
    confirm_password: str
