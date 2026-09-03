import sqlite3
import csv
import json
import uuid
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "clip_data.db")

def export_data():
    """Export all local data to an anonymized CSV file."""
    if not os.path.exists(DB_PATH):
        print("No data found. Run the app first.")
        return None
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT timestamp, cli_score, interpretation, features, breakdown 
        FROM cli_snapshots 
        ORDER BY timestamp
    """)
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        print("Database is empty. No data to export.")
        return None
    
    # Generate anonymous participant ID
    participant_id = uuid.uuid4().hex[:12]
    filename = f"clip_export_{participant_id}.csv"
    filepath = os.path.join(os.path.dirname(__file__), filename)
    
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'participant_id', 'timestamp', 'cli_score', 
            'interpretation', 'cpm', 'backspace_ratio', 
            'pause_ratio', 'mouse_rate'
        ])
        
        for row in rows:
            ts, score, interp, features_json, _ = row
            features = json.loads(features_json)
            
            writer.writerow([
                participant_id,
                ts,
                score,
                interp,
                features.get('cpm', 0),
                features.get('backspace_ratio', 0),
                features.get('pause_ratio', 0),
                features.get('mouse_rate', 0),
            ])
    
    print(f"=" * 50)
    print(f"  EXPORT SUCCESSFUL")
    print(f"=" * 50)
    print(f"  File: {filename}")
    print(f"  Rows: {len(rows)}")
    print(f"  Participant ID: {participant_id}")
    print(f"=" * 50)
    print(f"  Send this file to the researcher via email.")
    print(f"  Location: {filepath}")
    print(f"=" * 50)
    
    return filepath

if __name__ == "__main__":
    export_data()