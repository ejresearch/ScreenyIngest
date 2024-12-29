import sqlite3
import json
from sentence_transformers import SentenceTransformer
import os

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def fetch_screenplays_from_sql(db_path):
    """Fetches screenplays and metadata from the SQL database."""
    print(f"Connecting to database at {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT title, content, metadata FROM screenplays")
    rows = cursor.fetchall()
    conn.close()

    print(f"Fetched {len(rows)} screenplays from the database.")
    screenplays = []
    for i, row in enumerate(rows):
        title, content, metadata_json = row
        metadata = json.loads(metadata_json)
        print(f"Processing screenplay {i + 1}: {title}")
        screenplays.append({"title": title, "content": content, "metadata": metadata})
    return screenplays

def dump_to_json(screenplays, output_dir):
    """Generates embeddings and saves screenplays as JSON for LightRAG."""
    os.makedirs(output_dir, exist_ok=True)
    print(f"Saving JSON files to {output_dir}...")

    for i, screenplay in enumerate(screenplays):
        print(f"Generating embedding for screenplay {i + 1}/{len(screenplays)}: {screenplay['title']}")

        # Generate embedding
        embedding = model.encode(screenplay["content"])

        # Prepare JSON structure
        lightrag_entry = {
            "title": screenplay["title"],
            "content": screenplay["content"],
            "metadata": screenplay["metadata"],
            "embedding": embedding.tolist()
        }

        # Save to JSON file
        filename = f"{screenplay['title'].replace(' ', '_')}.json"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w") as f:
            json.dump(lightrag_entry, f, indent=4)
        print(f"Saved {screenplay['title']} to {filepath}")

if __name__ == "__main__":
    db_path = "sql_screenplays.db"  # Path to SQLite database
    output_dir = "./lightrag_data"  # Output directory for LightRAG JSON files
