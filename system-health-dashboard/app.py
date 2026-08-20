import psutil
import os 
from flask import Flask, jsonify, render_template

app = Flask(__name__)

def get_system_info():
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
        "load_average": psutil.getloadavg() if hasattr(psutil, 'getloadavg') else [0, 0, 0]
    }

@app.route('/api/system-info')
def system_info():
    return jsonify(get_system_info())
@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
