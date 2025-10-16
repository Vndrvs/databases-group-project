import sqlite3
import os
from .seeders import seed_batches, seed_panels, seed_measurements

DATABASE_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database", "ivkemence_database.sqlite3"))

def seed_database():
    try:
        # connect to the database         
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            # run seeders
            seed_batches.run(cursor)
            seed_panels.run(cursor)
            seed_measurements.run(cursor)
            print("Seeding folyamat befejezve.")

    except Exception as e:
        print(f"Hiba a seeding soran: {e}")