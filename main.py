from fastapi import FastAPI
from mysql.connector import connect, Error
from sqlparse import format


class Database:
    def __init__(self):
        self.socket = None
        self.__cursor = None

    @staticmethod
    def __get_values():
        temp = {}
        with open(file=".env", mode="r", encoding="utf-8") as env:
            for line in env.readlines():
                key, value = line.split("=")
                temp[key.strip()] = value.strip()
        return temp

    def connect(self):
        try:
            connection = connect(
                host=self.__get_values()["DB_SERVER"],
                user=self.__get_values()["DB_USERNAME"],
                password=self.__get_values()["DB_PASSWORD"],
                database=self.__get_values()["DB_NAME"],
                port=self.__get_values()["DB_PORT"]
            )
            print(
                f" > Connecté à {self.__get_values()['DB_NAME']} sur {self.__get_values()['DB_SERVER']} en tant que {self.__get_values()['DB_USERNAME']}")
            self.socket = connection
            self.__cursor = connection.cursor()
            return True
        except Error as err:
            print(f" > {err}")
        except KeyError as err:
            print(f" > Erreur de clé: {err} n'existe pas dans .env ou le champ est vide !")

    def show_tables(self):
        return self.__cursor.execute("SHOW TABLES;")


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
