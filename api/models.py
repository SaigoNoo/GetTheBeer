from pydantic import BaseModel

"""Pour les requests POST, on crée un model, qui coorespond a l'en-tête HTTP a insérer lors du POST"""


class CreateUser(BaseModel):
    username: str
    first_name: str = None
    last_name: str = None
    password: str
    email: str
    card_id: str


class DeleteUser(BaseModel):
    username: str
    password: str
    email: str


class Authorization(BaseModel):
    email: str
    password: str
