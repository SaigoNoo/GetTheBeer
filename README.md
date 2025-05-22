# GetTheBeer
## Rapide explicatif
### Base de données
Nous vous proposons de déployer par le moyen de votre choix votre base de donnée (dans notre cas MariaDB) !
Ensuite, executez le contenu de backend/database_init/tables.sql puis fctn_proc_trigger.sql !

### Backend
#### Exemple de .env
```dotenv
DB_SERVER=doussis.be
DB_USERNAME=username
DB_PASSWORD=password
DB_NAME=getTheBeer
DB_PORT=3306
SMTP_EMAIL=info@doussis.be
SMTP_PASSWORD=password
SMTP_SERVER=ssl0.ovh.net
SMTP_PORT=587
SECRET_KEY=TO_SET_OR_AUTO
```
```bash
cd Backend
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
uvicorn main:app
```

### Frontend
```bash
npm install
npm run dev
```

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