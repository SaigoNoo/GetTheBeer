from uuid import uuid4

from bcrypt import hashpw, gensalt, checkpw
from fastapi import HTTPException

from api.models import CreateUser
from classes.database import Database
from classes.debug import Debug
from classes.mail import Mail, OpenMailHTML


class UsersAPI:
    def __init__(self, db: Database, debug: Debug):
        self.db = db
        self.debug = debug
        print(self.do_transaction(winner_id=5, loser_id=6, beers=3))

    def generate_token(self):
        self.debug.print(app_module="UserAPI", text="Génération du token...")
        return uuid4()

    def get_user_infos(self, user_id: int) -> dict or None:
        self.debug.print(app_module="UserAPI", text=f"Obtention des infos sur l'utilisateur avec l'id: {user_id}")
        for line in self.db.call_function(name="get_all_users", to_json=True):
            if line["user_ID"] == user_id:
                self.debug.print(
                    app_module="UserAPI",
                    text="Infos trouvées !"
                )
                return line
        self.debug.print(
            app_module="UserAPI",
            text="Aucune info trouvée !"
        )
        return None

    def user_exist(self, username: str):
        for line in self.db.call_function(name="get_all_users", to_json=True):
            if line["pseudo"] == username:
                return True
        return False

    def get_id(self, username: str):
        for line in self.db.call_function(name="get_all_users", to_json=True):
            if line["pseudo"] == username:
                return line["user_ID"]
        return None

    def get_mail(self, id_user: int):
        for line in self.db.call_function(name="get_all_users", to_json=True):
            if line["user_ID"] == id_user:
                return line["mail"]
        return None

    def get_username(self, email: str):
        for line in self.db.call_function(name="get_all_users", to_json=True):
            if line["mail"] == email:
                return line["pseudo"]
        return None

    def ask_reset(self, username: str):
        if self.user_exist(username=username):
            id_u = self.get_id(username=username)
            infos = self.get_user_infos(user_id=id_u)
            if self.db.call_function(name="have_reset_token", uid=id_u) == 0:
                gen_token = self.generate_token()
                self.db.call_procedure(name="token_reset", user_id=id_u, token=str(gen_token))
                content = OpenMailHTML().html_raw(file="reset", name=infos["prenom"], token=str(gen_token))
                try:
                    Mail(receiver=infos['mail'], title="Demande de reset", body=content).send()
                    return {
                        "code": "MAIL_SEND_OK",
                        "message": "Un mail à été envoyé si votre compte existe !"
                    }
                except:
                    return {
                        "code": "MAIL_SEND_FAIL",
                        "message": "Un soucis semble exister au niveau du serveur MAIL (SMTP ERROR) !"
                    }
            else:
                return {
                    "code": "MAIL_OK_SEND_FAIL",
                    "message": "Un mail a déjà été envoyé ! Patientez 15 minutes avant de relancer une demande !"
                }
        else:
            return {
                "code": "USER_NOT_EXIST",
                "message": f"{username} n'est pas inscrit dans GetTheBeer!"
            }

    def reset_password(self, token: str, new_password: str):
        try:
            self.db.call_procedure(name="update_password_by_token", p_id=token, new_pass=new_password)
            return {
                "code": "RESET_OK",
                "message": "Le mot de passe a bien été modifié !"
            }
        except Exception as e:
            return {
                "code": "RESET_FAIL",
                "message": e
            }

    def create_user(self, data: CreateUser):
        if not self.user_exist(username=data.username):
            self.db.call_procedure(
                name="add_user",
                lname=data.l_name,
                fname=data.f_name,
                pseudo=data.username,
                mail=data.email,
                picture=data.image,
                hashed_password=hashpw(password=data.password.encode(), salt=gensalt()),
                bio=data.bio
            )
            content = OpenMailHTML().html_raw(file="welcome", name=data.username)
            Mail(receiver=data.email, title="Confirmation de création de compte", body=content).send()
            return {
                "code": "USER_ADD_OK",
                "message": "Utilisateur crée avec succès !"
            }
        else:
            raise HTTPException(status_code=405, detail=f"{data.username} ou {data.email} existe déjà !")

    def list_members(self):
        return self.db.call_function(name="get_all_users", to_json=True)

    def login_user(self, username: str, password: str):
        if self.user_exist(username):
            stored_password = self.db.call_function(name="get_user_password", username=username)
            if checkpw(password=password.encode(), hashed_password=stored_password.encode()):
                return {
                    "success": True,
                    "code": "SUCCESS_LOGIN",
                    "message": "Connexion réussie !"
                }
        return {
            "success": False,
            "code": "FAIL_LOGIN",
            "message": "Connexion échouée !"
        }

    def add_friend(self, my_id: int, friend_id: int):
        if self.user_exist(username=self.get_user_infos(user_id=my_id)["pseudo"]):
            if self.db.call_function(name="is_friend", my_id=my_id, friend_id=friend_id) == 0:
                self.db.call_procedure(name="add_friend", my_id=my_id, friend_id=friend_id)
                content = OpenMailHTML().html_raw(
                    file="new_friend",
                    name=self.get_user_infos(
                        user_id=friend_id
                    )['pseudo'],
                    friend=self.get_user_infos(
                        user_id=my_id
                    )['pseudo']
                )
                Mail(
                    receiver=self.get_user_infos(
                        user_id=friend_id
                    )["mail"],
                    title="Nouvelle demande d'ami",
                    body=content
                ).send()
                return {"message": "Ami ajouté avec succès !"}
            else:
                raise HTTPException(status_code=405, detail=f"{friend_id} est déjà dans votre liste d'amis !")
        else:
            raise HTTPException(status_code=404, detail=f"{friend_id} est soit innexistant soit vide !")

    def delete_friend(self, my_id: int, friend_id: int):
        if self.user_exist(username=self.get_user_infos(user_id=my_id)["pseudo"]):
            if self.db.call_function(name="is_friend", my_id=my_id, friend_id=friend_id) == 1:
                self.db.call_procedure(name="delete_friend", my_id=my_id, friend_id=friend_id)
                return {"message": "Ami supprimé avec succès !"}
            else:
                raise HTTPException(status_code=405, detail=f"{friend_id} n'est pas dans votre liste d'amis !")
        else:
            raise HTTPException(status_code=404, detail=f"{friend_id} est soit innexistant soit vide !")

    def get_opponent(self, user_id: int):
        response = []
        for user in self.list_members():
            response.append(user) if user["user_ID"] != user_id else None
        return response

    def do_transaction(self, winner_id, loser_id, beers):
        self.debug.print(app_module="UserTransaction", text="Calcul des changements de bieres...")
        beers_left_looser = self.db.call_function(
            name="how_many_beer",
            uid=loser_id
        ) - beers

        beers_left_winner = self.db.call_function(
            name="how_many_beer",
            uid=winner_id
        ) + beers

        self.debug.print(app_module="UserTransaction", text="Modifications des bieres dans la DB...")

        self.db.call_procedure(
            name="do_beer_transaction",
            uid=loser_id,
            beer=beers_left_looser
        )

        self.db.call_procedure(
            name="do_beer_transaction",
            uid=winner_id,
            beer=beers_left_winner
        )

        # Record the transaction
        self.db.call_procedure(
            name="add_transaction",
            looser_uid=loser_id,
            winner_uid=winner_id,
            beers_owed=beers
        )

        return {
            "success": True,
            "message": "Transaction completed"
        }
