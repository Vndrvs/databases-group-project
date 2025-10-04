import sqlite3

def run(cursor):
    try:
         # mivel a feladat leirasa tartalmazta a hutopanelek szamat, nem szukseges figyelembe vennunk, hogy a csv-bol hianyzik egy panel adatsora
        panel_ids = list(range(1, 16))

        for panel_id in panel_ids:
            cursor.execute("""
                INSERT OR IGNORE INTO Hutopanelek (Panel_ID)
                VALUES (?)
            """, (panel_id,))

        print("Hutopanelek seeding sikeres.")

    except Exception as e:
        print(f"Hiba a Hutopanelek seeding soran: {e}")