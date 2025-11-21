import sqlite3
import os

def update_schema():
    db_path = os.path.join(os.path.dirname(__file__), '../data/gitta.db')
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    
    print(f"Updating database at {db_path}")
    
    if not os.path.exists(schema_path):
        print(f"Schema file not found at {schema_path}")
        return

    try:
        conn = sqlite3.connect(db_path)
        with open(schema_path, 'r') as f:
            schema = f.read()
        conn.executescript(schema)
        conn.commit()
        conn.close()
        print("Database schema updated successfully.")
    except Exception as e:
        print(f"Error updating database: {e}")

if __name__ == "__main__":
    update_schema()
