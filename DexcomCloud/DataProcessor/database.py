import psycopg2
from psycopg2.extras import RealDictCursor
import os

def get_db_connection():
    """Retourne une connexion à la base de données PostgreSQL."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", 5432),
        database=os.getenv("DB_NAME", "dexcom"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "password"),
        cursor_factory=RealDictCursor
    )

def create_tables():
    """Crée les tables nécessaires si elles n'existent pas."""
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS validated_data (
            id SERIAL PRIMARY KEY,
            sensor_id VARCHAR(50),
            glucose_level NUMERIC,
            status VARCHAR(50),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS alerts (
            id SERIAL PRIMARY KEY,
            type VARCHAR(50),
            message TEXT,
            glucose_level NUMERIC,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    connection.commit()
    cursor.close()
    connection.close()
