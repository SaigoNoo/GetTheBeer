from uuid import uuid4

from fastapi import FastAPI, HTTPException

from api.models import CreateUser, ResetEmailRequest
from classes.database import Database
from classes.mail import Mail


class Users:
    def __init__(self, db: Database):
        self.reset_password_pool = {
        }
        self.db = db

    def get_email_from_username(self, username: str):
        if self.db.call_function(name="user_exists", username=username) == 1:
            id_u = self.db.call_function(name="id_of_user", username=username)
            return self.db.call_function(name="get_user_info_by_id", to_json=True, id=id_u)["email"]

    @staticmethod
    def generate_token():
        return uuid4()

    def ask_reset(self, email: str):
        if self.db.call_function(name="user_exists", email_username=email):
            if "@" not in email:
                email = self.get_email_from_username(username=email)
            Mail(receiver=email, title="Demande de reset", body="VOILA").send()
        else:
            return False

    def reset_password(self, username: str, token: str):
        pass

    def get_user_infos(self, user_id: int):
        try:
            return self.db.call_function(name="get_user_info_by_id", to_json=True, id=user_id)
        except TypeError:
            raise HTTPException(status_code=404, detail=f"{user_id} est soit innexistant soit vide !")
        except Exception as error:
            raise HTTPException(status_code=400, detail=f"Erreur inconnue: {error} !")

    def create_user(self, data: CreateUser):
        user_exist = self.db.call_function(name="user_exists", username=data.username)
        if user_exist == 0:
            self.db.call_procedure(
                name="create_user",
                user=data.username,
                password=data.password,
                avatar=data.url_avatar,
                last_name=data.last_name,
                first_name=data.first_name,
                email=data.email,
                is_admin=1 if data.is_admin else 0
            )
            return {
                "message": "Utilisateur crée avec succès !"
            }
        else:
            raise HTTPException(status_code=405, detail=f"{data.username} existe déjà !")

    def list_members(self):
        return self.db.call_function(name="show_members_admin", to_json=True)


def load(app: FastAPI, db: Database) -> None:
    """
    Charger toutes les CALLS API
    """
    user = Users(db=db)

    @app.get(
        path="/api/user/infos",
        description="Permet de trouver le username sur base de l'ID",
        tags=["USER"]
    )
    async def get_name(user_id: int):
        return user.get_user_infos(user_id=user_id)

    @app.post(
        path="/api/user/create/",
        description="Permet de créer un utilisateurs",
        tags=["user"],
    )
    async def create_user(data: CreateUser):
        return user.create_user(data=data)

    @app.get(
        path="/api/admin/users",
        description="Permet de lister les utilisateurs",
        tags=["ADMIN"],
    )
    async def get_users() -> list or None:
        return user.list_members()

    @app.post(
        path="/api/user/reset_password_request",
        description="Demander un reset du mot de passe !",
        tags=["USER"]
    )
    async def reset_password_request(data: ResetEmailRequest):
        return user.ask_reset(email=data.email)
