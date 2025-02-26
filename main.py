from os.path import exists

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mysql.connector import connect, Error


class Validation:
    @staticmethod
    def master_login_valid(password: str) -> bool:
        return Env().get_value(key="BACKEND_MASTER_PASSWORD") == password

    @staticmethod
    def have_master_password() -> bool:
        return "BACKEND_MASTER_PASSWORD" in Env().get_value()

    @staticmethod
    def env_exist() -> bool:
        return exists(".env")


class Env:
    def __init__(
            self,
            server=None,
            username=None,
            password=None,
            dbname=None,
            port=None
    ):
        self.server = "localhost" if server == "" else server
        self.username = username
        self.password = password
        self.dbname = dbname
        self.port = "3306" if port == "" else port

    def store_values(self, master_password: str):
        temp = (
            f"DB_SERVER={self.server}\n"
            f"DB_USERNAME={self.username}\n"
            f"DB_PASSWORD={self.password}\n"
            f"DB_NAME={self.dbname}\n"
            f"DB_PORT={self.port}\n"
            f"BACKEND_MASTER_PASSWORD={master_password}"
        )
        with open(file=".env", mode="w", encoding="utf-8") as env:
            return env.write(temp)

    def set_master_password(self, password: str):
        datas = self.get_value()
        text = ""
        datas["BACKEND_MASTER_PASSWORD"] = password
        for element in datas:
            text += f"{element}={datas[element]}\n"
        text = text[:-1]
        with open(file=".env", mode="w", encoding="utf-8") as env:
            env.write(text)

    @staticmethod
    def get_value(key: str = None):
        temp = {}
        with open(file=".env", mode="r", encoding="utf-8") as env:
            for line in env.readlines():
                key_dict, value_dict = line.strip().split("=")
                temp[key_dict.strip()] = value_dict.strip()
        return temp if key is None else temp[key]


class Database:
    def __init__(self):
        self.socket = None
        self.__cursor = None

    def connect(self):
        print(f" > Tentative de connexion avec {Env().get_value(key='DB_USERNAME')}@{Env().get_value(key='DB_SERVER')}")
        try:
            connection = connect(
                host=Env().get_value(key="DB_SERVER"),
                user=Env().get_value(key="DB_USERNAME"),
                password=Env().get_value(key="DB_PASSWORD"),
                database=Env().get_value(key="DB_NAME"),
                port=Env().get_value(key="DB_PORT")
            )
            print(
                f" > Connecté à {Env().get_value('DB_NAME')} "
                f"via {Env().get_value('DB_USERNAME')}@{Env().get_value('DB_SERVER')}")
            self.socket = connection
            self.__cursor = connection.cursor()
            return True
        except Error as err:
            print(f" > {err}")
        except KeyError as err:
            print(f" > Erreur de clé: {err} n'existe pas dans .env ou le champ est vide !")

    def login_valid(self, username: str, password: str):
        response = {}
        self.__cursor.execute("SELECT username, password FROM `gtb_users` WHERE username = %s;", (username,))
        rows = self.__cursor.fetchall()
        if len(rows) > 0:
            if rows[0][1] == password:
                response["success"] = True
                response["message"] = "Connexion avec succès..."
            else:
                response["success"] = False
                response["message"] = "Les identifiants sont erronés !"
        else:
            response["success"] = False
            response["message"] = "Les identifiants sont erronés !"

        return response


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Autorise tous les headers
)

valid = Validation()

if not valid.env_exist():
    Env().store_values(master_password="getthebeer")

if valid.env_exist() and valid.have_master_password():
    db = Database()
    db.connect()


# API Calls
@app.get(
    path="/admin/env/set",
    tags=["Admin | Env"]
)
async def env_set(
        username: str,
        password: str,
        database: str,
        master_password: str,
        port: str = "3306",
        server: str = "localhost"
):
    response = {}
    if valid.have_master_password() and valid.master_login_valid(password=master_password):
        response["success"] = True
        response["message"] = f"Le .env a bien été modifié !"
        Env(
            server=server,
            username=username,
            password=password,
            dbname=database,
            port=port
        ).store_values(master_password=master_password)
    else:
        response["success"] = False
        response["message"] = "Le MASTER_PASSWORD est erroné, vide où n'a pas été déclaré !"
    return response


@app.get(
    path="/admin/env/change_master_password",
    tags=["Admin | Env"]
)
async def change_passwd(old_password: str, new_password, confirm_password: str):
    response = {}
    # Si le nouveau mot de passe est vide
    if len(new_password) == 0:
        response["success"] = False
        response["message"] = "Le nouveau mot de passe est vide ! Valeur obligatoire !"

    # Si l'ancien mot de passe est validé
    if valid.master_login_valid(password=old_password):
        if new_password == confirm_password:
            response["success"] = True
            response["message"] = "Le MASTER PASSWORD a bien été modifié !"
            Env().set_master_password(password=new_password)
        else:
            response["success"] = False
            response["message"] = "Le nouveau mot de passe n'est pas le même qu'a la confirmation !"
    else:
        response["success"] = False
        response["message"] = "L'ancien master password est incorrect !"
    return response


# A CHANGER: Passer en mode POST pour utiliser LoginRequest par question de sécurité
"""
La fonction try_login() utilise fetch() pour envoyer des données à l’API, mais elle a plusieurs problèmes :
Les données sensibles (password) sont envoyées en GET → Mauvaise pratique car elles peuvent être stockées dans les logs du serveur ou visibles dans l'URL.
Aucune gestion de réponse → One ne sait pas si le serveur a bien reçu la requête ou s'il y a une erreur.
Il faut utiliser POST avec JSON pour la sécurité.
"""


@app.get(
    path="/api/login",
    tags=["Core"]
)
async def login(username: str, password: str):
    return db.login_valid(username=username, password=password)
