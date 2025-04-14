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
