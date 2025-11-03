import sqlite3
import os

# path to database file
DATABASE_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "database", "ivkemence_database.sqlite3"))

def Union_Clean_Database():
    print("Meresi adatok tisztitasa...")
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        query = """
            CREATE TABLE IF NOT EXISTS Meresek_UNION AS
            SELECT DISTINCT
                meres_id,
                panel_id,
                adag_id,
                meres_idodatum,
                homerseklet_c
            FROM meresek
            WHERE homerseklet_c <= 100
            AND homerseklet_c IS NOT NULL
            AND meres_idodatum IS NOT NULL

            UNION

            SELECT DISTINCT
                m.meres_id,
                m.panel_id,
                m.adag_id,
                m.meres_idodatum,
                m.homerseklet_c
            FROM meresek m
            WHERE m.meres_id NOT IN (
                SELECT meres_id
                FROM meresek
                WHERE homerseklet_c > 100
                OR homerseklet_c IS NULL
                OR meres_idodatum IS NULL
            )
            AND m.homerseklet_c <= 100;

    """

        cursor.execute(query)
        conn.commit()

        conn.close()

        print("Meresek adatainak tisztitasa sikeres.")
        print("A 100 fok feletti ertekek eltavolitva.")
        print("Meresek_UNION tabla letrehozva.")

    except Exception as e:
        print(f"Hiba a meresek adatinak tisztitasa kozben: {e}")




