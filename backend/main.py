from fastapi import FastAPI, HTTPException, Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from db_utils import (
    create_account,
    get_username,
    login_db,
    get_opponent,
    get_user_beer_reserve,
    do_transaction,
    recup,
    get_user_profile
)
import bcrypt
from db_utils import get_friends


# Modèle pour l'inscription
class UserSignup(BaseModel):
    nom: str
    prenom: str
    pseudo: str
    mail: str
    motdepasse: str
    biographie: str

# ✅ Modèle pour la connexion
class UserLogin(BaseModel):
    username: str
    password: str

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="user123",  # À changer pour la prod
    max_age=3600
)

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/api/signup")
def signup(user: UserSignup):
    try:
        hashed_password = bcrypt.hashpw(user.motdepasse.encode(), bcrypt.gensalt())
        result = create_account(
            user.nom, user.prenom, user.pseudo, user.mail, hashed_password, user.biographie
        )
        if isinstance(result, int):
            return {"message": "Inscription réussie!", "userId": result}
        else:
            raise HTTPException(status_code=400, detail=result)
    except HTTPException as he:
        raise he
    except Exception as e:
        print("exception =", e)
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")

@app.post("/api/login")
async def login(user: UserLogin, request: Request):
    try:
        user_id = login_db(user.username)
        if user_id is None:
            return {"success": False, "message": "Utilisateur inconnu"}
        elif bcrypt.checkpw(user.password.encode(), user_id[1]):
            request.session["user_id"] = user_id[0]
            return {"success": True, "message": "Connexion réussie"}
        else:
            return {"success": False, "message": "Mot de passe incorrect"}
    except Exception as e:
        import traceback
        traceback.print_exc()  # 💥 affiche la stack complète dans les logs du backend
        raise HTTPException(status_code=500, detail=str(e))  # Affiche l'erreur dans Swagger


@app.post("/api/logout")
async def logout(request: Request):
    request.session.clear()
    return {"message": "Déconnexion réussie"}

@app.get("/api/me")
async def get_current_user(request: Request):
    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Non authentifié")
    pseudo = get_username(user_id)
    reserve_biere = get_user_beer_reserve(user_id)
    return {"user": {"user_id": user_id, "pseudo": pseudo, "reserve_biere": reserve_biere}}

@app.get("/api/users/game")
async def get_users(request: Request):
    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Non authentifié")
    opponents = get_opponent(user_id)
    return opponents

@app.post("/api/game/transaction")
async def handle_transaction(request: Request):
    data = await request.json()
    winner_id = data.get("winner_id")
    loser_id = data.get("loser_id")
    beers = data.get("beers")
    if not winner_id or not loser_id or not beers:
        raise HTTPException(status_code=400, detail="Invalid data")
    try:
        result = do_transaction(winner_id, loser_id, beers)
        return result
    except Exception as e:
        print("Error in transaction:", e)
        raise HTTPException(status_code=500, detail="Transaction failed")

@app.get("/api/test")
def test_backend():
    return {"message": "Connexion au backend réussie ✅"}

@app.get("/api/user/{user_id}")
def get_user_profile_route(user_id: int):
    user = recup(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user

@app.get("/api/profile")
async def get_profile(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Non authentifié")
    user_data = get_user_profile(user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user_data

@app.get("/api/friends/{user_id}")
def get_user_friends(user_id: int):
    try:
        friends = get_friends(user_id)
        print("Amis récupérés :", friends)  # ➜ Ajout temporaire
        return friends
    except Exception as e:
        print("Erreur API /api/friends :", e)
        raise HTTPException(status_code=500, detail=str(e))