from fastapi import FastAPI

import api.backend as backend_api
import api.mail as mail_api
import api.user as user_api
from classes.database import Database
from classes.debug import Debug

# Database Init for API
db = Database()
db.connect()


def start(app: FastAPI, debug: Debug):
    """
    Charger toutes les routes préecrites et appellées après le update_swagger()
    """

    def update_swagger():
        """
        Une fois toutes les routes chargées, on appelle update_swagger pour forcer le reset du swagger et afficher
        toutes les requetes!
        """
        debug.print(app_module="API", text="Updating Swagger !")
        app.openapi_schema = None
        app.setup()

    """
    A partir d'ici, on load toutes les routes API et à la fin, on update le swagger !
    """
    debug.print(app_module="API", text="Loading all API endpoints !")
    user_api.load(app=app, db=db, debug=debug)
    mail_api.load(app=app)
    backend_api.load(app=app, debug=debug)

    update_swagger()
