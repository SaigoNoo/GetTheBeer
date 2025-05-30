from uuid import uuid4

from api.models import CreateUser
from bcrypt import hashpw, gensalt, checkpw
from classes.database import Database
from classes.debug import Debug
from classes.mail import Mail, OpenMailHTML
from fastapi import HTTPException
from fastapi import Request


class UsersAPI:
    def __init__(self, db: Database, debug: Debug):
        self.db = db
        self.debug = debug

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

    def uid_exist(self, uid: int):
        if uid == 0:
            return False
        for line in self.db.call_function(name="get_all_users", to_json=True):
            if line["user_ID"] == uid:
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

    def check_uid(self, uid: int):
        self.debug.print(app_module="UserCheck", text=f"Vérification que l'ID {uid} existe...")
        if not self.uid_exist(uid=uid):
            self.debug.print(
                app_module="UserCheck",
                text=f"L'UID {uid} n'existe pas !"
            )
            return False
        return True

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

    @staticmethod
    def encrypt_password(data: str):
        return hashpw(password=data.encode(), salt=gensalt())

    def reset_password(self, token: str, new_password: str):
        try:
            if self.db.call_function(
                    name="have_reset_token",
                    uid=self.db.call_function(
                        name="get_token_owner_id",
                        token=token
                    )
            ):
                self.db.call_procedure(
                    name="update_password_by_token",
                    p_id=token,
                    new_pass=self.encrypt_password(
                        data=new_password
                    ))
                infos = self.get_user_infos(user_id=self.db.call_function(name="get_token_owner_id", token=str(token)))
                content = OpenMailHTML().html_raw(file="reset_confirm", name=infos["prenom"])
                Mail(receiver=infos['mail'], title="Demande de reset", body=content).send()
                return {
                    "code": "RESET_OK",
                    "message": "Le mot de passe a bien été modifié !"
                }
        except Exception as e:
            return {
                "code": "RESET_FAIL",
                "message": "Votre TOKEN est certainement invalide",
                "erreur": e
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
                hashed_password=self.encrypt_password(data=data.password),
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

    def login_user(self, username: str, password: str, request: Request):
        if self.user_exist(username):
            stored_password = self.db.call_function(name="get_user_password", username=username)
            if checkpw(password=password.encode(), hashed_password=stored_password.encode()):
                request.session["user_id"] = self.get_id(username=username)
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

    def list_friends(self, my_id: int):
        return self.db.call_function(name="get_friends", user_id=my_id)

    def get_opponent(self, user_id: int):
        response = []
        for user in self.list_members():
            data = user
            data["beers"] = self.db.call_function(
                name="get_user_beer_reserve",
                uid=data["user_ID"]
            )
            response.append(user) if user["user_ID"] != user_id else None
        return response

    def do_transaction(self, winner_id: int, loser_id: int, beers: int):
        self.check_uid(uid=winner_id) and self.check_uid(uid=loser_id)
        self.debug.print(app_module="UserTransaction",
                         text="Verification de si le perdant n'est pas en endeté ou si il tombera pas en négatif")
        if self.db.call_function("has_enough_beer", uid=loser_id, beers=beers) == 0:
            self.debug.print(app_module="UserTransaction", text="Le perdant n'a plus assez de bieres a offrir")
            raise HTTPException(status_code=405, detail="Le perdant n'a plus assez de bieres a offrir !")
        self.debug.print(app_module="UserTransaction", text="Calcul des changements de bieres...")

        self.debug.print(app_module="UserTransaction", text="Modifications des bieres dans la DB...")
        self.db.call_procedure(
            name="do_beer_transaction",
            w_uid=winner_id,
            l_uid=loser_id,
            beer=beers
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
