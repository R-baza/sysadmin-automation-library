#!/usr/bin/env python3
import subprocess
import os
import datetime
import requests
from dotenv import load_dotenv

def send_discord_notification(message):
    load_dotenv()
    webhook_url = os.getenv("discord_url")
    
    payload = {"content": message}
    try:
        requests.post(webhook_url, json=payload)
    except requests.exceptions.RequestException as e:
        print(f"Failed to send webhook: {e}")
date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  

backup_source = os.environ.get("BACKUP_SOURCE", "/home/atlas-01/sysadmin-automation-library/deploy")
backup_filename = f"backup_{date}.tar.gz"

if not os.path.exists(backup_source):
   
    msg = f"Error: Backup source '{backup_source}' does not exist"
    print(msg)
    send_discord_notification(f"❌ {msg}")
    exit(1)

try: 
    result = subprocess.run(["tar", "-czf", backup_filename, backup_source], 
                            check=True, 
                            capture_output=True, 
                            text=True)
   
    success_msg = f"Backup created successfully: {backup_filename}"
    print(success_msg)
    send_discord_notification(f"✅ {success_msg}")

except subprocess.CalledProcessError as e:
    fail_msg = f"Backup failed: {e.stderr}"
    print(fail_msg)
    send_discord_notification(f"❌ {fail_msg}")
 


    



