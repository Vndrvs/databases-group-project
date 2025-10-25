import sqlite3
import os

# path to sqlite database
DATABASE_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database"))
os.makedirs(DATABASE_FOLDER, exist_ok=True)
DATABASE_FILE = os.path.join(DATABASE_FOLDER, "ivkemence_database.sqlite3")

# path to schema
SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "create_schema.sql")

def initialize_database():
    print("Initialize function started")
    print("ITT:", os.path.isfile(DATABASE_FILE))
    if os.path.isfile(DATABASE_FILE):
        # returns False if database already exists
        return False
    try:
        # create our database
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        # read and execute our schema
        with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())

        #make the changes
        conn.commit()
        conn.close()
        print(f"Adatbazis letrehozva: {DATABASE_FILE}")
        
        # returns True if database is newly created
        return True
    except Exception as e:
        print(f"Hiba az adatbazis letrehozasa soran: {e}")