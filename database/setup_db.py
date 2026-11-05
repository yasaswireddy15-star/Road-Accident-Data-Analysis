from database.connection import init_db, DATABASE_URL
if __name__ == "__main__":
    init_db()
    print("Database tables are ready.")
    print(f"Configured database: {DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else DATABASE_URL}")
