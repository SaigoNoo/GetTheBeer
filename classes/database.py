from json import loads
from os import getenv

from dotenv import load_dotenv
from mysql.connector import connect, Error, ProgrammingError

load_dotenv()


class Database:
    def __init__(self):
        self.socket = None
        self.cursor = None
        self.commands = []

    def connect(self) -> connect or Error or ProgrammingError:
        """
        Création d'un socket de connexion permettant la communication entre la DB et le backend FastAPI
        :return:
        """
        print(f" > Tentative de connexion avec {getenv(key='DB_USERNAME')}@{getenv(key='DB_SERVER')}")
        try:
            connection = connect(
                host=getenv(key="DB_SERVER"),
                user=getenv(key="DB_USERNAME"),
                password=getenv(key="DB_PASSWORD"),
                database=getenv(key="DB_NAME"),
                port=getenv(key="DB_PORT")
            )
            print(
                f" > Connecté à {getenv('DB_NAME')} "
                f"via {getenv('DB_USERNAME')}@{getenv('DB_SERVER')}")
            self.socket = connection
            self.cursor = connection.cursor()
            return True
        except Error as err:
            print(f" > {err}")
        except KeyError as err:
            print(f" > Erreur de clé: {err} n'existe pas dans .env ou le champ est vide !")

    def call_function(self, name: str, to_json: bool = False, **parameters):
        if len(parameters) > 0:
            parameters = str(tuple(parameters.values()))
            if parameters[-2] == ",":
                parameters = f"{parameters[:-2]})"

        if len(parameters) > 0:
            command = f"SELECT {name}{parameters};"
        else:
            command = f"SELECT {name}();"

        self.cursor.execute(command)

        result = self.cursor.fetchone()[0]

        if to_json:
            if type(result) is type(None):
                return None
            else:
                return loads(result)
        else:
            return result

    def call_procedure(self, name: str, **parameters):
        if len(parameters) > 0:
            parameters = list(parameters.values())
        try:
            self.cursor.callproc(name, parameters)
            self.socket.commit()
        except Exception as e:
            self.socket.rollback()
            return {
                "code": "SQL_ERROR",
                "message": "L'opération a été annulée !",
                "error": e
            }
