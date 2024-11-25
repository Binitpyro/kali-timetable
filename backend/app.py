from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('timetable.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS timetable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT NOT NULL,
            start TEXT NOT NULL,
            end TEXT NOT NULL,
            class TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/add-timetable', methods=['POST'])
def add_timetable():
    data = request.json
    if not data or 'day' not in data or 'slots' not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    conn = sqlite3.connect('timetable.db')
    c = conn.cursor()
    for slot in data['slots']:
        c.execute('''
            INSERT INTO timetable (day, start, end, class)
            VALUES (?, ?, ?, ?)
        ''', (data['day'], slot['start'], slot['end'], slot['class']))
    conn.commit()
    conn.close()
    return jsonify({"message": f"Timetable for {data['day']} added successfully!"}), 200

@app.route('/free-now', methods=['GET'])
def free_now():
    day = datetime.now().strftime('%A')
    current_time = datetime.now().strftime('%H:%M')
    
    conn = sqlite3.connect('timetable.db')
    c = conn.cursor()
    c.execute('''
        SELECT class FROM timetable
        WHERE day = ? AND start <= ? AND end >= ?
    ''', (day, current_time, current_time))
    result = c.fetchall()
    conn.close()
    
    if result:
        return jsonify({"free_now": []}), 200
    return jsonify({"free_now": "Everyone is free"}), 200

@app.route('/free-next', methods=['GET'])
def free_next():
    day = datetime.now().strftime('%A')
    current_time = datetime.now().strftime('%H:%M')
    
    conn = sqlite3.connect('timetable.db')
    c = conn.cursor()
    c.execute('''
        SELECT class, start FROM timetable
        WHERE day = ? AND start > ?
        ORDER BY start ASC
        LIMIT 1
    ''', (day, current_time))
    result = c.fetchone()
    conn.close()
    
    if result:
        return jsonify({"free_next": {"class": result[0], "start": result[1]}}), 200
    return jsonify({"free_next": "No more classes today"}), 200

if __name__ == '__main__':
    app.run(debug=True)
