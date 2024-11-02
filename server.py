from flask import Flask, jsonify, request
import os
from datetime import datetime

app = Flask(__name__)

# In-memory database to simulate recovery systems and event logs
recovery_systems = []
event_log = []
log_file = 'event_logs.txt'

# Ensure the log file and directory exist
if not os.path.exists(log_file):
    with open(log_file, 'w') as f:
        f.write("Event Logs:\n")

def log_event(message):
    # Append event to log file and in-memory event log
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    with open(log_file, 'a') as f:
        f.write(log_entry + '\n')
    event_log.append(log_entry)

# Endpoint to list all recovery systems
@app.route('/v2/systems', methods=['GET'])
def get_systems():
    return jsonify(recovery_systems), 200

# Endpoint to create a new recovery system
@app.route('/v2/systems', methods=['POST'])
def create_system():
    new_system = request.json
    new_system['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_system['status'] = "active"
    recovery_systems.append(new_system)
    log_event(f"Created system: {new_system['name']}")
    return jsonify(new_system), 201

# Endpoint to reboot the system to recovery mode
@app.route('/v2/reboot', methods=['POST'])
def reboot_to_recovery_mode():
    system_name = request.json.get("name", "Unknown")
    log_event(f"Rebooted system: {system_name} to recovery mode.")
    return jsonify({"message": f"{system_name} rebooting to recovery mode..."}), 200

# Endpoint to get event logs
@app.route('/v2/logs', methods=['GET'])
def get_event_logs():
    with open(log_file, 'r') as f:
        logs = f.readlines()
    return jsonify(logs), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)