#!/usr/bin/env python3
# Script Name: bind_serial_rotator.py
# Description: Automatically increments the BIND DNS zone file serial number 
#              based on the current date. Preserves daily increment sequences 
#              or resets to 01 on a new day.

import re 
import datetime
import subprocess

target = "/etc/bind/db.atlas.local"
today_date = datetime.datetime.now().strftime("%Y%m%d")

with open(target, "r") as f:
    content = f.read()
    for line in content.split("\n"):
        pattern = r"^\s*(\d+)\s*;\s*[Ss]erial"
        match = re.search(pattern, line)
        if match:
            old_serial = match.group(1)
            file_date = old_serial[:8] 

            if file_date == today_date:
                new_serial = str(int(old_serial) + 1)
            else:
                new_serial = today_date + "01"
            
            print(f"Updating serial from {old_serial} to {new_serial}")
            content = content.replace(old_serial, new_serial)
            break

# 1. Write the updated content to disk FIRST
with open(target, "w") as f:
    f.write(content)

# 2. Run the syntax check against the updated file on disk
check_results = subprocess.run(
    ["named-checkzone", "atlas.local", target], 
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# 3. Evaluate the return code properly (0 means success)
if check_results.returncode == 0:
    print("[+] Zone file syntax is valid!")
else:
    print("[-] ERROR: Zone file syntax check failed!")
    print(check_results.stderr)
    exit(1)

            


