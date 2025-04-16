from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from db_utils import recup, create_account, get_friends

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
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint d'inscription
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

# Endpoint pour récupérer les amis d’un utilisateur
@app.get("/api/friends/{user_id}")
def friends(user_id: int):
    try:
        return {"amis": get_friends(user_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
