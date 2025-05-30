from os import getenv
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from classes.env import entry
from starlette.middleware.sessions import SessionMiddleware

from api import start
from classes.debug import Debug

app = FastAPI()
debug = Debug()
load_dotenv()

debug.print(text="Mode debug: ACTIF")

secret_key = getenv(key="SECRET_KEY")
if secret_key is None or secret_key == "":
    secret_key = uuid4()
    debug.print(app_module="SecretKey", text=f"Pas de SECRET_KEY, génération de la clé: {secret_key}...")
    data = entry()
    data["SECRET_KEY"] = secret_key
    entry(data=data, read_mode=False)

debug.print(app_module="Secretkey", text="Middleware déclaré !")

app.add_middleware(
    SessionMiddleware,
    secret_key=secret_key
)

debug.print(
    app_module="CORS",
    text=f"Autorisation données à {getenv(key='CORS_URL')}..."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        str(getenv(key="CORS_URL"))
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

start(app=app, debug=debug)
