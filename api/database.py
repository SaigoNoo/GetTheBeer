from fastapi import FastAPI
from classes.database import Database


def load(app: FastAPI, db: Database) -> None:
    """Charger toutes les CALLS API"""

    @app.get(
        path="/api/db/test",
        description="Permet d'obtenir une confirmation de l'accès a la base de donnée",
        tags=["db"]
    )
    async def db_test() -> str:
        return db.call(ctype="func", name="test_api")
