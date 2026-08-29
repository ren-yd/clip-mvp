import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "clip_data.db")

class Database:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cli_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                cli_score REAL NOT NULL,
                interpretation TEXT,
                features TEXT,
                breakdown TEXT
            )
        """)
        conn.commit()
        conn.close()
    
    def insert(self, score, interpretation, features, breakdown):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO cli_snapshots (timestamp, cli_score, interpretation, features, breakdown)
            VALUES (?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            score,
            interpretation,
            json.dumps(features),
            json.dumps(breakdown)
        ))
        conn.commit()
        conn.close()
    
    def get_history(self, limit=100):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT timestamp, cli_score, interpretation, features, breakdown
            FROM cli_snapshots
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        conn.close()
        return rows