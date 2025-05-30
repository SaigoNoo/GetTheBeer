from json import loads
from os import getenv

from classes.debug import Debug
from dotenv import load_dotenv
from mysql.connector import connect, Error, ProgrammingError

load_dotenv()


class Database:
    def __init__(self, debug: Debug):
        self.socket = None
        self.cursor = None
        self.is_socket_valid = False
        self.commands = []
        self.debug = debug

    def connect(self) -> connect or Error or ProgrammingError:
        """
        Création d'un socket de connexion permettant la communication entre la DB et le backend FastAPI
        :return:
        """
        self.debug.print(
            app_module="MySQL",
            text=f"Tentative de connexion: {getenv(key='DB_USERNAME')}@{getenv(key='DB_SERVER')}"
        )
        try:
            connection = connect(
                host=getenv(key="DB_SERVER"),
                user=getenv(key="DB_USERNAME"),
                password=getenv(key="DB_PASSWORD"),
                database=getenv(key="DB_NAME"),
                port=getenv(key="DB_PORT")
            )
            self.debug.print(
                app_module="MySQL",
                text=f"Connecté à {getenv(key='DB_NAME')} !"
            )
            self.is_socket_valid = True
            self.socket = connection
            self.cursor = connection.cursor()
            return True
        except Error as err:
            print(f" > {err}")
        except KeyError as err:
            print(f" > Erreur de clé: {err} n'existe pas dans .env ou le champ est vide !")

    def reconnect_if_needed(self):
        if self.is_socket_valid:
            try:
                self.debug.print(
                    app_module="MySQL",
                    text=f"Vérification de si le curseaur est actif..."
                )
                self.socket.ping(reconnect=True, attempts=3, delay=5)
                return {
                    "code": "SQL_SUCCESS",
                    "message": "Socket connecté avec succès"
                }
            except Error:
                self.debug.print(
                    app_module="MySQL",
                    text=f"Reconnexion et actualisation du curseur !"
                )
                self.connect()
                return {
                    "code": "SQL_SUCCESS_RECONNECT",
                    "message": "Socket reconnecté avec succès"
                }
        else:
            return {
                "code": "SQL_SOCKET_FAIL",
                "message": "Votre socket à la base est incorrect, vérifiez votre .env !",
                "data": {
                    "username": f'{getenv(key="DB_USERNAME")[0]}{"*" * (len(getenv(key="DB_USERNAME")) - 1)}',
                    "server": f'sql://{getenv(key="DB_SERVER")}:{getenv(key="DB_PORT")}',
                    "db_name": getenv(key="DB_NAME")
                }
            }

    def call_function(self, name: str, to_json: bool = False, **parameters):
        try_connect = self.reconnect_if_needed()
        if try_connect["code"] != "SQL_SOCKET_FAIL":
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
        else:
            return try_connect

    def call_procedure(self, name: str, **parameters):
        try_connect = self.reconnect_if_needed()
        if try_connect["code"] != "SQL_SOCKET_FAIL":
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
        else:
            return try_connect
