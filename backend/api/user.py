
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from api.models import CreateUser, ResetEmailRequest
from classes.database import Database
from classes.mail import Mail
from classes.level import LevelSystem 

class Users:
    def __init__(self, db: Database):
        self.db = db
        self.level_system = LevelSystem(db)

    def test_get_all_users(self):
        users = self.db.call_function(name="get_all_users", to_json=True)
        return users

    def get_email_from_username_or_email(self, username: str):
        if self.db.call_function(name="user_exists", username=username) == 1:
            id_u = self.db.call_function(name="id_of_user", username=username)
            return self.db.call_function(name="get_user_info_by_id", to_json=True, id=id_u)["email"]

    @staticmethod
    def generate_token():
        return uuid4()

    def ask_reset(self, email: str):
        if self.db.call_function(name="user_exists", email_username=email):
            id_u = self.db.call_function(name="id_of_user", email_username=email)
            if "@" not in email:
                email = self.get_email_from_username_or_email(username=email)
            if not self.db.call_function(name="is_active_token", id=id_u) == 1:
                url_reset = f"https://localhost:8000/api/reset/token/{id_u}"
                message = ("Vous avez fait une demande réinitialisation de mot de passe.\n"
                           f"Rendez vous sur {url_reset}\n")
                Mail(receiver=email, title="Demande de reset", body=message).send()
                return "Un mail à été envoyé si votre compte existe !"
            else:
                return "Une demande a déjà été effectuée, veuillez patienter 15min à compter du premier reset !"
        else:
            return "Erreur ou compte inconnu !"

    def reset_password(self, username: str, token: str):
        pass

    def get_user_infos(self, user_id: int):
        try:
            return self.db.call_function(name="get_user_info_by_id", to_json=True, id=user_id)
        except TypeError:
            raise HTTPException(status_code=404, detail=f"{user_id} est soit innexistant soit vide !")
        except Exception as error:
            raise HTTPException(status_code=400, detail=f"Erreur inconnue: {error} !")

    def create_user(self, data: CreateUser):
        user_exist = self.db.call_function(name="user_exists", username=data.username)
        if user_exist == 0:
            self.db.call_procedure(
                name="create_user",
                user=data.username,
                password=data.password,
                avatar=data.url_avatar,
                last_name=data.last_name,
                first_name=data.first_name,
                email=data.email,
                is_admin=1 if data.is_admin else 0
            )
            return {
                "message": "Utilisateur créé avec succès !"
            }
        else:
            raise HTTPException(status_code=405, detail=f"{data.username} existe déjà !")

    def list_members(self):
        return self.db.call_function(name="show_members_admin", to_json=True)

    def login_user(self, username: str, password: str):
        user_exist = self.db.call_function(name="user_exists", username=username)
        if user_exist == 1:
            stored_password = self.db.call_function(name="get_user_password", username=username)
            if stored_password == password:
                return {"message": "Connexion réussie !"}
        raise HTTPException(status_code=401, detail="Identifiants incorrects")

    def add_friend(self, user_id: int, friend_id: int):
        if self.db.call_function(name="user_exists", id=friend_id) == 1:
            if self.db.call_function(name="is_friend", id=user_id, friend_id=friend_id) == 0:
                self.db.call_procedure(name="add_friend", user_id=user_id, friend_id=friend_id)
                return {"message": "Ami ajouté avec succès !"}
            else:
                raise HTTPException(status_code=405, detail=f"{friend_id} est déjà dans votre liste d'amis !")
        else:
            raise HTTPException(status_code=404, detail=f"{friend_id} est soit innexistant soit vide !")

    def delete_friend(self, user_id: int, friend_id: int):
        if self.db.call_function(name="user_exists", id=friend_id) == 1:
            if self.db.call_function(name="is_friend", id=user_id, friend_id=friend_id) == 1:
                self.db.call_procedure(name="delete_friend", user_id=user_id, friend_id=friend_id)
                return {"message": "Ami supprimé avec succès !"}
            else:
                raise HTTPException(status_code=405, detail=f"{friend_id} n'est pas dans votre liste d'amis !")
        else:
            raise HTTPException(status_code=404, detail=f"{friend_id} est soit innexistant soit vide !")


def load(app: FastAPI, db: Database) -> None:
    user = Users(db=db)

    @app.get("/api/users", tags=["USER"])
    async def get_users():
        return user.test_get_all_users()

    @app.get("/api/user/infos", tags=["USER"])
    async def get_name(user_id: int):
        return user.get_user_infos(user_id=user_id)

    @app.get("/api/admin/users", tags=["ADMIN"])
    async def get_users_admin():
        return user.list_members()

    @app.post("/api/user/create/", tags=["USER"])
    async def create_user(data: CreateUser):
        return user.create_user(data=data)

    @app.post("/api/user/reset_password_request", tags=["USER"])
    async def reset_password_request(data: ResetEmailRequest):
        return user.ask_reset(email=data.email)

    @app.post("/api/user/login/", tags=["USER"])
    async def login(username: str, password: str):
        return user.login_user(username=username, password=password)

    @app.post("/api/user/add_friend/", tags=["USER"])
    async def add_friend(user_id: int, friend_id: int):
        return user.add_friend(user_id=user_id, friend_id=friend_id)

    @app.post("/api/user/delete_friend/", tags=["USER"])
    async def delete_friend(user_id: int, friend_id: int):
        return user.delete_friend(user_id=user_id, friend_id=friend_id)

    @app.get("/api/user/level", tags=["USER"])
    async def get_user_level(user_id: int):
        return user.level_system.get_user_level(user_id)

    @app.get("/api/user/friends", tags=["USER"])
    async def get_user_friends(pseudo: str):
        query = '''
            SELECT u.pseudo 
            FROM utilisateurs u
            JOIN amis a ON u.id_utilisateur = a.id_ami
            JOIN utilisateurs current ON current.id_utilisateur = a.id_utilisateur
            WHERE current.pseudo = %s
        '''
        result = db.fetch_all(query, (pseudo,))
        amis = [row[0] for row in result]
        return amis
