from mysql.connector import connect, Error, ProgrammingError

from classes.env import Env


class Database:
    def __init__(self):
        self.socket = None
        self.cursor = None

    def connect(self) -> connect or Error or ProgrammingError:
        """
        Création d'un socket de connexion permettant la communication entre la DB et le backend FastAPI
        :return:
        """
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
            self.cursor = connection.cursor()
            return True
        except Error as err:
            print(f" > {err}")
        except KeyError as err:
            print(f" > Erreur de clé: {err} n'existe pas dans .env ou le champ est vide !")

    def call(self, ctype: str, name: str, **kwargs):
        options = []
        for key in kwargs.values():
            options.append(f"\"{key}\"")
        command = f"{'SELECT' if ctype == 'func' else 'CALL'} {name}({', '.join(options)})"
        print(f" > {command}")

        try:
            self.cursor.execute(command)
            result = self.cursor.fetchone()
            if result and result[0]:
                return result[0]
        except ProgrammingError:
            print(f" > La {'fonction' if ctype == 'func' else 'procédure'} {name} n'existe pas !")
