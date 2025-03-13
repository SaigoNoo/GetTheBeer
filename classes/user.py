from classes.database import Database


class User:
    def __init__(self, database: Database):
        self.db = database

    def create_user(self, data: dict):
        instruction = f"INSERT INTO ma_table (colonne1, colonne2) VALUES ('valeur1', 'valeur2');"
        self.db.cursor("")
