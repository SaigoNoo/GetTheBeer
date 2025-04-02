from uuid import uuid4

from fastapi import FastAPI, HTTPException

from api.models import CreateUser, ResetEmailRequest
from classes.database import Database
from classes.mail import Mail


class Users:
    def __init__(self, db: Database):
        self.db = db

    def get_email_from_username_or_email(self, username: str):
        if self.db.call_function(name="user_exists", username=username) == 1:
            id_u = self.db.call_function(name="id_of_user", username=username)
            return self.db.call_function(name="get_user_info_by_id", to_json=True, id=id_u)["email"]

    @staticmethod
    def generate_token():
        return uuid4()

    def ask_reset(self, email: str):
        if self.db.call_function(name="user_exists", email_username=email):
            id_u = self.db.call_function(name="id_of_user", email_username=email)
            if "@" not in email:
                email = self.get_email_from_username_or_email(username=email)
            if not self.db.call_function(name="is_active_token", id=id_u) == 1:
                url_reset = f"https://localhost:8000/api/reset/token/{id_u}"
                message = ("Vous avez fait une demande réinitialisation de mot de passe.\n"
                           f"Rendez vous sur {url_reset}\n")
                Mail(receiver=email, title="Demande de reset", body=message).send()
                return "Un mail à été envoyé si votre compte existe !"
            else:
                return "Une demande a déjà été effectuée, veuillez patienter 15min à compter du premier reset !"
        else:
            return "Erreur ou compte inconnu !"

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
                "message": "Utilisateur créé avec succès !"
            }
        else:
            raise HTTPException(status_code=405, detail=f"{data.username} existe déjà !")

    def list_members(self):
        return self.db.call_function(name="show_members_admin", to_json=True)

    def login_user(self, username: str, password: str):
        user_exist = self.db.call_function(name="user_exists", username=username)
        if user_exist == 1:
            stored_password = self.db.call_function(name="get_user_password", username=username)
            if stored_password == password:  # Faudra faire gaffe à hacher pour la sécurité
                return {"message": "Connexion réussie !"}
        raise HTTPException(status_code=401, detail="Identifiants incorrects")

    def add_friend(self, user_id: int, friend_id: int):
        if self.db.call_function(name="user_exists", id=friend_id) == 1:
            if self.db.call_function(name="is_friend", id=user_id, friend_id=friend_id) == 0:
                self.db.call_procedure(name="add_friend", user_id=user_id, friend_id=friend_id)
                return {"message": "Ami ajouté avec succès !"}
            else:
                raise HTTPException(status_code=405, detail=f"{friend_id} est déjà dans votre liste d'amis !")
        else:
            raise HTTPException(status_code=404, detail=f"{friend_id} est soit innexistant soit vide !")

    def delete_friend(self, user_id: int, friend_id: int):
        if self.db.call_function(name="user_exists", id=friend_id) == 1:
            if self.db.call_function(name="is_friend", id=user_id, friend_id=friend_id) == 1:
                self.db.call_procedure(name="delete_friend", user_id=user_id, friend_id=friend_id)
                return {"message": "Ami supprimé avec succès !"}
            else:
                raise HTTPException(status_code=405, detail=f"{friend_id} n'est pas dans votre liste d'amis !")
        else:
            raise HTTPException(status_code=404, detail=f"{friend_id} est soit innexistant soit vide !")


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

    @app.get(
        path="/api/admin/users",
        description="Permet de lister les utilisateurs",
        tags=["ADMIN"],
    )

    @app.post(
        path="/api/user/create/",
        description="Permet de créer un utilisateurs",
        tags=["user"],
    )
    async def create_user(data: CreateUser):
        return user.create_user(data=data)

    async def get_users() -> list or None:
        return user.list_members()

    @app.post(
        path="/api/user/reset_password_request",
        description="Demander un reset du mot de passe !",
        tags=["USER"]
    )
    async def reset_password_request(data: ResetEmailRequest):
        return user.ask_reset(email=data.email)

    @app.post(
        path="/api/user/login/",
        description="Connexion d'un utilisateur",
        tags=["USER"]
    )
    async def login(username: str, password: str):
        return user.login_user(username=username, password=password)

    @app.post(
    path="/api/user/add_friend/",
    description="Permet d'ajouter un ami",
    tags=["USER"]
    )
    async def add_friend(user_id: int, friend_id: int):
        return user.add_friend(user_id=user_id, friend_id=friend_id)
 
    @app.post(
    path="/api/user/delete_friend/",
    description="Permet de supprimer un ami",
    tags=["USER"]
    )
    async def delete_friend(user_id: int, friend_id: int):
        return user.delete_friend(user_id=user_id, friend_id=friend_id)