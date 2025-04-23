from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import start
from classes.debug import Debug

app = FastAPI()
debug = Debug()

debug.print(text="Mode debug: ACTIF")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

debug.print(app_module="FastAPI", text="CORS Authorization")
start(app=app, debug=debug)
debug.print(app_module="FastAPI", text="Démarrage...")
