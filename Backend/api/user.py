from api.models import CreateUser, ResetEmailResponse, RequestPasswordReset, Authentification
from classes.database import Database
from classes.debug import Debug
from classes.users import UsersAPI
from fastapi import FastAPI, Request, HTTPException


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
    async def get_users():
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
        return user.reset_password(token=data.token, new_password=data.password)

    @app.post(
        path="/api/user/login/",
        description="Connexion d'un utilisateur",
        tags=["Authentification"]
    )
    async def login(data: Authentification, request: Request):
        return user.login_user(username=data.username, password=data.password, request=request)

    @app.get(
        path="/api/user/list_friends",
        tags=["Friends", "Show"]
    )
    async def show_friends(request: Request):
        return user.list_friends(my_id=request.session.get("user_id"))

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
        description="Wait...",
        tags=["Users", "Show"]
    )
    async def get_current_user(request: Request):
        user_id = request.session.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Non authentifié")

        pseudo = user.get_username(
            email=user.get_mail(
                id_user=user_id
            )
        )

        return {
            "user": {
                "user_id": user_id,
                "pseudo": pseudo,
                "reserve_biere": db.call_function(name="get_user_beer_reserve", uid=user_id),
                "parties_jouees": db.call_function(name="count_games", uid=user_id),
                "bieres_pariees": db.call_function(name="beers_bet", uid=user_id),
                "bieres_perdues": db.call_function(name="get_loose_beer", uid=user_id),
                "bieres_gagnes": db.call_function(name="get_win_beer", uid=user_id)
            }
        }

    @app.get("/api/user/profil")
    async def get_profile(request: Request):
        user_id = request.session.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Non authentifié")
        user_data = user.get_user_infos(user_id=user_id)
        if not user_data:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        return user_data

    @app.get(
        path="/api/game/opponents",
        tags=["Friends", "Game"]
    )
    async def get_users(request: Request):
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Non authentifié")
        opponents = user.get_opponent(user_id=user_id)
        return opponents

    @app.get("/api/users/opponents")
    async def get_users(request: Request):
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Non authentifié")
        return user.get_opponent(user_id=user_id)

    @app.post("/api/game/transaction")
    async def handle_transaction(request: Request):
        data = await request.json()

        debug.print(app_module="UserTransaction", text=f"Received transaction data: {data}")

        # Validate input data
        if not data.get("winner_id") or not data.get("loser_id") or not data.get("beers"):
            raise HTTPException(status_code=400, detail="Invalid data")

        try:
            # Call the do_transaction function
            result = user.do_transaction(winner_id=data.get("winner_id"), loser_id=data.get("loser_id"),
                                         beers=data.get("beers"))
            return result
        except Exception as e:
            debug.print(app_module="UserTransaction", text=f"Error in transaction: {e}")
            raise HTTPException(status_code=500, detail="Transaction failed")
