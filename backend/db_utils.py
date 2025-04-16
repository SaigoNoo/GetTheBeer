# Module Imports
import mariadb
import sys
print(mariadb.__file__)
import mysql.connector
from mysql.connector import Error
# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
    user="myuser",
    password="mypassword",
    host="mariadb_container",  # <-- très important !
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
    print("test")
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

def get_friends(user_id):
    try:
        connection = mysql.connector.connect(
            host="mariadb",  # ou "localhost" si tu es hors Docker
            user="myuser",
            password="mypassword",
            database="mydatabase"
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT u.user_ID, u.nom, u.prenom, u.pseudo, u.mail, u.image
                FROM utilisateurs u
                JOIN amis a ON 
                    (u.user_ID = a.IDuser1 AND a.IDuser2 = %s)
                    OR (u.user_ID = a.IDuser2 AND a.IDuser1 = %s)
                WHERE u.user_ID != %s;
            """

            cursor.execute(query, (user_id, user_id, user_id))
            friends = cursor.fetchall()

            return friends

    except Error as e:
        raise Exception(f"Erreur de connexion à la base de données : {str(e)}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()