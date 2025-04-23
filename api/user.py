from fastapi import FastAPI, Request, HTTPException

from api.models import CreateUser, ResetEmailResponse, RequestPasswordReset
from classes.database import Database
from classes.debug import Debug
from classes.users import UsersAPI


def load(app: FastAPI, db: Database, debug: Debug) -> None:
    """
    Charger toutes les CALLS API
    """
    user = UsersAPI(db=db, debug=debug)

    @app.post(
        path="/api/user/create/",
        description="Permet de créer un utilisateurs",
        tags=["Create"],
    )
    async def create_user(data: CreateUser):
        return user.create_user(data=data)

    @app.get(
        path="/api/user/show_members",
        description="Permet de lister les utilisateurs",
        tags=["Show"],
    )
    async def get_users() -> list or None:
        return user.list_members()

    @app.post(
        path="/api/user/reset_password_request",
        description="Demander un reset du mot de passe !",
        tags=["Reset"]
    )
    async def reset_password_request(data: RequestPasswordReset):
        return user.ask_reset(username=data.username)

    @app.post(
        path="/api/user/reset_password",
        description="Reset le mot de passe",
        tags=["Reset"]
    )
    async def reset_password(data: ResetEmailResponse):
        pass

    @app.post(
        path="/api/user/login/",
        description="Connexion d'un utilisateur",
        tags=["Authentification"]
    )
    async def login(username: str, password: str):
        return user.login_user(username=username, password=password)

    @app.post(
        path="/api/user/add_friend/",
        description="Permet d'ajouter un ami",
        tags=["Friends", "Create"]
    )
    async def add_friend(user_id: int, friend_id: int):
        return user.add_friend(my_id=user_id, friend_id=friend_id)

    @app.post(
        path="/api/user/delete_friend/",
        description="Permet de supprimer un ami",
        tags=["Friends", "Delete"]
    )
    async def delete_friend(user_id: int, friend_id: int):
        return user.delete_friend(my_id=user_id, friend_id=friend_id)

    @app.get(
        path="/api/user/is_friend",
        description="Vérifier si deux joueurs sont amis sur base de leur usernames",
        tags=["Friends", "Show"]
    )
    async def are_friends(username_a: str, username_b: str):
        if user.user_exist(username=username_a) and user.user_exist(username=username_b):
            id_a, id_b = user.get_id(username=username_a), user.get_id(username=username_b)
            info = db.call_function(
                name="is_friend",
                id_a=id_a,
                id_b=id_b
            )
            return {
                "code": "FRIENDS_FIND" if info == 1 else "NOT_FRIENDS",
                "message": f"{username_a} et {username_a} {'sont' if info == 1 else 'ne sont pas'} amis !"
            }
        else:
            return {
                "code": "USER_NOT_FIND",
                "message": "Un ou plusieurs utilisateurs ne sont pas reconnus dans dans notre base de donnée !"
            }

    @app.post(
        path="/api/user/logout",
        description="Déconnexion utilisateur",
        tags=["Users"]
    )
    async def logout(request: Request):
        request.session.clear()
        return {
            "code": "LOGOUT_SUCCESS",
            "message": "Déconnexion réussi"
        }

    @app.get(
        path="/api/user/me",
        tags=["Users", "Show"]
    )
    async def get_current_user(request: Request):
        user_id = request.session.get("user_id")
        if user_id is None:
            print("test1")
            raise HTTPException(status_code=401, detail="Non authentifié")
        print("test2")
        # Récupère les infos utilisateur selon ton besoin (ici, pseudo)
        pseudo = user.get_username(
            email=user.get_mail(
                id_user=user_id
            )
        )
        reserve_biere = db.call_function(name="get_user_beer_reserve", uid=user_id)
        print(pseudo)
        return {"user": {"user_id": user_id, "pseudo": pseudo, "reserve_biere": reserve_biere}}

    @app.get("/api/users/opponents")
    async def get_users(request: Request):
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Non authentifié")
        return user.get_opponent(user_id=user_id)

    @app.post("/api/game/transaction")
    async def handle_transaction(request: Request):
        data = await request.json()
        winner_id = data.get("winner_id")
        loser_id = data.get("loser_id")
        beers = data.get("beers")

        debug.print(app_module="UserTransaction", text=f"Received transaction data: {data}")

        # Validate input data
        if not winner_id or not loser_id or not beers:
            raise HTTPException(status_code=400, detail="Invalid data")

        try:
            # Call the do_transaction function
            result = user.do_transaction(winner_id=winner_id, loser_id=loser_id, beers=beers)
            return result
        except Exception as e:
            debug.print(app_module="UserTransaction", text=f"Error in transaction: {e}")
            raise HTTPException(status_code=500, detail="Transaction failed")
