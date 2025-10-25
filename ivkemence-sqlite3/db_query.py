import sqlite3
import os


DATABASE_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "database", "ivkemence_database.sqlite3"))

def db_query():
    try:
        # connect to the database
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            # Average temperature, Adagidő query
            cursor.execute("""
                           SELECT
                                Meresek.Adag_ID,
                                a.Adagido_Perc,
                                AVG(Meresek.Homerseklet_C) AS Atlag_homerseklet_C
                           FROM Meresek
                           JOIN (SELECT Adagok.Adag_ID, Adagok.Adagido_Perc FROM Adagok) AS a
                           ON Meresek.Adag_ID = a.Adag_ID
                           GROUP BY a.Adag_ID;
                           """)
            results = cursor.fetchall()
            for row in results:
                print(f"Adag_ID: {row[0]}, Adagido_Perc: {row[1]}, Atlag_homerseklet_C: {row[2]}")


            print("Query befejezve.")
    except Exception as e:
        print(f"Hiba a lekerdezes soran")
        print(e)
        
    # Transaction példa
    try:
        print("Tranzakcio megkezdese dummy adatokkal...")
        conn.execute("BEGIN TRANSACTION;")
        cursor.execute("""
            INSERT INTO Adagok (Adag_ID, Adagido_Perc, Start_IdoDatum, Vege_IdoDatum)
            VALUES (33, 45, '2025-11-01 10:00:00', '2025-11-01 10:45:00');
        """)
        cursor.execute("""
            INSERT INTO Adagok (Adag_ID, Adagido_Perc, Start_IdoDatum, Vege_IdoDatum)
            VALUES (34, 42, '2025-11-02 10:00:00', '2025-11-02 10:45:00');
        """)
        conn.commit()
        print("Sikeres tranzakcio.")
        cursor.execute("""SELECT * 
                       FROM Adagok 
                       WHERE adag_ID = 33 
                       OR adag_ID = 34;""")
        results = cursor.fetchall()
        print("Beszurt adatok:")
        for row in results:
            print(f"Adag_ID: {row[0]}, Adagido_Perc: {row[1]}, Atlag_homerseklet_C: {row[2]}")
        print("Lekerdezes sikeres.")
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            print("Létezo Adag_ID miatt a tranzakcio meghiusult.")
            cursor.execute("""SELECT * 
                       FROM Adagok 
                       WHERE adag_ID = 33 
                       OR adag_ID = 34;""")
            results = cursor.fetchall()
            for row in results:
                print(f"Adag_ID: {row[0]}, Adagido_Perc: {row[1]}, Atlag_homerseklet_C: {row[2]}")
        else:       
            conn.rollback()
            print(e)
            print("Tranzakcio meghiusult")
    finally:
        conn.close()

