from uuid import uuid4

from fastapi import HTTPException

from api.models import CreateUser
from classes.database import Database
from classes.mail import Mail, OpenMailHTML


class UsersAPI:
    def __init__(self, db: Database):
        self.db = db

    @staticmethod
    def generate_token():
        return uuid4()

    def get_user_infos(self, user_id: int) -> dict or None:
        for line in self.db.call_function(name="get_all_users", to_json=True):
            if line["user_ID"] == user_id:
                return line
        return None

    def user_exist(self, email: str):
        for line in self.db.call_function(name="get_all_users", to_json=True):
            if line["mail"] == email:
                return True
        return False

    def get_id(self, email: str):
        for line in self.db.call_function(name="get_all_users", to_json=True):
            if line["mail"] == email:
                return line["user_ID"]
        return None

    def get_mail(self, id_user: int):
        for line in self.db.call_function(name="get_all_users", to_json=True):
            if line["user_ID"] == id_user:
                return line["mail"]
        return None

    def ask_reset(self, email: str):
        if self.user_exist(email=email):
            id_u = self.get_id(email=email)
            infos = self.get_user_infos(user_id=id_u)
            if self.db.call_function(name="have_reset_token", uid=id_u) == 0:
                gen_token = self.generate_token()
                self.db.call_procedure(name="token_reset", user_id=id_u, token=str(gen_token))
                content = OpenMailHTML().html_raw(file="reset", name=infos["prenom"], token=str(gen_token))
                Mail(receiver=email, title="Demande de reset", body=content).send()
                return {
                    "code": "MAIL_SEND_OK",
                    "message": "Un mail à été envoyé si votre compte existe !"
                }
            else:
                return {
                    "code": "MAIL_OK_SEND_FAIL",
                    "message": "Un mail a déjà été envoyé ! Patientez 15 minutes avant de relancer une demande !"
                }
        else:
            return {
                "code": "MAIL_SEND_FAIL",
                "message": "Erreur ou compte inconnu !"
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
        if self.user_exist(email=data.mail) == 0:
            self.db.call_procedure(
                name="add_user",
                nom=data.l_name,
                prenom=data.f_name,
                psuedo=data.username,
                mail=data.mail,
                image=data.image,
                password=data.password,
                bio=data.bio,
                description=data.desc
            )
            return {
                "code": "USER_ADD_OK",
                "message": "Utilisateur crée avec succès !"
            }
        else:
            raise HTTPException(status_code=405, detail=f"{data.mail} existe déjà !")

    def list_members(self):
        return self.db.call_function(name="get_all_users", to_json=True)
