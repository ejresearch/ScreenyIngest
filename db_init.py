import sqlite3

def init_db():
    """Initializes the SQLite database and creates the screenplays table if it doesn't exist."""
    try:
        print("Connecting to database...")
        conn = sqlite3.connect("sql_screenplays.db")  # Use the correct filename
        cursor = conn.cursor()

        # Create the screenplays table
        print("Creating table if it doesn't exist...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS screenplays (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata TEXT NOT NULL
            )
        """)
        conn.commit()
        print("Table created successfully.")
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == "__main__":
    init_db()

