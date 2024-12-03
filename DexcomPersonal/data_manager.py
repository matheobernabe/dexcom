import sqlite3
from datetime import datetime, timedelta
import pandas as pd

class DataManager:
    def __init__(self, db_path="dexcom_personal.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialise la base de données"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS glucose_readings (
                    timestamp TEXT,
                    glucose_level REAL
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS insulin_records (
                    timestamp TEXT,
                    units REAL,
                    type TEXT
                )
            ''')

    def add_glucose_reading(self, timestamp, glucose_level):
        """Ajoute une lecture de glucose"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                'INSERT INTO glucose_readings VALUES (?, ?)',
                (timestamp.isoformat(), glucose_level)
            )

    def add_insulin_record(self, record):
        """Ajoute un enregistrement d'insuline"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                'INSERT INTO insulin_records VALUES (?, ?, ?)',
                (record['timestamp'].isoformat(), record['units'], record['type'])
            )

    def get_glucose_history(self, hours=24):
        """Récupère l'historique des glycémies"""
        since = datetime.now() - timedelta(hours=hours)
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(
                'SELECT * FROM glucose_readings WHERE timestamp > ?',
                conn,
                params=(since.isoformat(),)
            )
        return df

    def get_insulin_history(self, hours=24):
        """Récupère l'historique des doses d'insuline"""
        since = datetime.now() - timedelta(hours=hours)
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(
                'SELECT * FROM insulin_records WHERE timestamp > ?',
                conn,
                params=(since.isoformat(),)
            )
        return df