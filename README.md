# GetTheBeer
## Rapide explicatif
### Base de données
Nous vous proposons de déployer par le moyen de votre choix votre base de donnée (dans notre cas MariaDB) !
Ensuite, executez le contenu de backend/database_init/tables.sql puis fctn_proc_trigger.sql !

# GetTheBeer
Projet de DEV 3 écrit en React JS niveau fronted et Python (FastAPI) pour la backend...

Pour lancer le projet, je vais vous fournir 3 captures d'écran pour tester via PyCharm !

## D'abord le .env Backend:
```ini
DB_SERVER=<ip_ou_dns_mysql>
DB_USERNAME=<username>
DB_PASSWORD=<password>
DB_NAME=<nom_db>
DB_PORT=3306
SMTP_EMAIL=info@doussis.be
SMTP_PASSWORD=<smtp_password>
SMTP_SERVER=ssl0.ovh.net
SMTP_PORT=587
SECRET_KEY=<si_pas_precisé_généré>
CORS_URL=<url_frontend>
BACKEND_URL=<url_backend_pour tests>
```

## Config PyCharm
### Backend:
![image](https://github.com/user-attachments/assets/51275bc0-1572-4b95-a86b-a349a8379ab6)
![image](https://github.com/user-attachments/assets/009fae7a-a716-4785-84dd-1fa37a869252)

### Frontend
> D'abord faire un npm install dans le dossier frontend
![image](https://github.com/user-attachments/assets/a8d98b57-7c66-4286-8e84-23a7b59ff49b)
![image](https://github.com/user-attachments/assets/84187914-b3b7-43c4-ab64-293674d5a003)

### Tests
![image](https://github.com/user-attachments/assets/56c06d21-2518-4272-a64f-4dad70f14a32)
![image](https://github.com/user-attachments/assets/437f9367-74ce-434c-912a-5d5f1d7a0e76)


### Modèles services systemctl:
#### Backend
```bash
[Unit]
Description=GTB_BACKEND
After=network.target

[Service]
User=debian
Group=users
WorkingDirectory=/home/debian/getTheBeer/backend
Environment="PATH=/home/debian/getTheBeer/backend/venv/bin"
ExecStart=/home/debian/getTheBeer/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

#### Frontend
```bash
[Unit]
Description=GTB_FRONTEND
After=network.target

[Service]
User=debian
Group=users
WorkingDirectory=/home/debian/getTheBeer/frontend
ExecStart=npm run dev

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```
