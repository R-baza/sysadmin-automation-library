import os
import re
import requests
from dotenv import load_dotenv

# 1. Get the directory of the script 
script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Go up one level to the repository root folder 
repo_root = os.path.dirname(script_dir)

# 3. Load the central .env file from the root folder
load_dotenv(dotenv_path=os.path.join(repo_root, ".env"))

webhook_url = os.getenv("discord_url")

# The Regex pattern to find the IP and username from a failed attempt
# Example line: "Jul 14 12:00:00 atlas sshd[1234]: Failed password for invalid user admin from 203.0.113.5 port 54321 ssh2"
log_pattern = r"Failed password for (?:invalid user )?(\S+) from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"

failed_attempts = {}

# Open and read the file line-by-line
with open("/var/log/auth.log", "r") as f:
    for line in f:
        match = re.search(log_pattern, line)
        if match:
            username = match.group(1)
            ip_address = match.group(2)
            
            # Track how many times each IP has failed
            failed_attempts[ip_address] = failed_attempts.get(ip_address, 0) + 1
            
            print(f"Failed password attempt detected from {ip_address} using username '{username}'")
            
            # Construct a detailed alert payload
            payload = {
                "content": f"🚨 **SSH Brute Force Warning** 🚨\n"
                           f"**User Targeted:** `{username}`\n"
                           f"**Attacker IP:** `{ip_address}`\n"
                           f"**Total Failed Attempts from this IP:** {failed_attempts[ip_address]}"
            }
            
            # Send to Discord
            requests.post(webhook_url, json=payload)

