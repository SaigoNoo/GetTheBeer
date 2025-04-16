# Module Imports
import mariadb
import sys
print(mariadb.__file__)
# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="myuser",
        password="mypassword",
        host="localhost",
        port=3306,
        database="mydatabase"
    )
except Exception as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    print(f"Error connecting to MariaDB Platform")
    sys.exit(1)

# Get cursor
cur = conn.cursor()


def recup():
    cur.execute("SELECT * FROM utilisateurs;")
    print(cur.fetchall())


def create_account(nom, prenom, pseudo, mail, motdepasse, biographie):
    try:
        # Requête SQL préparée pour éviter les injections SQL
        query = f"INSERT INTO utilisateurs (nom, prenom, pseudo, mail, motdepasse, biographie) VALUES (?, ?, ?, ?, ?, ?)"
        cur.execute(query, (nom, prenom, pseudo, mail, motdepasse, biographie))
        conn.commit()  # Important : valider la transaction
        return True
    except Exception as e:
        print(f"Erreur lors de la création du compte : {e}")
        conn.rollback()  # Annuler la transaction en cas d'erreur
        return False


def verify_user(pseudo, motdepasse):
    try:
        cur.execute("SELECT * FROM utilisateurs WHERE pseudo = ? AND motdepasse = ?", (pseudo, motdepasse))
        user = cur.fetchone()

        if user:
            return True
        else:
            print(f"Utilisateur non trouvé pour pseudo: {pseudo}")
            return False
    except Exception as e:
        print(f"Erreur lors de la vérification de l'utilisateur : {e}")
        return False
