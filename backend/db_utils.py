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

def get_username(user_id):
    try:
        query = "SELECT pseudo FROM utilisateurs WHERE user_ID = ?"
        cur.execute(query, (user_id,))
        result = cur.fetchone()
        return result[0] if result else None
    except Exception as e:
        print("Erreur : ", e)
        return None



def create_account(nom, prenom, pseudo, mail, motdepasse, biographie):
    try:
        # Requête SQL préparée
        query = "INSERT INTO utilisateurs (nom, prenom, pseudo, mail, motdepasse, biographie, ID_level) VALUES (?, ?, ?, ?, ?, ?, 1);"
        cur.execute(query, (nom, prenom, pseudo, mail, motdepasse, biographie))
        conn.commit()  # Important : valider la transaction

        # Récupérer l'ID du dernier utilisateur inséré
        cur.execute("SELECT LAST_INSERT_ID();")
        user_id = cur.fetchone()[0]
        return user_id
    except Exception as e:
        print(f"Erreur lors de la création du compte : {e}")
        conn.rollback()  # Annuler la transaction en cas d'erreur
        return str(e)