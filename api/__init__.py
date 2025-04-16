from fastapi import FastAPI

import api.user as user_api
import api.mail as mail_api

from classes.database import Database

# Database Init for API
db = Database()
db.connect()


def start(app: FastAPI):
    """
    Charger toutes les routes préecrites et appellées après le update_swagger()
    """

    def update_swagger():
        """
        Une fois toutes les routes chargées, on appelle update_swagger pour forcer le reset du swagger et afficher
        toutes les requetes!
        """
        app.openapi_schema = None
        app.setup()

    """
    A partir d'ici, on load toutes les routes API et à la fin, on update le swagger !
    """
    user_api.load(app=app, db=db)
    mail_api.load(app=app)

    update_swagger()
