from data_init import database_initializer, seed_data_initializer
from db_query import db_query

def main():
    try:
        print("Adatbazis elokeszitese...")
        db_state = database_initializer.initialize_database()

        if db_state == True:
            print("Seeding megkezdese...")
            seed_data_initializer.seed_database()
            print("A folyamat sikeres.")
        
        print("Lekérdezés meginditása...")
        db_query()
        
        
    except Exception as e:
        print(f"Hiba a folyamat soran: {e}")

if __name__ == "__main__":
    main()