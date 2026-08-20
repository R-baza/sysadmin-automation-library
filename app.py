from flask import Flask, render_template, request, jsonify
from datetime import datetime
from google import genai
import os
import psutil
import subprocess
from dotenv import load_dotenv
from argus_sentinel import get_telemetry

load_dotenv()

app = Flask(__name__)
log_file_path = '/var/log/argus/argus.log'
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
chat_session = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "system_instruction": "You are ARGUS, an all-seeing mythological sentinel and systems administration assistant. Maintain historical context of the conversation and provide precise technical insights."
    }
)

@app.route('/')
def dashboard():
    system_data = get_telemetry()
    hour = datetime.now().hour
    if 5 <= hour < 12:
        greeting = "Good Morning"
    elif 12 <= hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"
        
    return render_template('index.html', data=system_data, greeting=greeting)

@app.route('/log')
def view_log():
    try:
        with open(log_file_path, 'r') as f:
            log_content = f.read()
            has_error = 'ERROR' in log_content
            return jsonify({"log": log_content, "error": has_error})
    except FileNotFoundError:
        return jsonify({"log": "Log file not found yet.", "error": False})

@app.route('/ask-ai', methods=['POST'])
def ask_ai():
    user_prompt = request.json.get('prompt', '')
    if not user_prompt:
        return jsonify({"response": "No prompt provided."})
    
    telemetry = get_telemetry()
    system_context = f"[System Telemetry Update - CPU: {telemetry['cpu_usage']}%, Memory: {telemetry['memory_percent']}%, Disk: {telemetry['disk_percent']}%]"
    
    full_prompt = f"{system_context}\nUser Directive: {user_prompt}"
    
    try:
        response = chat_session.send_message(full_prompt)
        ai_reply = response.text
    except Exception as e:
        ai_reply = f"Error communicating with AI core: {str(e)}"
        
    return jsonify({"response": ai_reply})

@app.route('/execute-command', methods=['POST'])
def execute_command():
    data = request.get_json()
    command = data.get('command', '')
    
    if not command:
        return jsonify({'output': 'Error: Empty command directive.'})
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        output = result.stdout if result.stdout else result.stderr
        return jsonify({'output': output})
    except subprocess.TimeoutExpired:
        return jsonify({'output': 'Error: Command execution timed out.'})
    except Exception as e:
        return jsonify({'output': f'Execution fault: {str(e)}'})

@app.route('/get-telemetry', methods=['GET'])
def get_telemetry_endpoint():
    telemetry = get_telemetry()
    return jsonify(telemetry)

@app.route('/resources')
def resources():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'cpu_percent': proc.info['cpu_percent'],
                'memory_percent': proc.info['memory_percent']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return jsonify({"processes": processes})

@app.route('/service-health')
def service_health():
    ssh = subprocess.run(['systemctl', 'status', 'argus-service'], capture_output=True, text=True)
    output = ssh.stdout if ssh.stdout else ssh.stderr
    return jsonify({"service": output if output else "No service output returned."})

@app.route('/docker-containers')
def docker_containers():
    ssh = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
    output = ssh.stdout if ssh.stdout else ssh.stderr
    return jsonify({"containers": output if output else "No container output returned."})

@app.route('/log-analysis')
def log_analysis():
    ssh = subprocess.run(['tail', '-n', '100', '/var/log/argus-service.log'], capture_output=True, text=True)
    output = ssh.stdout if ssh.stdout else ssh.stderr
    return jsonify({"logs": output if output else "No log output returned."})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)