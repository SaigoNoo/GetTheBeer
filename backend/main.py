from fastapi import FastAPI, HTTPException, Request, status
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from db_utils import recup, create_account, get_username, login_db
from passlib.context import CryptContext    #Crypter le mot de passe

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
    secret_key="votre_cle_secrete",
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

@app.get("/")
def read_root():
    #print(recup())
    return {"message": "Hello World"}



# Nouvel endpoint pour l'inscription
@app.post("/api/signup")
def signup(user: UserSignup):
    try:
        hashed_password = pwd_context.hash(user.motdepasse)

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
    if pwd_context.verify(password, user_id[1]):
        request.session["user_id"] = user_id[0]
        return {"success": True, "message": "Connexion réussie"}
    else:
        return {"success": False, "message": "Mot de passe incorrect"}

@app.post("/api/logout")
async def logout(request: Request):
    request.session.clear()
    return {"message": "Déconnexion réussie"}