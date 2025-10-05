import csv
import os
from datetime import datetime

def run(cursor):
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "Adagok.csv"))

    try:
        with open(csv_path, newline="", encoding="cp852") as file:
            # use semicolon delimiter
            reader = csv.reader(file, delimiter=';')
            headers = next(reader)  # skip header row

            for i, row in enumerate(reader, start=2):
                # skip empty rows or invalid rows
                if not row or not row[0].strip().isdigit():
                    continue

                try:
                    # parse Adag_ID
                    adag_id = int(row[0].strip())

                    # parse start datetime
                    start_dt = datetime.strptime(f"{row[1].strip()} {row[2].strip()}", "%Y.%m.%d %H:%M:%S")
                    start_datetime = start_dt.isoformat(sep=' ')

                    # parse end datetime
                    end_dt = datetime.strptime(f"{row[3].strip()} {row[4].strip()}", "%Y.%m.%d %H:%M:%S")
                    vege_datetime = end_dt.isoformat(sep=' ')

                    # Adagido_Perc (optional)
                    adagido_perc = int(row[6].strip()) if row[6].strip() else None

                    # insert into database
                    cursor.execute("""
                        INSERT OR IGNORE INTO Adagok
                        (Adag_ID, Start_IdoDatum, Vege_IdoDatum, Adagido_Perc)
                        VALUES (?, ?, ?, ?)
                    """, (adag_id, start_datetime, vege_datetime, adagido_perc))

                except Exception as e:
                    print(f"Sor {i} hiba miatt atugorva: {e}")

        print("Adagok seeding sikeres.")

    except FileNotFoundError:
        print(f"Adagok.csv file nem talalhato: {csv_path}")
    except Exception as e:
        print(f"Hiba az adagok.csv file olvasasa soran: {e}")