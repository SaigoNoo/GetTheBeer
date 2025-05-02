# GetTheBeer
Projet de DEV 3 écrit en React JS niveau fronted et Python (FastAPI) pour la backend...

## Installation en local

Copier la branche dev

### ReactJS
Aller dans le dossier frontend, faire
npm install
npm run dev

### MariaDB
(Si vous travaillez sur Windows, ne pas oubblier de démarrer Docker Desktop)

Aller dans le dossier backend

Il faut après faire
docker-compose up

Il faut ensuite faire
docker exec -it mariadb_container mariadb -umyuser -pmypassword mydatabase
Ce qui ouvrira un terminal MariaDB qui sert à mettre des instructions SQL.

### FastAPI
Aller dans le dossier backend
Pour lancer le backend, il faut créer le venv :

python -m venv venv

.\venv\Scripts\activate

pip install fastapi uvicorn python-dotenv sqlalchemy mariadb itsdangerous bcrypt

uvicorn main:app --reload
