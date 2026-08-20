#!/usr/bin/env python3
import os
import pathlib
import stat
import requests

from dotenv import load_dotenv

load_dotenv()
webhook_url = os.getenv("discord_url")

folder = pathlib.Path("/home/atlas-01/private_folder")


if os.path.exists(folder):
    violation_detected = False
    permissions = stat.S_IMODE(os.stat(folder).st_mode)
    
    if os.stat(folder).st_uid != 1000:
        with open("access_alert.log", "a") as log:
            log.write(f"Unauthorized access to {folder} by user {os.getuid()}\n")
        violation_detected = True
    
    if permissions != 0o700:
        with open("access_alert.log", "a") as log:
            log.write(f"Unauthorized access to {folder} by user {os.getuid()}\n")
        violation_detected = True

    if violation_detected:
        requests.post(webhook_url, json={"content": "Unauthorized access detected on private folder!"})
        print("Unauthorized access detected on private folder!")
        exit(1)









