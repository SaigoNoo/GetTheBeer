FROM python:3.11-slim

# 🔧 Ajout de la dépendance système manquante
RUN apt-get update && \
    apt-get install -y gcc libmariadb-dev netcat-openbsd && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

# 🔁 Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

CMD ["/wait-for-it.sh", "mariadb_container", "3306", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
