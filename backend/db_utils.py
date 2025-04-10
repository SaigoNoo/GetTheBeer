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
    print("caca")
    cur.execute("SELECT * FROM utilisateurs;")
    print(cur.fetchall())