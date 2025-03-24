from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from classes.database import Database


def load(app: FastAPI, db: Database) -> None:
    """Charger toutes les CALLS API"""

    @app.get(
        path="/api/db/test",
        description="Permet d'obtenir une confirmation de l'accès a la base de donnée",
        tags=["DATABASE"]
    )
    async def db_test():
        return db.call_function(name="test_api")
