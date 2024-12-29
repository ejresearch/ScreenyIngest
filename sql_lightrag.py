import sqlite3
from lightrag import LightRAG
from lightrag.llm import gpt_4o_mini_complete  # Replace with your preferred model

# Paths and working directory
DB_PATH = "./sql_screenplays.db"
WORKING_DIR = "./lightrag_data"

# Initialize LightRAG
rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=gpt_4o_mini_complete  # Replace with your model function
)

def fetch_data_from_sqlite(db_path):
    """Fetch data from SQLite database."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Replace 'screenplays' with your table name and adjust column names as needed
        cursor.execute("SELECT id, title, content FROM screenplays")
        rows = cursor.fetchall()

        # Convert rows to a list of documents
        documents = [{"id": row[0], "title": row[1], "content": row[2]} for row in rows]
        conn.close()

        return documents
    except Exception as e:
        print(f"Error fetching data from SQLite: {e}")
        return []

def ingest_documents_to_lightrag(documents):
    """Ingest documents into LightRAG."""
    for doc in documents:
        # Prepare document text
        doc_text = f"Title: {doc['title']}\n\nContent: {doc['content']}"

        # Insert document into LightRAG
        rag.insert(doc_text)
        print(f"Ingested document ID: {doc['id']}")

if __name__ == "__main__":
    # Fetch data from SQLite
    documents = fetch_data_from_sqlite(DB_PATH)

    if documents:
        print(f"Fetched {len(documents)} documents from the database.")

        # Ingest data into LightRAG
        ingest_documents_to_lightrag(documents)
        print("Ingestion completed.")
    else:
        print("No documents found in the database.")

