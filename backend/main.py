from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from db_utils import recup, create_account

class UserSignup(BaseModel):
    nom: str
    prenom: str
    pseudo: str
    mail: str
    motdepasse: str
    biographie: str

app = FastAPI()

# Liste des origines autorisées
origins = [
    "http://localhost:5173",  # React.js en développement
]

# Appliquer CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permettre l'accès uniquement depuis localhost:3000
    allow_credentials=True,
    allow_methods=["*"],  # Accepter toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Accepter tous les headers
)

# Base.metadata.create_all(bind=engine)
"""
@app.get("/")
def read_root():
    print(recup())
    return {"message": "Hello World"}
"""
# Nouvel endpoint pour l'inscription
@app.post("/api/signup")
def signup(user: UserSignup):
    try:
        success = create_account(
            user.nom,
            user.prenom,
            user.pseudo,
            user.mail,
            user.motdepasse,
            user.biographie
        )

        if success:
            return {"message": "Inscription réussie!"}
        else:
            raise HTTPException(status_code=400, detail="Échec de l'inscription")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")

# Endpoint pour la connexion
class UserLogin(BaseModel):
    pseudo: str
    motdepasse: str

@app.post("/api/login")
def login(user: UserLogin):
    try:
        if verify_user(user.pseudo, user.motdepasse):
            return {"message": "Connexion réussie"}
        else:
            raise HTTPException(status_code=401, detail="Identifiants incorrects")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")
