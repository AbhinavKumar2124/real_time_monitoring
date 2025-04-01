from flask import Flask, jsonify, request
from flask_cors import CORS
import psutil
import time
import os #for alerts file
import json #for alerts file

app = Flask(__name__)
CORS(app)

#-----------------------------------------------------------------------------------------
ALERTS_FILE = "alerts.json"

# Load saved alerts (if exists)
if os.path.exists(ALERTS_FILE):
    with open(ALERTS_FILE, "r") as f:
        alert_settings = json.load(f)
else:
    alert_settings = {"cpu": 90, "memory": 90, "disk": 90, "enabled": True}


@app.route('/api/set_alerts', methods=['POST'])
def set_alerts():
    global alert_settings
    data = request.json
    alert_settings.update(data)
    print("\n",alert_settings,"\n")
    with open(ALERTS_FILE, "w") as f:
        json.dump(alert_settings, f)

    return jsonify({"message": "Alerts updated", "alerts": alert_settings})


@app.route('/api/get_alerts', methods=['GET'])
def get_alerts():
    return jsonify(alert_settings)


@app.route('/api/check_alerts', methods=['GET'])
def check_alerts():
    if not alert_settings["enabled"]:
        return jsonify({"alerts": []})  

    alerts_triggered = []
    
    # Check CPU
    if psutil.cpu_percent(interval=1) > alert_settings["cpu"]:
        alerts_triggered.append("⚠ High CPU Usage!")

    # Check Memory
    if psutil.virtual_memory().percent > alert_settings["memory"]:
        alerts_triggered.append("⚠ High Memory Usage!")

    # Check Disk
    if psutil.disk_usage('/').percent > alert_settings["disk"]:
        alerts_triggered.append("⚠ High Disk Usage!")

    return jsonify({"alerts": alerts_triggered})


@app.route('/api/toggle_alerts', methods=['POST'])
def toggle_alerts():
    global alert_settings
    alert_settings["enabled"] = request.json.get("enabled", True)
    
    with open(ALERTS_FILE, "w") as f:
        json.dump(alert_settings, f)

    return jsonify({"message": f"Alerts {'enabled' if alert_settings['enabled'] else 'disabled'}."})
#-----------------------------------------------------------------------------------------


@app.route('/api/system_stats', methods=['GET'])
def get_system_stats():
    '''
    stats = {
        "cpu_cores": psutil.cpu_count(logical=True),
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent
    }'''

    cpu_usage = psutil.cpu_percent(interval=1)

    mem = psutil.virtual_memory()
    memory_stats = {
        "total": round(mem.total / (1024**3), 2),
        "used": round(mem.used / (1024**3), 2),
        "percent": mem.percent,
        "available": round(mem.available / (1024**3), 2),
        "standby": round((mem.available - mem.free) / (1024**3), 2)
    }

    disk = psutil.disk_usage('/')
    disk_stats = {
        "total": round(disk.total / (1024**3), 2),
        "used": round(disk.used / (1024**3), 2),
        "percent": disk.percent,
        "free": round(disk.free / (1024**3), 2)
    }

    net = psutil.net_io_counters()
    network_stats = {
        "bytes_sent": round(net.bytes_sent / (1024**2), 2),
        "bytes_recv": round(net.bytes_recv / (1024**2), 2)
    }

    stats = {
        "cpu": cpu_usage,
        "memory": memory_stats,
        "disk": disk_stats,
        "network": network_stats,
        "timestamp": int(time.time())
    }

    return jsonify(stats)

STATUS_MAPPING = {
    "running": "🟢 Active",
    "stopped": "🔴 Halted",
    "sleeping": "🟡 Idle",
    "zombie": "⚫ Defunct(zombie)"
}
#-----------------------------------------------------------------------------------------
@app.route('/api/processes', methods=['GET'])
def get_processes():
    process_list = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status']):
        proc_info = proc.info
        original_status = proc_info.get("status", "").lower()
        proc_info["status"] = STATUS_MAPPING.get(original_status, f"⚪ {original_status.capitalize()}")
        process_list.append(proc_info)
    return jsonify(process_list)
#-----------------------------------------------------------------------------------------
@app.route('/api/process_manager', methods=['POST'])
def process_manager():
    try:
        data = request.json
        pid = int(data['pid'])
        action = data['action']
        process = psutil.Process(pid)
        print("\n",pid,"\n")
        print("\n",action,"\n")
        if action == "Pause":
            process.suspend()
            message = f"Process {pid} paused successfully."
        elif action == "Resume":
            process.resume()
            message = f"Process {pid} resumed successfully."
        elif action == "Kill":
            process.terminate()
            message = f"Process {pid} terminated successfully."
        else:
            return jsonify({"status": "error", "message": "Invalid action."})
        
        return jsonify({"status": "success", "message": message})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
#-----------------------------------------------------------------------------------------          


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
