from data_init import database_initializer, seed_data_initializer

def main():
    try:
        print("Adatbazis elokeszitese...")
        database_initializer.initialize_database()

        print("Seeding megkezdese...")
        seed_data_initializer.seed_database()

        print("A folyamat sikeres.")

    except Exception as e:
        print(f"Hiba a folyamat soran: {e}")

if __name__ == "__main__":
    main()