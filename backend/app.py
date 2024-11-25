
from flask import Flask, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# Load the timetable
timetable = {}

@app.route('/upload', methods=['POST'])
def upload_timetable():
    global timetable
    file = request.files.get('file')
    if file:
        timetable = json.load(file)
        return jsonify({"message": "Timetable uploaded successfully!"}), 200
    return jsonify({"error": "No file provided"}), 400

@app.route('/free-now', methods=['GET'])
def free_now():
    global timetable
    day = datetime.now().strftime('%A')
    current_time = datetime.now().strftime('%H:%M')
    
    if day not in timetable:
        return jsonify({"error": "No timetable available for today"}), 400
    
    for slot in timetable[day]:
        if slot['start'] <= current_time <= slot['end']:
            return jsonify({"free_now": []}), 200
    
    return jsonify({"free_now": "Everyone is free"}), 200

@app.route('/free-next', methods=['GET'])
def free_next():
    global timetable
    day = datetime.now().strftime('%A')
    current_time = datetime.now().strftime('%H:%M')
    
    if day not in timetable:
        return jsonify({"error": "No timetable available for today"}), 400
    
    for slot in timetable[day]:
        if slot['start'] > current_time:
            return jsonify({"free_next": slot['class']}), 200
    
    return jsonify({"free_next": "No more classes today"}), 200

if __name__ == '__main__':
    app.run(debug=True)
