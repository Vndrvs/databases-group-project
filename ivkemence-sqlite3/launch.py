from data_init import database_initializer, seed_data_initializer
from db_query import db_query
from db_clean import Union_Clean_Database
from db_clean_from_stats import Union_Clean_Database_76

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

        Union_Clean_Database()
        Union_Clean_Database_76()
        
        
    except Exception as e:
        print(f"Hiba a folyamat soran: {e}")

if __name__ == "__main__":
    main()