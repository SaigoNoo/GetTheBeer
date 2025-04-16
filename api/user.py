from fastapi import FastAPI

from api.models import CreateUser, ResetEmailRequest, ResetEmailResponse
from classes.database import Database
from classes.users import UsersAPI


def load(app: FastAPI, db: Database) -> None:
    """
    Charger toutes les CALLS API
    """
    user = UsersAPI(db=db)

    @app.post(
        path="/api/user/create/",
        description="Permet de créer un utilisateurs",
        tags=["USER"],
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

    @app.post(
        path="/api/user/reset_password",
        description="Reset le mot de passe",
        tags=["USER"]
    )
    async def reset_password(data: ResetEmailResponse):
        pass

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

    @app.post(                      #il fallait ajouter un truc dans un autre file pour les post mais jsais plus quoi ....
    path="/api/user/delete_friend/",
    description="Permet de supprimer un ami",
    tags=["USER"]
    )
    async def delete_friend(user_id: int, friend_id: int):
        return user.delete_friend(user_id=user_id, friend_id=friend_id)

    @app.get(
    path="/api/user/level",
    description="Récupère le niveau et le titre d'un utilisateur",
    tags=["USER"]
    )
    async def get_user_level(user_id: int):
        return user.get_user_level(user_id)