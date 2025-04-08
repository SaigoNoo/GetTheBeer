from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from classes.database import Database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def load(app: FastAPI, db: Database) -> None:
    """Charger toutes les CALLS API"""

    @app.get(
        path="/api/db/test",
        description="Permet d'obtenir une confirmation de l'accès a la base de donnée",
        tags=["DATABASE"]
    )
    async def db_test():
        return db.call_function(name="test_api")
    

# URL de connexion à la base de données MariaDB
SQLALCHEMY_DATABASE_URL = "mariadb+mariadbconnector://myuser:mypassword@localhost/mydatabase"

# Créer une instance d'un moteur SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=10, max_overflow=20)

# Créer une session qui te permet d'interagir avec la base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Déclarative Base qui te permet de définir tes modèles de tables
Base = declarative_base()

# database.py
from sqlalchemy.orm import Session

# Fonction pour obtenir une session de base de données
def get_db():
    db = SessionLocal()  # Créer une session
    try:
        yield db  # Retourner la session pour utilisation
    finally:
        db.close()  # Fermer la session une fois l'opération terminée

