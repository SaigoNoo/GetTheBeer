from fastapi import FastAPI

from api.models import CreateUser, Authorization


def load(app: FastAPI) -> None:
    """Charger toutes les CALLS API"""
    @app.get(
        path="/api/user/name_id/{id}",
        description="Permet de trouver le username sur base de l'ID",
        tags=["user"]
    )
    async def get_name(id: str) -> None:
        return ""

    @app.post(
        path="/api/user/create/",
        description="Permet de créer un utilisateurs",
        tags=["user"],
    )
    async def create_user(data: CreateUser, auth: Authorization):
        return {"message": "Item créé avec succès", "item": data}
