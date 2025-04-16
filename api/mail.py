from fastapi import FastAPI

from api.models import SendMail
from classes.mail import Mail, OpenMailHTML


def load(app: FastAPI) -> None:
    """
    Charger toutes les CALLS API
    """

    @app.post(
        path="/api/mail/send/",
        description="Permet d'envoyer un email à un utilisateur !",
        tags=["MAIL"],
    )
    async def create_user(data: SendMail):
        content = OpenMailHTML().html_raw(file=data.file, **data.extra)
        mail = Mail(receiver=data.email, title=data.subject, body=content)
        mail.send()
        return {
            "code": "MAIL_SEND_OK",
            "message": "Le mail a bien été envoyé !"
        }