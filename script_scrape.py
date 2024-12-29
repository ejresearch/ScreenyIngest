import sqlite3
import json
from bs4 import BeautifulSoup
import requests

# Initialize the database
def init_db():
    conn = sqlite3.connect("sql_screenplays.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS screenplays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            metadata TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

# Save to SQLite database
def save_to_db(title, content, metadata):
    try:
        conn = sqlite3.connect("sql_screenplays.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO screenplays (title, content, metadata) VALUES (?, ?, ?)",
            (title, content, json.dumps(metadata))
        )
        conn.commit()
        conn.close()
        print(f"Screenplay '{title}' saved to database.")
    except Exception as e:
        print(f"Error saving '{title}' to database: {e}")

# Fetch screenplay content from a URL
def fetch_screenplay(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        # Fetch the screenplay page
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse the page
        soup = BeautifulSoup(response.text, "html.parser")
        content = soup.find("pre")  # Most IMSDb screenplays are inside <pre> tags
        if content:
            return content.text.strip()
        else:
            print(f"No screenplay content found at {url}.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching screenplay from {url}: {e}")
        return None

# Main function
if __name__ == "__main__":
    init_db()

    # Example usage
    url = "https://imsdb.com/scripts/Clueless.html"
    screenplay_content = fetch_screenplay(url)
    if screenplay_content:
        metadata = {"source": url}
        save_to_db("Clueless", screenplay_content, metadata)

