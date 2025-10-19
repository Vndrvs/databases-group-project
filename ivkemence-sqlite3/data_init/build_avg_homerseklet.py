import sqlite3
import os

# path to database file
DATABASE_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database", "ivkemence_database.sqlite3"))

def build_database():
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        query = """
            CREATE TABLE IF NOT EXISTS Adagok_AVG_Ho AS
            SELECT 
                a.adag_id,
                a.start_idodatum,
                a.vege_idodatum,
                a.adagido_perc,
                (
                    SELECT AVG(m.homerseklet_c)
                    FROM meresek m
                    WHERE m.adag_id = a.adag_id
                ) AS Atlag_Homerseklet
            FROM adagok a
            WHERE a.adag_id IN (SELECT DISTINCT adag_id FROM meresek);
            """

        cursor.execute(query)
        conn.commit()

        conn.close()

    except Exception as e:
        print(f"Hiba az adatbazis letrehozasa soran: {e}")

