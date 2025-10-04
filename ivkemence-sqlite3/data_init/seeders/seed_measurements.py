import csv
import os
from datetime import datetime

def run(cursor):
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "Hűtőpanelek.csv"))

    try:
        # fetch all batches
        cursor.execute("SELECT Adag_ID, Start_IdoDatum, Vege_IdoDatum FROM Adagok")
        batches = cursor.fetchall()

        # convert datetime strings to datetime objects
        batches = [
            (adag_id, datetime.fromisoformat(start.strip()), datetime.fromisoformat(end.strip()))
            for adag_id, start, end in batches
        ]

        with open(csv_path, newline="", encoding="cp852") as file:
            reader = csv.reader(file, delimiter=";")
            headers = next(reader)

            num_panels = len(headers) // 2

            inserted = 0
            skipped = 0

            for row_index, row in enumerate(reader, start=2):
                for panel_index in range(num_panels):
                    panel_id = panel_index + 1
                    time_col = panel_index * 2
                    value_col = time_col + 1

                    time_str = row[time_col].strip()
                    value_str = row[value_col].strip()

                    if not time_str or not value_str:
                        skipped += 1
                        continue

                    try:
                        meas_time = datetime.strptime(time_str, "%Y.%m.%d %H:%M:%S")
                        temperature = float(value_str.replace(",", "."))

                        # find batch that the measurement belongs to
                        adag_id = None
                        for b_id, start_dt, end_dt in batches:
                            if start_dt <= meas_time <= end_dt:
                                adag_id = b_id
                                break

                        if adag_id is None:
                            print(f"Sor {row_index} panel {panel_id}: nem talalhato megfelelo adag ID")
                            skipped += 1
                            continue

                        cursor.execute("""
                            INSERT INTO Meresek (Panel_ID, Adag_ID, Meres_IdoDatum, Homerseklet_C)
                            VALUES (?, ?, ?, ?)
                        """, (panel_id, adag_id, meas_time.isoformat(sep=' '), temperature))
                        inserted += 1

                    except Exception as e:
                        print(f"Sor {row_index} panel {panel_id} hiba miatt atugorva: {e}")
                        skipped += 1

        print(f"Meresek seeding sikeres.")

    except FileNotFoundError:
        print(f"Hűtőpanelek.csv file nem talalhato: {csv_path}")
    except Exception as e:
        print(f"Hiba a Hűtőpanelek.csv file olvasasa soran: {e}")