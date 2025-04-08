from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Hello World"}
