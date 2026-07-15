import os
import shutil
import subprocess
import requests
from dotenv import load_dotenv

# Load environment variables from a .env file in the same directory
load_dotenv()

# Retrieve your secret Discord webhook URL
webhook_url = os.getenv("discord_url")

# 1. Choose a unique topic name for your phone/browser notifications
NOTIFICATION_URL = "https://ntfy.sh/atlas_server_alerts_1829"

# 2. Check the root directory '/' on Ubuntu
total, used, free = shutil.disk_usage("/")

# Convert free space to Gigabytes
free_gb = free / (1024 ** 3)
print(f"Current free space: {free_gb:.2f} GB")

# 3. Trigger the alert if free space drops below 1.0 GB
if free_gb < 1.0:
    print("Disk space low! Sending alert...")
    
    # Send a POST request to ntfy.sh to send a push notification
    payload_text = "⚠️ PANIC! atlas-01 is running out of disk space! under 1GB free."
    
    try:
        response = requests.post(NOTIFICATION_URL, data=payload_text)
        if response.status_code == 200:
            print("Alert sent successfully!")
        else:
            print(f"Failed to send alert. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
else:
    print("Disk space is healthy. No alert needed.")
    
    # Send the healthy status update to Discord
    if webhook_url:
        payload = {"content": f"🟢 Disk space is healthy: {free_gb:.2f} GB remaining. No alert needed."}
        try:
            # Discord returns a 204 No Content status code on success
            response = requests.post(webhook_url, json=payload)
            if response.status_code == 204:
                print("Healthy status sent to Discord!")
            else:
                print(f"Discord returned status code: {response.status_code}")
        except Exception as e:
            print(f"Failed to send to Discord: {e}")
    else:
        print("Warning: 'discord_url' not found in environment variables.")