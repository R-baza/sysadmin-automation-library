import shutil
import psutil
import requests
import os
from dotenv import load_dotenv
import subprocess

load_dotenv()
webhook_url = os.getenv("discord_url")
approved_users = ["root",
"daemon",
"bin",
"sys",
"sync",
"games",
"lp",
"mail",
"news",
"uucp",
"proxy",
"www-data",
"backup",
"list",
"irc",
"_apt",
"nobody",
"systemd-network",
"dhcpcd",
"messagebus",
"systemd-resolve",
"_chrony",
"usbmux",
"pollinate",
"polkitd",
"syslog",
"uuidd",
"tcpdump",
"tss",
"landscape",
"fwupd-refresh",
"atlas-01",
"sshd",
"atlas-02",
"atlas-03",
"atlas-04",
"posidon_1",
"posidon-2",
"posidon-3"]
with open("/etc/passwd", "r") as f:
    users = f.read().split("\n")
    for user in users:
        if not user.strip():
            continue
        parts = user.split(":")
        username = parts[0]
        if username not in approved_users:
            print(f"Warning: Unapproved user found: {username}")
            payload = {"content": f"Warning: Unapproved user found: {username}"}
            requests.post(webhook_url, json=payload)

total, used, free = shutil.disk_usage("/")
percent_used = (used / total) * 100
if percent_used > 78: 
   payload = {"content": f"Warning: Disk usage is {percent_used:.1f}%"}
   requests.post(webhook_url, json=payload)
