import sqlite3
import json
from enum import Enum

DB_FILE = "ecocycle.db"

class ProviderType(Enum):
    RUMAH_TANGGA = 'Rumah Tangga'
    RESTO = 'Restoran'
    PASAR = 'Pasar'

class WasteCategory(Enum):
    SISA_MAKANAN = 'Sisa Makanan'
    SAYUR_BUAH = 'Sayur/Buah'
    LIMBAH_DAPUR = 'Limbah Dapur'
    TAMAN = 'Taman'

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database and creates the waste_posts table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS waste_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            provider_type TEXT NOT NULL,
            waste_category TEXT,
            suitable_for TEXT,
            weight_est REAL,
            lat REAL NOT NULL,
            lon REAL NOT NULL,
            contact_info TEXT,
            image_blob BLOB,
            ai_analysis TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()
    print("Database initialized.")

def add_waste_post(provider_type: ProviderType, lat: float, lon: float, image_blob: bytes, ai_analysis: dict, contact_info: str = None):
    """Adds a new waste post to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Extract data from AI analysis
    waste_category = ai_analysis.get('main_composition', 'Lainnya')
    suitable_for = ", ".join(ai_analysis.get('suitability_tags', []))
    weight_est = ai_analysis.get('estimated_weight_kg', 0.0)
    
    cursor.execute(
        """
        INSERT INTO waste_posts (provider_type, waste_category, suitable_for, weight_est, lat, lon, contact_info, image_blob, ai_analysis)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            provider_type.value,
            waste_category,
            suitable_for,
            weight_est,
            lat,
            lon,
            contact_info,
            image_blob,
            json.dumps(ai_analysis)
        )
    )
    conn.commit()
    post_id = cursor.lastrowid
    conn.close()
    return post_id

def get_waste_posts(filters: list = None):
    """
    Retrieves waste posts from the database.
    Can be filtered by a list of 'suitable_for' tags.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM waste_posts ORDER BY created_at DESC"
    
    if filters:
        # Creates a query like: WHERE suitable_for LIKE '%Filter1%' OR suitable_for LIKE '%Filter2%'
        where_clauses = [f"suitable_for LIKE '%{f.strip()}%'" for f in filters]
        query = f"SELECT * FROM waste_posts WHERE {' OR '.join(where_clauses)} ORDER BY created_at DESC"

    cursor.execute(query)
    posts = cursor.fetchall()
    conn.close()
    return [dict(row) for row in posts]

# Initialize the database when this module is imported
if __name__ == '__main__':
    print("Running DB setup...")
    init_db()
    print("DB setup complete.")
