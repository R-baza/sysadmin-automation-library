import csv
import os
import re
import requests  
from dotenv import load_dotenv

load_dotenv("/home/atlas-01/sysadmin-tooling/.env")

webhook_url = os.getenv("discord_url")
fields = ["Timestamp", "Username", "IP_Address"]

failed_count = 0

with open("/var/log/auth.log", "r") as log_file:
    with open("/home/atlas-01/sysadmin-tooling/failed_logins.csv", "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()

        for line in log_file:
            match = re.search(
                r"(.*) (myserver|atlas).*Failed password for (\S+) from (\S+)",
                line,
            )
            if match:
                data = {
                    "Timestamp": match.group(1).strip(),
                    "Username": match.group(3),
                    "IP_Address": match.group(4),
                }
                failed_count += 1
                writer.writerow(data)


payload = {"content": f"🚨 Failed logins parsed and saved to failed_logins.csv. Total failed logins: {failed_count}"}
response = requests.post(webhook_url, json=payload)


if response.status_code == 204:
    print("Discord notified successfully!")
else:
    print(f"Failed to send Discord notification. Status code: {response.status_code}")

