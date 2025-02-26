from argparse import ArgumentParser
from os.path import exists

from fastapi import FastAPI
from mysql.connector import connect, Error

# ARGS
arg = ArgumentParser()
arg.add_argument("-me", "--make-env", action="store_true", help="Créer un fichier .env")
arg.add_argument("-ei", "--env-intuitive", action="store_true", help="Remplir le .env depuis ici...")
arg = arg.parse_args()


def press_exit():
    input(" > Pressez Enter pour continuer...")
    exit()


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

    def store_values(self):
        temp = (
            f"DB_SERVER={self.server}\n"
            f"DB_USERNAME={self.username}\n"
            f"DB_PASSWORD={self.password}\n"
            f"DB_NAME={self.dbname}\n"
            f"DB_PORT={self.port}"
        )
        with open(file=".env", mode="w", encoding="utf-8") as env:
            return env.write(temp)

    @staticmethod
    def get_value(key: str = None):
        temp = {}
        with open(file=".env", mode="r", encoding="utf-8") as env:
            for line in env.readlines():
                key, value = line.split("=")
                temp[key.strip()] = value.strip()
        return temp if key is None else temp[key]


class Database:
    def __init__(self):
        self.socket = None
        self.__cursor = None
        self.env_exist()

    @staticmethod
    def env_exist():
        if not exists(".env"):
            print(" > Votre fichier .env n'existe pas, utilisez --make-env pour créer un .env")
            press_exit()

    def connect(self):
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
            press_exit()
        except KeyError as err:
            print(f" > Erreur de clé: {err} n'existe pas dans .env ou le champ est vide !")
            press_exit()

    def show_tables(self):
        return self.__cursor.execute("SHOW TABLES;")


if arg.make_env:
    print(f" > Création du fichier .env {'en mode intuitif' if arg.env_intuitive else ''}")
    if arg.env_intuitive:
        env = Env(
            server=input(" > Adresse vers le serveur mySQL [localhost]: "),
            username=input(" > Nom d'utilisateur: "),
            password=input(" > Mot de passe: "),
            dbname=input(" > Nom de la base de donnée: "),
            port=input(" > Port d'écoute de la base de donnée [3306]: ")
        )
    else:
        env = Env()
    env.store_values()

app = FastAPI()
db = Database()
db.connect()

print(" > Vérification de si la DB est complète...")
print(" > Vérifications finies...")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
