from fastapi import FastAPI, HTTPException

from api.models import CreateUser, Authorization
from classes.database import Database


def load(app: FastAPI, db: Database) -> None:
    """Charger toutes les CALLS API"""

    @app.get(
        path="/api/user/infos",
        description="Permet de trouver le username sur base de l'ID",
        tags=["USER"]
    )
    async def get_name(user_id: int):
        try:
            return db.call_function(name="get_user_info_by_id", to_json=True, id=user_id)
        except TypeError:
            raise HTTPException(status_code=404, detail=f"{user_id} est soit innexistant soit vide !")
        except Exception as error:
            raise HTTPException(status_code=400, detail=f"Erreur inconnue: {error} !")

    @app.post(
        path="/api/user/create/",
        description="Permet de créer un utilisateurs",
        tags=["user"],
    )
    async def create_user(data: CreateUser):
        user_exist = db.call_function(name="user_exists", username=data.username)
        if user_exist == 0:
            db.call_procedure(
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

    @app.get(
        path="/api/admin/users",
        description="Permet de lister les utilisateurs",
        tags=["ADMIN"],
    )
    async def get_users() -> dict:
        return db.call_function(name="show_members_admin", to_json=True)
