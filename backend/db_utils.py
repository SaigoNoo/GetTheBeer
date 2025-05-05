import mariadb
import sys
import bcrypt
import traceback

try:
    conn = mariadb.connect(
        user="myuser",
        password="mypassword",
        host="mariadb_container",
        port=3306,
        database="mydatabase"
    )
except Exception as e:
    print(f"Erreur de connexion à MariaDB : {e}")
    sys.exit(1)

cur = conn.cursor()


def create_account(nom, prenom, pseudo, mail, motdepasse, biographie):
    try:
        query = """
        INSERT INTO utilisateurs (nom, prenom, pseudo, mail, motdepasse, biographie, ID_level)
        VALUES (?, ?, ?, ?, ?, ?, 1);
        """
        cur.execute(query, (nom, prenom, pseudo, mail, motdepasse, biographie))
        conn.commit()
        cur.execute("SELECT LAST_INSERT_ID();")
        return cur.fetchone()[0]
    except Exception as e:
        conn.rollback()
        print("Erreur création de compte:", e)
        return str(e)


def login_db(username):
    try:
        cur.execute("SELECT user_ID, motdepasse FROM utilisateurs WHERE pseudo = ?", (username,))
        return cur.fetchone()
    except Exception as e:
        print("Erreur login_db:", e)
        return None


def get_username(user_id):
    try:
        cur.execute("SELECT pseudo FROM utilisateurs WHERE user_ID = ?", (user_id,))
        result = cur.fetchone()
        return result[0] if result else None
    except Exception as e:
        print("Erreur get_username:", e)
        return None


def get_user_beer_reserve(user_id):
    try:
        cur.execute("SELECT reserve_biere FROM utilisateurs WHERE user_ID = ?", (user_id,))
        result = cur.fetchone()
        return result[0] if result else None
    except Exception as e:
        print("Erreur get_user_beer_reserve:", e)
        return None


def get_opponent(user_id):
    try:
        query = """
        SELECT user_ID AS id, pseudo, reserve_biere
        FROM utilisateurs
        WHERE user_ID != ?
        """
        cur.execute(query, (user_id,))
        columns = [desc[0] for desc in cur.description]
        return [dict(zip(columns, row)) for row in cur.fetchall()]
    except Exception as e:
        print("Erreur get_opponent:", e)
        return []


def do_transaction(winner_id, loser_id, beers):
    try:
        cur.execute("UPDATE utilisateurs SET reserve_biere = reserve_biere - ? WHERE user_ID = ?", (beers, loser_id))
        cur.execute("INSERT INTO transactions (debtor_ID, creditor_ID, beers_owed) VALUES (?, ?, ?)", (loser_id, winner_id, beers))
        conn.commit()
        return {"success": True, "message": "Transaction effectuée"}
    except Exception as e:
        conn.rollback()
        print("Erreur transaction:", e)
        return {"success": False, "message": "Erreur transaction"}


def recup(user_id):
    try:
        cur.execute("SELECT * FROM utilisateurs WHERE user_ID = ?", (user_id,))
        row = cur.fetchone()
        if row:
            columns = [desc[0] for desc in cur.description]
            return dict(zip(columns, row))
        else:
            return None
    except Exception as e:
        print("Erreur recup:", e)
        return None


def get_user_profile(user_id):
    try:
        cur.execute("SELECT pseudo, nom, prenom, mail, biographie FROM utilisateurs WHERE user_ID = ?", (user_id,))
        row = cur.fetchone()
        if row:
            columns = [desc[0] for desc in cur.description]
            return dict(zip(columns, row))
        else:
            return None
    except Exception as e:
        print("Erreur get_user_profile:", e)
        return None

def login_user(username, password):
    try:
        cur = conn.cursor()
        query = "SELECT * FROM utilisateurs WHERE pseudo = %s"
        cur.execute(query, (username,))
        user = cur.fetchone()

        if user:
            hashed_password = user[6]  # motdepasse (varbinary(60))

            # Ne surtout pas encoder hashed_password, il est déjà en bytes
            print("🔐 hashed_password type:", type(hashed_password))
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                return {"id": user[0], "pseudo": user[3]}  # id et pseudo
            else:
                return None
        else:
            return None
    except Exception as e:
        print("Erreur lors de la tentative de connexion :", e)
        traceback.print_exc()
        return None


def get_friends(user_id):
    try:
        cur.execute("""
            SELECT pseudo FROM utilisateurs 
            WHERE user_ID IN (
                SELECT IDuser2 FROM amis WHERE IDuser1 = %s
                UNION
                SELECT IDuser1 FROM amis WHERE IDuser2 = %s
            )
        """, (user_id, user_id))
        rows = cur.fetchall()
        friends = [{"pseudo": row[0]} for row in rows]  # Conversion tuple -> dict
        return friends
    except Exception as e:
        print(f"Erreur lors de la récupération des amis : {e}")
        return []


