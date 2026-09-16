from flask import Flask, request, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "collected_data.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            received_at TEXT NOT NULL,
            participant_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            cli_score REAL,
            interpretation TEXT,
            cpm REAL,
            backspace_ratio REAL,
            pause_ratio REAL,
            mouse_rate REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/upload", methods=["POST"])
def upload():
    data = request.get_json()
    
    if not data or "records" not in data:
        return jsonify({"error": "Invalid payload. Expected {'records': [...]}"}), 400
    
    records = data["records"]
    if not records:
        return jsonify({"error": "No records provided"}), 400
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    inserted = 0
    for record in records:
        cursor.execute("""
            INSERT INTO submissions 
            (received_at, participant_id, timestamp, cli_score, interpretation, cpm, backspace_ratio, pause_ratio, mouse_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            record.get("participant_id", "unknown"),
            record.get("timestamp", ""),
            record.get("cli_score", 0),
            record.get("interpretation", ""),
            record.get("cpm", 0),
            record.get("backspace_ratio", 0),
            record.get("pause_ratio", 0),
            record.get("mouse_rate", 0),
        ))
        inserted += 1
    
    conn.commit()
    conn.close()
    
    return jsonify({
        "success": True,
        "inserted": inserted,
        "message": f"Received {inserted} records."
    }), 200

@app.route("/stats", methods=["GET"])
def stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(DISTINCT participant_id) FROM submissions")
    participants = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM submissions")
    total_rows = cursor.fetchone()[0]
    
    cursor.execute("SELECT AVG(cli_score) FROM submissions")
    avg_score = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        "participants": participants,
        "total_records": total_rows,
        "average_cli": round(avg_score, 2) if avg_score else 0
    })

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "CLiP server running", "version": "1.0"})

if __name__ == "__main__":
    print("[Server] CLiP data collection server starting...")
    print("[Server] Endpoint: POST http://localhost:5000/upload")
    print("[Server] Stats:    GET  http://localhost:5000/stats")
    app.run(host="0.0.0.0", port=5000, debug=False)