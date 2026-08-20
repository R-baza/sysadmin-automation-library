import psutil
import sys

def get_telemetry():
    """Returns a dictionary of current host health metrics."""
    cpu = psutil.cpu_percent(interval=None)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return {
        "cpu_usage": cpu,
        "memory_percent": memory.percent,
        "memory_available": round(memory.available / (1024**3), 2),
        "disk_percent": disk.percent,
        "disk_free": round(disk.free / (1024**3), 2)
    }

def check_system_health():
    """Standalone sentinel check for background systemd execution."""
    print("=== Argus-AI System Health Check ===")
    data = get_telemetry()
    
    print(f"[*] CPU Usage: {data['cpu_usage']}%")
    print(f"[*] Memory Usage: {data['memory_percent']}% | Available: {data['memory_available']} GB")
    print(f"[*] Disk Usage: {data['disk_percent']}% | Free: {data['disk_free']} GB")

if __name__ == "__main__":
    check_system_health()
