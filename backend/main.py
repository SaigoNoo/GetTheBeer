from fastapi import FastAPI, HTTPException, Request, status
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from db_utils import (
    recup,
    create_account,
    get_username,
    login_db,
    get_opponent,
    get_user_beer_reserve,
    do_transaction,
)
import bcrypt    #Crypter le mot de passe


class UserSignup(BaseModel):
    nom: str
    prenom: str
    pseudo: str
    mail: str
    motdepasse: str
    biographie: str

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="user123",   # à changer une fois en production
    max_age=3600    # max_age en secondes
)

# Liste des origines autorisées
origins = [
    "http://localhost:5173"  # React.js en développement
]

# Appliquer CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permettre l'accès uniquement depuis localhost:3000
    allow_credentials=True,
    allow_methods=["*"],  # Accepter toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"]  # Accepter tous les headers
)

# Base.metadata.create_all(bind=engine)

@app.get("/api/test")
def read_root():
    #print(recup())
    return {"message": "Hello World"}



# Nouvel endpoint pour l'inscription
@app.post("/api/signup")
def signup(user: UserSignup):
    try:
        hashed_password = bcrypt.hashpw(user.motdepasse.encode(), bcrypt.gensalt())

        result = create_account(
            user.nom,
            user.prenom,
            user.pseudo,
            user.mail,
            hashed_password,
            user.biographie
        )

        if isinstance(result, int):  # Si result est un ID (entier)
            return {"message": "Inscription réussie!", "userId": result}
        else:
            raise HTTPException(status_code=400, detail=result)
    except HTTPException as he:
        raise he
    except Exception as e:
        print("excepion = ", e)
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@app.post("/api/login")
async def login(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    user_id = login_db(username)  # Récupère l'ID et le mdp crypté
    if user_id == None:
        return {"success": False, "message": "Utilisateur inconnu"}
    elif bcrypt.checkpw(password.encode(), user_id[1]):
        request.session["user_id"] = user_id[0]
        return {"success": True, "message": "Connexion réussie"}
    else:
        return {"success": False, "message": "Mot de passe incorrect"}

@app.post("/api/logout")
async def logout(request: Request):
    request.session.clear()
    return {"message": "Déconnexion réussie"}


@app.get("/api/me")
async def get_current_user(request: Request):
    user_id = request.session.get("user_id")
    if user_id == None:
        print("test1")
        raise HTTPException(status_code=401, detail="Non authentifié")
    print("test2")
    # Récupère les infos utilisateur selon ton besoin (ici, pseudo)
    pseudo = get_username(user_id)
    reserve_biere = get_user_beer_reserve(user_id)
    print(pseudo)
    return {"user": {"user_id": user_id, "pseudo": pseudo, "reserve_biere": reserve_biere}}


@app.get("/api/users/game")
async def get_users(request: Request):
    user_id = request.session.get("user_id")
    if user_id == None:
        raise HTTPException(status_code=401, detail="Non authentifié")
    opponents = get_opponent(user_id)
    print(opponents)
    return (opponents)


@app.post("/api/game/transaction")
async def handle_transaction(request: Request):
    data = await request.json()
    winner_id = data.get("winner_id")
    loser_id = data.get("loser_id")
    beers = data.get("beers")

    print("Received transaction data:", data)  # Debug log

    # Validate input data
    if not winner_id or not loser_id or not beers:
        raise HTTPException(status_code=400, detail="Invalid data")

    try:
        # Call the do_transaction function
        result = do_transaction(winner_id, loser_id, beers)
        return result
    except Exception as e:
        print("Error in transaction:", e)
        raise HTTPException(status_code=500, detail="Transaction failed")
