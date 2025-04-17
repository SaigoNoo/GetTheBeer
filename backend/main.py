from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from db_utils import recup, create_account, get_username
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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